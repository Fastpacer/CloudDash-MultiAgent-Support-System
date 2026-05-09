from langchain_core.prompts import ChatPromptTemplate

from app.utils.llm_factory import get_llm
from app.observability.logger import logger


llm = get_llm()


rewrite_prompt = ChatPromptTemplate.from_template(
    """
You are a query rewriting assistant for a cloud support platform.

Your task is to rewrite vague or conversational user queries into
clear retrieval-optimized support queries.

Guidelines:
- Preserve original meaning
- Expand ambiguous references
- Include technical context if implied
- Keep query concise
- Do not hallucinate information

User Query:
{query}

Rewritten Query:
"""
)


def rewrite_query(
    query: str,
):

    logger.info(
        "query_rewriting_started",
        original_query=query,
    )

    chain = rewrite_prompt | llm

    response = chain.invoke(
        {
            "query": query
        }
    )

    rewritten_query = response.content.strip()

    logger.info(
        "query_rewriting_completed",
        rewritten_query=rewritten_query,
    )

    return rewritten_query