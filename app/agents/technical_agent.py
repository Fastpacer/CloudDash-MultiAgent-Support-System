from langchain_core.prompts import ChatPromptTemplate

from app.agents.base_agent import BaseAgent

from app.orchestration.state import (
    ConversationState,
    ConversationMessage,
)

from app.guardrails.output_guard import (
    validate_output,
)

from app.guardrails.hallucination_checker import (
    detect_possible_hallucination,
)

from app.retrieval.retriever import (
    retrieve_documents,
)

from app.utils.llm_factory import (
    get_llm,
)

from app.observability.logger import (
    logger,
)


class TechnicalAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            agent_name="technical_agent"
        )

        self.llm = get_llm()

        self.prompt = ChatPromptTemplate.from_template(
            """
You are CloudDash Enterprise Technical Support.

Your responsibilities:
- diagnose cloud platform issues
- provide operational troubleshooting
- use ONLY verified KB information
- avoid hallucinations
- remain concise and technical

STRICT RULES:
- Use ONLY the provided KB context
- Never invent infrastructure details
- Never speculate
- Never say "I think", "maybe", or "possibly"
- Do not ask unnecessary follow-up questions
- Keep responses under 180 words unless necessary
- If KB lacks information, explicitly state that verified information was unavailable

RESPONSE FORMAT:

Issue Summary:
- concise diagnosis

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

        # ---------------------------------------------------
        # User Query
        # ---------------------------------------------------

        query = (
            state.messages[-1].content
        )

        logger.info(
            "technical_agent_started",
            trace_id=state.trace_id,
        )

        # ---------------------------------------------------
        # Hybrid Retrieval Pipeline
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
        # Output Guardrails
        # ---------------------------------------------------

        is_safe, reason = validate_output(
            response=response.content,
            citations=citations,
        )

        possible_hallucination = (
            detect_possible_hallucination(
                response=response.content,
                citations=citations,
            )
        )

        # ---------------------------------------------------
        # Guardrail Fallback
        # ---------------------------------------------------

        if (
            not is_safe
            or possible_hallucination
        ):

            logger.warning(
                "output_guardrail_triggered",
                reason=reason,
                hallucination=(
                    possible_hallucination
                ),
            )

            safe_response = (
                "Unable to provide a fully "
                "verified response from the "
                "current knowledge base."
            )

            response.content = safe_response

        # ---------------------------------------------------
        # Append Citations
        # ---------------------------------------------------

        citation_text = "\n\nSources:\n"

        for citation in citations:

            citation_text += (
                f"- {citation}\n"
            )

        final_response = (
            response.content.strip()
            + citation_text
        )

        # ---------------------------------------------------
        # Store Assistant Message
        # ---------------------------------------------------

        state.messages.append(
            ConversationMessage(
                role="assistant",
                content=final_response,
            )
        )

        logger.info(
            "technical_agent_completed",
            retrieved_documents=len(
                retrieved_docs
            ),
            citations=len(citations),
        )

        return state