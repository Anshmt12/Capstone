"""Text-to-SQL agent using LangChain."""
import logging
import sqlite3
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.agents.llm_provider import get_llm
from app.sql.database import get_connection, get_table_info

logger = logging.getLogger(__name__)

SQL_PROMPT = ChatPromptTemplate.from_template("""You are a SQL expert working with an Indian legal case database.
Given the database schema and a natural language question, generate a valid SQLite query.
Return ONLY the SQL query, nothing else. No markdown, no explanation.

Database Schema:
{schema}

Sample values:
- status: 'pending', 'won', 'lost', 'settled', 'appealed'
- case_type: 'Civil', 'Criminal', 'Constitutional', 'Corporate', 'Family', 'Tax', 'Labor', 'Property', 'Environmental', 'IP'
- legal_area: 'Fundamental Rights', 'Criminal Law', 'Contract Law', 'Property Law', 'Family Law', 'Tax Law', 'Corporate Law', 'Environmental Law', 'Labor Law', 'IP Law'
- court: 'Supreme Court of India', 'Delhi High Court', 'Bombay High Court', 'Madras High Court', etc.
- articles_invoked: comma-separated like '14,19,21'
- priority: 'low', 'medium', 'high', 'critical'

Question: {question}

SQL Query:""")

EXPLAIN_PROMPT = ChatPromptTemplate.from_template("""You are a legal data analyst.
Given a SQL query and its results from an Indian legal case database, provide a clear, 
concise natural language explanation of the findings.

SQL Query: {sql}
Results: {results}
Original Question: {question}

Explanation:""")


class SQLAgent:
    """Natural language to SQL agent for case analytics."""

    def __init__(self):
        self.llm = get_llm(temperature=0.0)
        self.sql_chain = SQL_PROMPT | self.llm | StrOutputParser()
        self.explain_chain = EXPLAIN_PROMPT | self.llm | StrOutputParser()

    def query(self, question: str) -> dict:
        """Convert natural language to SQL, execute, and explain results."""
        schema = get_table_info()
        # Generate SQL
        sql = self.sql_chain.invoke({"schema": schema, "question": question})
        sql = sql.strip().strip("`").strip()
        if sql.lower().startswith("sql"):
            sql = sql[3:].strip()

        # Safety: only allow SELECT
        if not sql.upper().lstrip().startswith("SELECT"):
            return {"error": "Only SELECT queries are allowed.", "sql": sql}

        # Execute
        try:
            conn = get_connection()
            cursor = conn.execute(sql)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.close()
        except sqlite3.Error as e:
            return {"error": str(e), "sql": sql}

        # Explain results
        explanation = self.explain_chain.invoke({
            "sql": sql,
            "results": str(rows[:3]),
            "question": question,
        })

        return {
            "sql": sql,
            "columns": columns,
            "rows": rows[:100],
            "total_rows": len(rows),
            "explanation": explanation,
        }
