from langchain_core.prompts import ChatPromptTemplate

from app.agents.base_agent import BaseAgent

from app.orchestration.state import (
    ConversationState,
    ConversationMessage,
)

from app.retrieval.retriever import retrieve_documents

from app.utils.llm_factory import get_llm
from app.observability.logger import logger


class BillingAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            agent_name="billing_agent"
        )

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_template(
            """
You are CloudDash Enterprise Billing Support.

Your responsibilities:
- resolve subscription issues
- explain invoices and refunds
- provide operational billing guidance
- use ONLY verified KB information

STRICT RULES:
- Use ONLY the provided KB context
- Never invent billing policies
- Never speculate about charges
- Keep responses concise and professional
- If KB lacks information, explicitly state that verified billing information was unavailable

RESPONSE FORMAT:

Issue Summary:
- concise billing diagnosis

Likely Cause:
- root cause explanation

Resolution Steps:
1. Step one
2. Step two
3. Step three

Verification:
- expected confirmation behavior

Context:
{context}

User Question:
{question}
"""
        )

    def process(
        self,
        state: ConversationState,
    ) -> ConversationState:

        query = state.messages[-1].content

        logger.info(
            "billing_agent_started",
            trace_id=state.trace_id,
        )

        # ---------------------------------------------------
        # Hybrid Retrieval
        # ---------------------------------------------------

        retrieved_docs = retrieve_documents(
            query=query,
            top_k=4,
        )

        # ---------------------------------------------------
        # Citation Extraction
        # ---------------------------------------------------

        citations = list(
            {
                doc["metadata"]["filename"]
                for doc in retrieved_docs
            }
        )

        state.retrieved_docs = citations

        # ---------------------------------------------------
        # Context Compression
        # ---------------------------------------------------

        context = "\n\n".join(
            [
                doc["content"][:1200]
                for doc in retrieved_docs
            ]
        )

        # ---------------------------------------------------
        # LLM Generation
        # ---------------------------------------------------

        chain = self.prompt | self.llm

        response = chain.invoke(
            {
                "context": context,
                "question": query,
            }
        )

        # ---------------------------------------------------
        # Append Citations To Response
        # ---------------------------------------------------

        citation_text = "\n\nSources:\n"

        for citation in citations:

            citation_text += f"- {citation}\n"

        final_response = (
            response.content.strip()
            + citation_text
        )

        # ---------------------------------------------------
        # Append Assistant Response
        # ---------------------------------------------------

        state.messages.append(
            ConversationMessage(
                role="assistant",
                content=final_response,
            )
        )

        logger.info(
            "billing_agent_completed",
            retrieved_documents=len(retrieved_docs),
            citations=len(citations),
        )

        return state