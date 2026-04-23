"""MCP Server exposing legal co-counsel tools - stdio (local) and SSE (Azure)."""
import json
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.requests import Request
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


# ─── SSE transport (for Azure deployment) ────────────────────────────────────

sse = SseServerTransport("/messages/")


async def handle_sse(request: Request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())


starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
        Route("/health", endpoint=lambda _: __import__("starlette.responses", fromlist=["JSONResponse"]).JSONResponse({"status": "ok"})),
    ]
)


# ─── stdio transport (for local Claude Desktop) ───────────────────────────────

async def run_mcp_server():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_mcp_server())
