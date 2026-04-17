"""LLM provider abstraction - supports OpenRouter, Groq, HuggingFace (all free)."""
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from app.config import settings


def get_llm(temperature: float = 0.3):
    """Get LLM based on configured provider."""
    provider = settings.LLM_PROVIDER.lower()

    if provider == "openrouter":
        return ChatOpenAI(
            model=settings.OPENROUTER_MODEL,
            openai_api_key=settings.OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=temperature,
            max_tokens=2048,
        )
    elif provider == "groq":
        return ChatGroq(
            model=settings.GROQ_MODEL,
            groq_api_key=settings.GROQ_API_KEY,
            temperature=temperature,
            max_tokens=2048,
        )
    elif provider == "huggingface":
        from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
        endpoint = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
            huggingfacehub_api_token=settings.HF_API_KEY,
            temperature=temperature,
            max_new_tokens=2048,
        )
        return ChatHuggingFace(llm=endpoint)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
