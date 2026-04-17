"""MCP Server exposing legal co-counsel tools for external integration."""
import json
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from app.agents.rag_agent import RAGAgent
from app.sql.text_to_sql import SQLAgent
from app.agents.orchestrator import run_debate

logger = logging.getLogger(__name__)

server = Server("legal-cocounsel-mcp")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="legal_research",
            description="Search Indian legal documents (Constitution, Supreme Court judgments) using RAG",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Legal research question"}
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="case_analytics",
            description="Query case database using natural language (converts to SQL)",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Analytics question about cases"}
                },
                "required": ["question"],
            },
        ),
        Tool(
            name="legal_debate",
            description="Run multi-agent debate (Advocate vs Critic) with strategic brief",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Case details or legal question"}
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "legal_research":
            rag = RAGAgent()
            result = rag.query(arguments["query"])
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "case_analytics":
            sql_agent = SQLAgent()
            result = sql_agent.query(arguments["question"])
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

        elif name == "legal_debate":
            result = run_debate(arguments["query"])
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.error(f"MCP tool error: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def run_mcp_server():
    """Run the MCP server over stdio."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_mcp_server())
