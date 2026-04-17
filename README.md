# AI Legal Co-Counsel

An AI-powered legal assistant for Indian lawyers featuring RAG-based legal research, a multi-agent debate system, Text-to-SQL case analytics, document OCR ingestion, and safety guardrails — deployed on Azure with a full CI/CD pipeline.

## Live Demo

| Service | URL |
|---------|-----|
| Frontend | https://legal-cocounsel-frontend.azurewebsites.net |
| API | https://legal-cocounsel-api.azurewebsites.net |
| API Docs | https://legal-cocounsel-api.azurewebsites.net/docs |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│   Streamlit Frontend (Port 8501)                                │
│   4 Tabs: Legal Research | Documents | Case Analytics | Guardrail Test │
└──────────────────────┬──────────────────────────────────────────┘
                       │ HTTP
┌──────────────────────▼──────────────────────────────────────────┐
│   FastAPI Backend (Port 8000)                                   │
│                                                                 │
│  ┌─────────────────┐   ┌──────────────────────────────────┐    │
│  │ Input Guardrails│   │ LangGraph Orchestrator           │    │
│  │ - Jailbreak     │   │                                  │    │
│  │ - PII Redaction │──▶│  RAG Agent                       │    │
│  │ - Harmful       │   │    └── ChromaDB (12,170 chunks)  │    │
│  │ - Off-topic     │   │  Advocate Agent (strengths)      │    │
│  └─────────────────┘   │  Critic Agent (weaknesses)       │    │
│                        │  Mediator Agent (strategy)       │    │
│  ┌─────────────────┐   └──────────────────────────────────┘    │
│  │ Output Guardrails│                                          │
│  │ - Citation check│   ┌──────────────────────────────────┐    │
│  │ - Hallucination │   │ SQL Agent (Text-to-SQL)          │    │
│  │ - Harmful advice│   │  └── SQLite (220 cases)          │    │
│  │ - Disclaimer    │   └──────────────────────────────────┘    │
│  └─────────────────┘                                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
        ChromaDB                        SQLite
   (Indian Constitution,            (220 synthetic
    IPC, CrPC — 12,170 chunks)       Indian cases)
```

---

## Features

### 1. Legal Research (RAG)
- Semantic search over 12,170 legal Q&A chunks from the Indian Constitution, IPC, and CrPC
- Sourced from Kaggle dataset (`akshatgupta7/llm-fine-tuning-dataset-of-indian-legal-texts`)
- 10 additional landmark Supreme Court judgment chunks (Kesavananda Bharati, Maneka Gandhi, Puttaswamy, etc.)
- Retriever filters out non-Indian sources at query time
- Answers grounded in retrieved context with proper legal citations

### 2. Multi-Agent Debate (LangGraph)
A 5-step LangGraph state machine:
```
RAG Research → Advocate (Round 1) → Critic → Advocate (Rebuttal) → Mediator
```
- **RAG Agent**: retrieves relevant Indian law context
- **Advocate**: builds strongest arguments for the client
- **Critic**: challenges weaknesses, opposing arguments
- **Advocate (Round 2)**: rebuts the Critic
- **Mediator**: synthesizes a strategic legal brief

### 3. Case Analytics (Text-to-SQL)
- Natural language → SQL queries over 220 synthetic Indian cases
- Covers: courts, judges, case types, articles invoked, damages, win/loss status
- Example: *"How many Article 21 cases did we win in the Supreme Court?"*

### 4. Document Upload & OCR
- Upload PDFs, images (PNG, JPG), or text files
- PyMuPDF extracts text from digital PDFs
- Tesseract OCR handles scanned documents and images
- Chunks added to ChromaDB for immediate semantic search

### 5. Guardrails
**Input Guardrails:**
- Jailbreak / prompt injection detection
- Indian PII detection & redaction (Aadhaar, PAN, phone)
- Off-topic query blocking
- Harmful legal request blocking (evidence tampering, bribery)
- Query length validation

**Output Guardrails:**
- Hallucination indicator detection
- Citation format validation (SCC, AIR, SCR)
- Harmful advice detection
- Foreign law misuse detection
- Auto-appends legal disclaimer
- Returns confidence score (0.0–1.0)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| Multi-Agent | LangGraph |
| RAG | LangChain + ChromaDB |
| LLM | Groq (`llama-3.1-8b-instant`) / OpenRouter / HuggingFace |
| Embeddings | `BAAI/bge-base-en-v1.5` (local, no API needed) |
| Document Parsing | PyMuPDF + Tesseract OCR |
| Case Database | SQLite |
| Vector Database | ChromaDB (local persistence) |
| Dataset | Kaggle: `akshatgupta7/llm-fine-tuning-dataset-of-indian-legal-texts` |
| Containerization | Docker |
| Registry | Azure Container Registry (ACR) |
| Hosting | Azure App Service |
| CI/CD | GitHub Actions |

---

## Quick Start

### Run Locally

```bash
# 1. Clone and set up environment
git clone https://github.com/Anshmt12/Capstone.git
cd Capstone
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env — add GROQ_API_KEY (get free at console.groq.com)

# 3. Seed database and ingest legal documents
python scripts/seed_database.py
python scripts/ingest_constitution.py  # downloads Kaggle dataset

