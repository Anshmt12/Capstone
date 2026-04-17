"""AI Legal Co-Counsel - FastAPI Backend with Guardrails."""
import logging
import os
import shutil
from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import settings
from app.agents.orchestrator import run_debate
from app.agents.rag_agent import RAGAgent
from app.sql.text_to_sql import SQLAgent
from app.sql.database import init_db, get_connection
from app.parsers.document_parser import DocumentParser
from app.rag.vector_store import add_documents

# ═══════════════════════════════════════════════════════════════════════════════
# GUARDRAILS IMPORT - ADD THIS
# ═══════════════════════════════════════════════════════════════════════════════
from app.guardrails import (
    validate_input,
    validate_output,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Legal Co-Counsel",
    description="AI assistant for Indian lawyers - RAG, Text-to-SQL, Multi-Agent Debate",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


# ─── Request / Response Models ────────────────────────────────────────────────

class QueryRequest(BaseModel):
    query: str
    run_debate: bool = True  # If True, runs full debate; if False, just RAG


class SQLQueryRequest(BaseModel):
    question: str


class ImportConfig(BaseModel):
    column_mapping: Optional[dict] = None  # {"csv_col": "db_col", ...}


# ─── Startup ──────────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    init_db()
    logger.info("Database initialized. AI Legal Co-Counsel ready.")


# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"message": "AI Legal Co-Counsel API", "version": "1.0.0", "docs": "/docs"}


@app.post("/api/query")
async def legal_query(req: QueryRequest):
    """Legal research query - triggers RAG + optional multi-agent debate."""
    try:
        # ═══════════════════════════════════════════════════════════════════
        # STEP 1: INPUT GUARDRAIL - Validate query before processing
        # ═══════════════════════════════════════════════════════════════════
        input_passed, input_message, processed_query = validate_input(req.query)
        
        if not input_passed:
            logger.warning(f"Input guardrail blocked query: {input_message}")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "invalid_query",
                    "message": input_message
                }
            )
        
        # Use processed query (may have PII redacted)
        query = processed_query
        logger.info(f"Input guardrail passed for query: {query[:50]}...")
        
        # ═══════════════════════════════════════════════════════════════════
        # STEP 2: EXECUTE RAG OR DEBATE
        # ═══════════════════════════════════════════════════════════════════
        if req.run_debate:
            result = run_debate(query)
            response_text = result.get("strategic_brief", "")
            response_type = "debate"
        else:
            rag = RAGAgent()
            result = rag.query(query)
            response_text = result.get("answer", "")
            response_type = "rag"
        
        # ═══════════════════════════════════════════════════════════════════
        # STEP 3: OUTPUT GUARDRAIL - Validate response before returning
        # ═══════════════════════════════════════════════════════════════════
        output_result = validate_output(
            response=response_text,
            strict_mode=False
        )
        
        if not output_result.passed:
            logger.warning(f"Output guardrail failed: {output_result.issues}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "unreliable_response",
                    "message": "Unable to generate a reliable response. Please try rephrasing your question."
                }
            )
        
        # Use modified response (includes disclaimer)
        if req.run_debate:
            result["strategic_brief"] = output_result.modified_response
        else:
            result["answer"] = output_result.modified_response
        
        return {
            "status": "success",
            "type": response_type,
            "data": result,
            "confidence": output_result.confidence_score,
            "warnings": output_result.issues if output_result.issues else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and parse a legal document (PDF, image, text)."""
    try:
        # Save file
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Parse and chunk
        parser = DocumentParser()
        chunks = parser.parse_and_chunk(file_path)

        if not chunks:
            return {"status": "warning", "message": "No text extracted", "chunks": 0}

        # Add to vector store
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        add_documents(texts, metadatas)

        return {
            "status": "success",
            "filename": file.filename,
            "chunks_created": len(chunks),
            "sample_chunk": chunks[0]["text"][:200] if chunks else "",
        }
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sql/query")
async def sql_query(req: SQLQueryRequest):
    """Natural language query over case database."""
    try:
        # ═══════════════════════════════════════════════════════════════════
        # INPUT GUARDRAIL for SQL queries too
        # ═══════════════════════════════════════════════════════════════════
        input_passed, input_message, processed_query = validate_input(req.question)
        
        if not input_passed:
            raise HTTPException(
                status_code=400,
                detail={"error": "invalid_query", "message": input_message}
            )
        
        agent = SQLAgent()
        result = agent.query(processed_query)
        return {"status": "success", "data": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"SQL query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/cases/import")
async def import_cases(
    file: UploadFile = File(...),
    column_mapping: Optional[str] = None,
):
    """Import cases from Excel/CSV with optional column mapping."""
    try:
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Read file
        ext = Path(file.filename).suffix.lower()
        if ext in (".xlsx", ".xls"):
            df = pd.read_excel(file_path)
        elif ext == ".csv":
            df = pd.read_csv(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported format. Use .xlsx, .xls, or .csv")

        # Apply column mapping if provided
        if column_mapping:
            import json
            mapping = json.loads(column_mapping)
            df = df.rename(columns=mapping)

        # Expected columns
        db_cols = [
            "case_number", "case_title", "court", "judge", "filing_date",
            "decision_date", "status", "case_type", "legal_area",
            "articles_invoked", "opposing_counsel", "client_name", "summary",
            "outcome_summary", "damages_claimed", "damages_awarded", "priority",
        ]

        # Only keep columns that exist in both
        available = [c for c in db_cols if c in df.columns]
        if "case_number" not in available or "case_title" not in available:
            return {
                "status": "error",
                "message": "File must contain at least 'case_number' and 'case_title' columns.",
                "available_columns": list(df.columns),
                "expected_columns": db_cols,
            }

        df_import = df[available].fillna("")
        conn = get_connection()
        imported = 0
        for _, row in df_import.iterrows():
            try:
                placeholders = ",".join(["?"] * len(available))
                cols = ",".join(available)
                conn.execute(
                    f"INSERT OR IGNORE INTO cases ({cols}) VALUES ({placeholders})",
                    tuple(row[c] for c in available),
                )
                imported += 1
            except Exception:
                continue
        conn.commit()
        conn.close()

        return {
            "status": "success",
            "rows_imported": imported,
            "total_rows_in_file": len(df),
            "columns_mapped": available,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Import failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "llm_provider": settings.LLM_PROVIDER,
        "guardrails": "enabled"  # Added guardrails status
    }


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)