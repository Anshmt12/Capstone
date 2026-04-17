# AI Legal Co-Counsel

AI-powered assistant for Indian lawyers featuring RAG-based legal research, Text-to-SQL case analytics, and a multi-agent debate system — all using free LLM APIs.

## Architecture

```
┌─────────────┐     ┌──────────────────────────────────────────────┐
│   Client     │────▶│  FastAPI Backend (port 8000)                 │
└─────────────┘     │                                              │
                    │  POST /api/query ──────▶ LangGraph Orchestrator
                    │    ├── RAG Agent (LangChain + pgvector)      │
                    │    ├── Advocate Agent (strengths)             │
                    │    ├── Critic Agent (weaknesses)              │
                    │    └── Mediator Agent (strategic brief)       │
                    │                                              │
                    │  POST /api/sql/query ──▶ Text-to-SQL Agent   │
                    │    └── SQLite (220 synthetic Indian cases)    │
                    │                                              │
                    │  POST /api/documents/upload ──▶ Doc Parser   │
                    │    └── PyMuPDF + Tesseract OCR → pgvector    │
                    │                                              │
                    │  POST /api/cases/import ──▶ Excel/CSV Import │
                    └──────────────────────────────────────────────┘
                              │                    │
                    ┌─────────┘                    └──────────┐
                    ▼                                         ▼
              PostgreSQL + pgvector                    SQLite (cases)
              (Indian Constitution,                   (220 synthetic
               SC judgments, uploads)                   legal cases)
```

## Quick Start

### 1. Clone and configure

```bash
cp .env.example .env
# Edit .env — add at least one API key (Groq recommended)
```

### 2. Run with Docker (recommended)

```bash
docker-compose up --build
```

This starts PostgreSQL with pgvector, seeds the database with 220 cases, ingests 50 Indian legal document chunks, and launches the API on port 8000.

### 3. Run without Docker

```bash
# Install PostgreSQL with pgvector extension first
pip install -r requirements.txt
python scripts/seed_database.py
python scripts/ingest_constitution.py
uvicorn app.main:app --reload
```

## API Endpoints

### `POST /api/query` — Legal Research + Debate

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Can Article 21 be invoked for environmental protection?", "run_debate": true}'
```

Response includes: RAG research, Advocate arguments (Round 1), Critic challenges, Advocate rebuttal (Round 2), and Mediator's strategic brief.

Set `"run_debate": false` for RAG-only response.

### `POST /api/sql/query` — Case Analytics

```bash
curl -X POST http://localhost:8000/api/sql/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many Article 21 cases did we win?"}'
```

### `POST /api/documents/upload` — Upload Legal Documents

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@judgment.pdf"
```

### `POST /api/cases/import` — Import Cases from Excel/CSV

```bash
curl -X POST http://localhost:8000/api/cases/import \
  -F "file=@cases.xlsx" \
  -F 'column_mapping={"Case No": "case_number", "Title": "case_title", "Court": "court"}'
```

## Example Queries

**Legal Research:**
- "What are the fundamental rights under Part III of the Indian Constitution?"
- "Explain the basic structure doctrine and its significance"
- "What protections exist for arrested persons under Indian law?"

**Case Analytics (Text-to-SQL):**
- "How many cases are pending in the Supreme Court?"
- "What is our win rate for constitutional cases?"
- "Show top 5 cases by damages awarded"
- "Which judge has the most cases assigned?"

**Multi-Agent Debate:**
- "My client is challenging a property acquisition under Article 300A. The state claims eminent domain but compensation offered is below market value. What are our options?"

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Groq / OpenRouter / HuggingFace (free tiers) |
| Embeddings | BAAI/bge-base-en-v1.5 (local) |
| RAG | LangChain |
| Multi-Agent | LangGraph |
| Text-to-SQL | LangChain |
| Backend | FastAPI |
| Vector DB | PostgreSQL + pgvector |
| Case DB | SQLite |
| Doc Parsing | PyMuPDF + Tesseract OCR |
| External Integration | MCP Server |
| Deployment | Docker + docker-compose |

## MCP Server

The MCP server exposes three tools for external integration:

- `legal_research` — RAG-based legal search
- `case_analytics` — Natural language SQL queries
- `legal_debate` — Full multi-agent debate

Run standalone: `python -m app.mcp.server`

## Project Structure

```
legal-cocounsel/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Settings and API keys
│   ├── agents/
│   │   ├── orchestrator.py     # LangGraph state machine
│   │   ├── llm_provider.py     # LLM abstraction (Groq/OpenRouter/HF)
│   │   ├── rag_agent.py        # RAG with LangChain
│   │   ├── advocate_agent.py   # Finds strengths
│   │   ├── critic_agent.py     # Finds weaknesses
│   │   └── mediator_agent.py   # Synthesizes debate
│   ├── rag/
│   │   ├── embeddings.py       # HuggingFace embeddings
│   │   ├── vector_store.py     # pgvector operations
│   │   └── retriever.py        # LangChain retriever
│   ├── parsers/
│   │   └── document_parser.py  # PDF + OCR parsing
│   ├── sql/
│   │   ├── database.py         # SQLite setup
│   │   └── text_to_sql.py      # NL to SQL
│   └── mcp/
│       └── server.py           # MCP tools
├── data/
│   ├── constitution/
│   │   └── indian_law_chunks.py
│   └── seed_cases.py           # 220 synthetic cases
├── scripts/
│   ├── ingest_constitution.py
│   └── seed_database.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Free API Keys

1. **Groq** (recommended): https://console.groq.com → Create API key
2. **OpenRouter**: https://openrouter.ai/keys → Free models available
3. **HuggingFace**: https://huggingface.co/settings/tokens → Access token

## License

MIT