# 4. Run the API
uvicorn app.main:app --reload

# 5. Run the frontend (separate terminal)
streamlit run frontend/app.py
```

### Run with Docker

```bash
docker-compose up --build
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/query` | POST | Legal research + optional multi-agent debate |
| `/api/sql/query` | POST | Natural language case analytics |
| `/api/documents/upload` | POST | Upload PDF/image for OCR + ingestion |
| `/api/cases/import` | POST | Import cases from Excel/CSV |
| `/api/health` | GET | Health check |

### Example Requests

```bash
# Legal research with debate
curl -X POST https://legal-cocounsel-api.azurewebsites.net/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Can Article 21 be invoked for environmental protection?", "run_debate": true}'

# Case analytics
curl -X POST https://legal-cocounsel-api.azurewebsites.net/api/sql/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many cases are pending in the Supreme Court?"}'

# Upload a document
curl -X POST https://legal-cocounsel-api.azurewebsites.net/api/documents/upload \
  -F "file=@judgment.pdf"
```

---

## Dataset

The knowledge base is built from the Kaggle dataset `akshatgupta7/llm-fine-tuning-dataset-of-indian-legal-texts`:

| File | Entries | Loaded | Source |
|------|---------|--------|--------|
| `constitution_qa.json` | 4,082 | 3,390 | Indian Constitution |
| `ipc_qa.json` | 2,267 | 2,019 | Indian Penal Code |
| `crpc_qa.json` | 8,194 | 6,751 | Code of Criminal Procedure |
| Landmark judgments | 10 | 10 | Hardcoded SC judgments |
| **Total** | **14,553** | **12,170** | |

Short/stub answers are filtered out (min 30 characters). Each Q&A pair is stored as `Q: ...\nA: ...` for optimal semantic search.

---

## CI/CD Pipeline

Every push to `main` automatically:

```
git push → GitHub Actions triggers
  → Docker build (ubuntu-latest runner)
  → Push API image to ACR (:latest + :git-sha)
  → Push Frontend image to ACR
  → Azure App Service restarts with new image
  → Both apps live within ~10 minutes
```

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `ACR_USERNAME` | Azure Container Registry username |
| `ACR_PASSWORD` | Azure Container Registry password |
| `KAGGLE_USERNAME` | Kaggle username (for dataset download at build time) |
| `KAGGLE_KEY` | Kaggle API key |
| `AZURE_API_PUBLISH_PROFILE` | App Service publish profile XML (API) |
| `AZURE_FRONTEND_PUBLISH_PROFILE` | App Service publish profile XML (Frontend) |

---

## Project Structure

```
legal-cocounsel/
├── app/
│   ├── main.py                  # FastAPI app + all endpoints
│   ├── config.py                # Settings and env vars
│   ├── agents/
│   │   ├── orchestrator.py      # LangGraph debate state machine
│   │   ├── llm_provider.py      # Groq / OpenRouter / HuggingFace
│   │   ├── rag_agent.py         # RAG with LangChain
│   │   ├── advocate_agent.py    # Finds strengths
│   │   ├── critic_agent.py      # Finds weaknesses
│   │   └── mediator_agent.py    # Synthesizes debate
│   ├── rag/
│   │   ├── embeddings.py        # BAAI/bge-base-en-v1.5
│   │   ├── vector_store.py      # ChromaDB operations
│   │   └── retriever.py         # Indian-law-only retriever
│   ├── guardrails/
│   │   ├── input_guardrail.py   # Query validation
│   │   ├── output_guardrail.py  # Response validation
│   │   └── retrieval_guardrail.py
│   ├── parsers/
│   │   └── document_parser.py  # PyMuPDF + Tesseract OCR
│   ├── sql/
│   │   ├── database.py          # SQLite setup
│   │   └── text_to_sql.py       # NL → SQL
│   └── mcp/
│       └── server.py            # MCP server (external integration)
├── frontend/
│   └── app.py                   # Streamlit UI
├── data/
│   ├── constitution/
│   │   └── indian_law_chunks.py # Reference chunks (not ingested)
│   ├── seed_cases.py            # 220 synthetic case generator
│   ├── chroma_db/               # ChromaDB persistence
│   └── cases.db                 # SQLite case database
├── scripts/
│   ├── ingest_constitution.py   # Downloads Kaggle dataset → ChromaDB
│   └── seed_database.py         # Seeds SQLite with 220 cases
├── .github/
│   └── workflows/
│       └── deploy.yml           # CI/CD pipeline
├── Dockerfile                   # API image (includes Tesseract via apt)
├── Dockerfile.frontend          # Streamlit image
├── docker-compose.yml           # Local development
└── requirements.txt
```

---

## Free API Keys

| Provider | URL | Model Used |
|----------|-----|-----------|
| Groq (recommended) | console.groq.com | `llama-3.1-8b-instant` |
| OpenRouter | openrouter.ai/keys | `meta-llama/llama-3.1-8b-instruct:free` |
| HuggingFace | huggingface.co/settings/tokens | `Meta-Llama-3.1-8B-Instruct` |

---

## Disclaimer

This tool provides AI-generated legal information based on Indian law for research purposes only. It does not constitute legal advice. Always consult a qualified advocate for specific legal matters.

---

## License

MIT
