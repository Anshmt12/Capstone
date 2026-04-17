"""Mediator Agent - synthesizes the debate into a strategic brief."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.agents.llm_provider import get_llm

MEDIATOR_PROMPT = ChatPromptTemplate.from_template("""You are a senior Indian legal strategist serving as mediator.
You have observed a debate between an Advocate (strengths) and Critic (weaknesses).
Synthesize their arguments into a balanced strategic brief.

Case Details:
{case_details}

=== ADVOCATE'S ARGUMENTS (Round 1) ===
{advocate_round1}

=== CRITIC'S ARGUMENTS ===
{critic_response}

=== ADVOCATE'S REBUTTAL (Round 2) ===
{advocate_round2}

Instructions - produce a strategic brief with these sections:

1. CASE SUMMARY: Brief overview
2. KEY STRENGTHS: Top 3-5 strongest arguments (from Advocate)
3. KEY WEAKNESSES: Top 3-5 most critical risks (from Critic)
4. RISK SCORE: Rate overall case risk from 1 (very low) to 10 (very high), with justification
5. RECOMMENDED APPROACH: Specific strategic recommendations
6. PRIORITY ACTIONS: Immediate next steps ordered by urgency
7. SETTLEMENT CONSIDERATION: Whether to litigate or settle, with reasoning

Be specific, cite Indian law, and be actionable.

Strategic Brief:""")


class MediatorAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.3)
        self.chain = MEDIATOR_PROMPT | self.llm | StrOutputParser()

    def synthesize(
        self,
        case_details: str,
        advocate_round1: str,
        critic_response: str,
        advocate_round2: str,
    ) -> str:
        return self.chain.invoke({
            "case_details": case_details,
            "advocate_round1": advocate_round1,
            "critic_response": critic_response,
            "advocate_round2": advocate_round2,
        })
