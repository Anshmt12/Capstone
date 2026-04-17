#!/bin/bash
# =============================================================================
# Azure Deployment Script — Legal Co-Counsel
# Deploys: ACR, PostgreSQL Flexible Server, Container Apps (API + Frontend)
# Usage: ./deploy-azure.sh
# =============================================================================
set -euo pipefail

# ─── CONFIG — edit these ────────────────────────────────────────────────────
RESOURCE_GROUP="legal-cocounsel-rg"
LOCATION="eastus"
ACR_NAME="legalcocounselacr"          # must be globally unique, lowercase, 5-50 chars
POSTGRES_SERVER="legal-cocounsel-pg"  # must be globally unique
POSTGRES_DB="legal_cocounsel"
POSTGRES_USER="pgadmin"
POSTGRES_PASSWORD="Change_me_123!"    # change before running
ENV_NAME="legal-cocounsel-env"
API_APP_NAME="legal-cocounsel-api"
FRONTEND_APP_NAME="legal-cocounsel-frontend"
# ─────────────────────────────────────────────────────────────────────────────

echo "==> Logging in to Azure..."
az account show > /dev/null 2>&1 || az login

echo "==> Creating resource group: $RESOURCE_GROUP"
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

# ─── Azure Container Registry ────────────────────────────────────────────────
echo "==> Creating ACR: $ACR_NAME"
az acr create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$ACR_NAME" \
  --sku Basic \
  --admin-enabled true

ACR_LOGIN_SERVER=$(az acr show --name "$ACR_NAME" --query loginServer -o tsv)
ACR_USERNAME=$(az acr credential show --name "$ACR_NAME" --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --query "passwords[0].value" -o tsv)

echo "==> ACR login server: $ACR_LOGIN_SERVER"

# ─── Build & push images ─────────────────────────────────────────────────────
echo "==> Building and pushing API image..."
az acr build \
  --registry "$ACR_NAME" \
  --image "legal-cocounsel-api:latest" \
  --file Dockerfile \
  .

echo "==> Building and pushing frontend image..."
az acr build \
  --registry "$ACR_NAME" \
  --image "legal-cocounsel-frontend:latest" \
  --file Dockerfile.frontend \
  .

# ─── PostgreSQL Flexible Server ──────────────────────────────────────────────
echo "==> Creating PostgreSQL Flexible Server: $POSTGRES_SERVER"
az postgres flexible-server create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$POSTGRES_SERVER" \
  --location "$LOCATION" \
  --admin-user "$POSTGRES_USER" \
  --admin-password "$POSTGRES_PASSWORD" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 16 \
  --public-access 0.0.0.0

echo "==> Enabling pgvector extension..."
az postgres flexible-server parameter set \
  --resource-group "$RESOURCE_GROUP" \
  --server-name "$POSTGRES_SERVER" \
  --name azure.extensions \
  --value vector

echo "==> Creating database: $POSTGRES_DB"
az postgres flexible-server db create \
  --resource-group "$RESOURCE_GROUP" \
  --server-name "$POSTGRES_SERVER" \
  --database-name "$POSTGRES_DB"

POSTGRES_HOST="${POSTGRES_SERVER}.postgres.database.azure.com"

# ─── Container Apps Environment ──────────────────────────────────────────────
echo "==> Creating Container Apps environment: $ENV_NAME"
az containerapp env create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$ENV_NAME" \
  --location "$LOCATION"

# ─── Deploy API Container App ────────────────────────────────────────────────
echo "==> Deploying API Container App: $API_APP_NAME"
echo "    NOTE: Set your OPENAI_API_KEY and other secrets via:"
echo "    az containerapp secret set --name $API_APP_NAME ..."

az containerapp create \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$ENV_NAME" \
  --name "$API_APP_NAME" \
  --image "${ACR_LOGIN_SERVER}/legal-cocounsel-api:latest" \
  --registry-server "$ACR_LOGIN_SERVER" \
  --registry-username "$ACR_USERNAME" \
  --registry-password "$ACR_PASSWORD" \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 3 \
  --cpu 1.0 \
  --memory 2.0Gi \
  --env-vars \
    POSTGRES_HOST="$POSTGRES_HOST" \
    POSTGRES_PORT="5432" \
    POSTGRES_DB="$POSTGRES_DB" \
    POSTGRES_USER="${POSTGRES_USER}@${POSTGRES_SERVER}" \
    POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    SQLITE_DB="/app/data/cases.db"

API_URL=$(az containerapp show \
  --resource-group "$RESOURCE_GROUP" \
  --name "$API_APP_NAME" \
  --query "properties.configuration.ingress.fqdn" -o tsv)

echo "==> API deployed at: https://$API_URL"

# ─── Run seed scripts inside the API container ──────────────────────────────
echo "==> Running database seed scripts..."
az containerapp exec \
  --resource-group "$RESOURCE_GROUP" \
  --name "$API_APP_NAME" \
  --command "python scripts/seed_database.py && python scripts/ingest_constitution.py" \
  || echo "    WARN: Could not run seed scripts automatically. Run manually after deploy."

# ─── Deploy Frontend Container App ──────────────────────────────────────────
echo "==> Deploying Frontend Container App: $FRONTEND_APP_NAME"
az containerapp create \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$ENV_NAME" \
  --name "$FRONTEND_APP_NAME" \
  --image "${ACR_LOGIN_SERVER}/legal-cocounsel-frontend:latest" \
  --registry-server "$ACR_LOGIN_SERVER" \
  --registry-username "$ACR_USERNAME" \
  --registry-password "$ACR_PASSWORD" \
  --target-port 8501 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 2 \
  --cpu 0.5 \
  --memory 1.0Gi \
  --env-vars \
    API_BASE_URL="https://${API_URL}/api"

FRONTEND_URL=$(az containerapp show \
  --resource-group "$RESOURCE_GROUP" \
  --name "$FRONTEND_APP_NAME" \
  --query "properties.configuration.ingress.fqdn" -o tsv)

echo ""
echo "============================================================"
echo " Deployment complete!"
echo " API:      https://$API_URL"
echo " Frontend: https://$FRONTEND_URL"
echo "============================================================"
echo ""
echo "NEXT STEPS:"
echo "  1. Set your API keys as secrets:"
echo "     az containerapp secret set \\"
echo "       --resource-group $RESOURCE_GROUP \\"
echo "       --name $API_APP_NAME \\"
echo "       --secrets openai-key=<YOUR_KEY> groq-key=<YOUR_KEY>"
echo ""
echo "  2. Update env vars to reference secrets:"
echo "     az containerapp update \\"
echo "       --resource-group $RESOURCE_GROUP \\"
echo "       --name $API_APP_NAME \\"
echo "       --set-env-vars OPENAI_API_KEY=secretref:openai-key"
