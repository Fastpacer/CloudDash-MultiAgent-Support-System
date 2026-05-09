from langchain_groq import ChatGroq

from app.utils.config_loader import settings


def get_llm(
    temperature: float = 0.2,
):

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        groq_api_key=settings.GROQ_API_KEY,
    )