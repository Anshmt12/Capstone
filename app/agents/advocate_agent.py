"""Advocate Agent - finds all strengths and favorable arguments."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.agents.llm_provider import get_llm

ADVOCATE_PROMPT = ChatPromptTemplate.from_template("""You are a senior Indian litigation advocate.
Your role is to find ALL strengths and favorable arguments in the case.
Be thorough, persuasive, and cite relevant Indian legal provisions.

Legal Research Context:
{research_context}

Case Details:
{case_details}

{critic_response}

Instructions:
- Identify every strong legal argument available
- Cite specific Articles of the Constitution, IPC sections, or relevant Indian statutes
- Reference favorable Indian Supreme Court / High Court precedents from the context
- Highlight procedural advantages
- Assess strength of evidence
- If responding to the Critic, rebut their weaknesses with counter-arguments

Provide your analysis as the Advocate:""")


class AdvocateAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.4)
        self.chain = ADVOCATE_PROMPT | self.llm | StrOutputParser()

    def analyze(self, case_details: str, research_context: str, critic_response: str = "") -> str:
        critic_section = ""
        if critic_response:
            critic_section = f"\nCritic's Weaknesses to Rebut:\n{critic_response}"
        return self.chain.invoke({
            "case_details": case_details,
            "research_context": research_context,
            "critic_response": critic_section,
        })
