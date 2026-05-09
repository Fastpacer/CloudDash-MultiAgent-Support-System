import streamlit as st


# ---------------------------------------------------
# Application Header
# ---------------------------------------------------

def render_header():

    st.title(
        "☁️ CloudDash Multi-Agent Support"
    )

    st.caption(
        (
            "Enterprise AI Support System "
            "with Hybrid RAG, Guardrails, "
            "Memory, and Multi-Agent Routing"
        )
    )

    st.divider()


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

def render_sidebar():

    with st.sidebar:

        st.header(
            "System Overview"
        )

        st.markdown(
            """
### Active Capabilities
- Multi-Agent Orchestration
- Hybrid Retrieval
- BM25 + Dense Search
- Cross-Encoder Reranking
- Guardrails
- Conversation Memory
- Observability
"""
        )

        st.divider()

        st.subheader(
            "Supported Domains"
        )

        st.markdown(
            """
- AWS Monitoring
- Billing Support
- SSO Troubleshooting
- API Rate Limits
- Cloud Integrations
- Escalation Handling
"""
        )


# ---------------------------------------------------
# Escalation Banner
# ---------------------------------------------------

def render_escalation_banner():

    st.error(
        (
            "⚠️ Escalation Required: "
            "This request may require "
            "human support intervention."
        )
    )


# ---------------------------------------------------
# Citation Renderer
# ---------------------------------------------------

def render_citations(
    citations,
):

    if citations:

        with st.expander(
            "Sources"
        ):

            for citation in citations:

                st.markdown(
                    f"- {citation}"
                )


# ---------------------------------------------------
# Trace Information
# ---------------------------------------------------

def render_trace_id(
    trace_id: str,
):

    st.caption(
        f"Trace ID: {trace_id}"
    )