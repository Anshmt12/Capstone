"""Critic Agent - finds all weaknesses and risks (devil's advocate)."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.agents.llm_provider import get_llm

CRITIC_PROMPT = ChatPromptTemplate.from_template("""You are a seasoned Indian legal risk analyst and devil's advocate.
Your role is to find ALL weaknesses, risks, and potential pitfalls in the case.
Be brutally honest - the client's interests are best served by knowing the risks.

Legal Research Context:
{research_context}

Case Details:
{case_details}

Advocate's Arguments:
{advocate_response}

Instructions:
- Identify every legal weakness and vulnerability
- Point out unfavorable Indian precedents or statutory provisions
- Highlight evidentiary gaps
- Assess opposing counsel's likely counter-arguments
- Identify procedural risks and timeline concerns
- Rate each weakness as Minor, Moderate, or Critical
- Challenge the Advocate's strongest arguments specifically

Provide your analysis as the Critic:""")


class CriticAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.4)
        self.chain = CRITIC_PROMPT | self.llm | StrOutputParser()

    def analyze(self, case_details: str, research_context: str, advocate_response: str) -> str:
        return self.chain.invoke({
            "case_details": case_details,
            "research_context": research_context,
            "advocate_response": advocate_response,
        })
