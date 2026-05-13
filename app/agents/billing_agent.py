from langchain_core.prompts import (
    ChatPromptTemplate,
)

from app.agents.base_agent import (
    BaseAgent,
)

from app.orchestration.state import (
    ConversationState,
    AgentOutput,
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


class BillingAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            agent_name="billing_agent"
        )

        self.llm = get_llm()

        # ---------------------------------------------------
        # Billing-Only Scoped Prompt
        # ---------------------------------------------------

        self.prompt = (
            ChatPromptTemplate.from_template(
                """
You are CloudDash Enterprise Billing Support.

You ONLY handle:
- subscriptions
- pricing
- invoices
- refunds
- payments
- account upgrades
- enterprise plans
- billing operations
- licensing limits

IMPORTANT:
Ignore ALL technical troubleshooting topics including:
- SSO failures
- dashboard latency
- API errors
- sync failures
- infrastructure issues
- cloud integrations
- operational diagnostics

If the user asks BOTH technical and billing questions:
ONLY answer the billing-related portions.

STRICT RULES:
- Use ONLY the provided KB context
- Never invent billing policies
- Never speculate about charges
- Never discuss technical troubleshooting
- Never diagnose infrastructure problems
- Keep responses concise and professional
- If KB lacks information, explicitly state that verified billing information was unavailable

RESPONSE FORMAT:

Billing Summary:
- concise billing-related diagnosis

Billing Impact:
- pricing, plan, or subscription implications

Billing Resolution Steps:
1. Step one
2. Step two
3. Step three

Billing Verification:
- expected billing confirmation behavior

Context:
{context}

User Question:
{question}
"""
            )
        )

    def process(
        self,
        state: ConversationState,
    ) -> ConversationState:

        # ---------------------------------------------------
        # User Query
        # ---------------------------------------------------

        query = (
                   self.agent_name,
                   state.messages[-1].content,
        )

        logger.info(
            "billing_agent_started",
            trace_id=(
                state.trace_id
            ),
        )

        # ---------------------------------------------------
        # Hybrid Retrieval
        # ---------------------------------------------------

        retrieved_docs = (
            retrieve_documents(
                query=query,
                top_k=4,
            )
        )

        # ---------------------------------------------------
        # Citation Extraction
        # ---------------------------------------------------

        citations = list(
            {
                doc["metadata"][
                    "filename"
                ]
                for doc in (
                    retrieved_docs
                )
            }
        )

        # ---------------------------------------------------
        # Shared Retrieval Tracking
        # ---------------------------------------------------

        for citation in citations:

            if (
                citation
                not in state.retrieved_docs
            ):

                state.retrieved_docs.append(
                    citation
                )

        # ---------------------------------------------------
        # Context Compression
        # ---------------------------------------------------

        context = "\n\n".join(
            [
                doc["content"][:1200]
                for doc in (
                    retrieved_docs
                )
            ]
        )

        # ---------------------------------------------------
        # LLM Generation
        # ---------------------------------------------------

        chain = (
            self.prompt
            | self.llm
        )

        response = chain.invoke(
            {
                "context": context,
                "question": query,
            }
        )

        generated_response = (
            response.content.strip()
        )

        # ---------------------------------------------------
        # Structured Agent Output
        # ---------------------------------------------------

        state.agent_outputs.append(
            AgentOutput(
                agent_name=(
                    self.agent_name
                ),
                response=(
                    generated_response
                ),
                citations=citations,
            )
        )

        logger.info(
            "billing_agent_completed",
            retrieved_documents=len(
                retrieved_docs
            ),
            citations=len(
                citations
            ),
            trace_id=(
                state.trace_id
            ),
        )

        return state