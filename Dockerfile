FROM python:3.11-slim

# Install system deps (Tesseract OCR)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr  \
    libpq-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download embedding model at build time so it's cached in the image layer
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-base-en-v1.5')"

COPY . .

# Kaggle credentials — passed as build args (set as secrets in CI/CD)
# These are only used at build time to download the dataset; not stored in the final image
ARG KAGGLE_USERNAME=""
ARG KAGGLE_KEY=""
ENV KAGGLE_USERNAME=$KAGGLE_USERNAME
ENV KAGGLE_KEY=$KAGGLE_KEY

# Pre-populate ChromaDB and SQLite at build time.
# If chroma_db already exists (e.g. copied from local data/), skip ingestion.
RUN python scripts/seed_database.py && \
    if [ ! -f "data/chroma_db/chroma.sqlite3" ]; then \
      echo "ChromaDB not found — running ingestion..."; \
      python scripts/ingest_constitution.py; \
    else \
      echo "ChromaDB already present — skipping ingestion."; \
    fi

# Clear Kaggle credentials from environment after build
ENV KAGGLE_USERNAME=""
ENV KAGGLE_KEY=""

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
