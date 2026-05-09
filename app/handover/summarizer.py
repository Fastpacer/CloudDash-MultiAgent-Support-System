from langchain_core.prompts import (
    ChatPromptTemplate,
)

from app.utils.llm_factory import get_llm


llm = get_llm()


summary_prompt = ChatPromptTemplate.from_template(
    """
Summarize the support conversation for agent handover.

Focus on:
- customer issue
- actions already attempted
- unresolved problems
- urgency level

Conversation:
{conversation}
"""
)


def summarize_conversation(
    conversation_text: str,
):

    chain = summary_prompt | llm

    response = chain.invoke(
        {
            "conversation": conversation_text
        }
    )

    return response.content.strip()