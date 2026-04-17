"""LangGraph orchestrator - multi-agent debate system."""
import logging
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from app.agents.rag_agent import RAGAgent
from app.agents.advocate_agent import AdvocateAgent
from app.agents.critic_agent import CriticAgent
from app.agents.mediator_agent import MediatorAgent

logger = logging.getLogger(__name__)


class DebateState(TypedDict):
    query: str
    research_context: str
    research_sources: list
    advocate_round1: str
    critic_response: str
    advocate_round2: str
    mediator_brief: str
    debate_log: list
    error: str


def research_node(state: DebateState) -> dict:
    """RAG retrieval step."""
    try:
        rag = RAGAgent()
        result = rag.query(state["query"])
        return {
            "research_context": result["answer"],
            "research_sources": result["sources"],
            "debate_log": state.get("debate_log", []) + [
                {"agent": "RAG", "action": "research", "summary": f"Retrieved {len(result['sources'])} sources"}
            ],
        }
    except Exception as e:
        logger.error(f"Research failed: {e}")
        return {"error": str(e), "research_context": "No research context available."}


def advocate_round1_node(state: DebateState) -> dict:
    """Advocate's initial arguments."""
    advocate = AdvocateAgent()
    response = advocate.analyze(state["query"], state.get("research_context", ""))
    return {
        "advocate_round1": response,
        "debate_log": state.get("debate_log", []) + [
            {"agent": "Advocate", "action": "round1", "summary": response[:200]}
        ],
    }


def critic_node(state: DebateState) -> dict:
    """Critic challenges the Advocate."""
    critic = CriticAgent()
    response = critic.analyze(
        state["query"], state.get("research_context", ""), state["advocate_round1"]
    )
    return {
        "critic_response": response,
        "debate_log": state.get("debate_log", []) + [
            {"agent": "Critic", "action": "challenge", "summary": response[:200]}
        ],
    }


def advocate_round2_node(state: DebateState) -> dict:
    """Advocate rebuts the Critic."""
    advocate = AdvocateAgent()
    response = advocate.analyze(
        state["query"], state.get("research_context", ""), state["critic_response"]
    )
    return {
        "advocate_round2": response,
        "debate_log": state.get("debate_log", []) + [
            {"agent": "Advocate", "action": "rebuttal", "summary": response[:200]}
        ],
    }


def mediator_node(state: DebateState) -> dict:
    """Mediator synthesizes the debate."""
    mediator = MediatorAgent()
    brief = mediator.synthesize(
        state["query"],
        state["advocate_round1"],
        state["critic_response"],
        state["advocate_round2"],
    )
    return {
        "mediator_brief": brief,
        "debate_log": state.get("debate_log", []) + [
            {"agent": "Mediator", "action": "synthesis", "summary": brief[:200]}
        ],
    }


def build_debate_graph() -> StateGraph:
    """Build the LangGraph debate workflow."""
    graph = StateGraph(DebateState)

    graph.add_node("research", research_node)
    graph.add_node("advocate_round1", advocate_round1_node)
    graph.add_node("critic", critic_node)
    graph.add_node("advocate_round2", advocate_round2_node)
    graph.add_node("mediator", mediator_node)

    graph.set_entry_point("research")
    graph.add_edge("research", "advocate_round1")
    graph.add_edge("advocate_round1", "critic")
    graph.add_edge("critic", "advocate_round2")
    graph.add_edge("advocate_round2", "mediator")
    graph.add_edge("mediator", END)

    return graph.compile()


def run_debate(query: str) -> dict:
    """Run the full multi-agent debate."""
    app = build_debate_graph()
    initial_state = {
        "query": query,
        "research_context": "",
        "research_sources": [],
        "advocate_round1": "",
        "critic_response": "",
        "advocate_round2": "",
        "mediator_brief": "",
        "debate_log": [],
        "error": "",
    }
    result = app.invoke(initial_state)
    return {
        "query": query,
        "research_sources": result.get("research_sources", []),
        "advocate_round1": result.get("advocate_round1", ""),
        "critic_response": result.get("critic_response", ""),
        "advocate_round2": result.get("advocate_round2", ""),
        "strategic_brief": result.get("mediator_brief", ""),
        "debate_log": result.get("debate_log", []),
    }
