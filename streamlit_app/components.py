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
- Cross-Agent Handovers
- Workflow Orchestration
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

        st.divider()

        st.subheader(
            "Workflow Features"
        )

        st.markdown(
            """
- Multi-Intent Detection
- Sequential Agent Routing
- Contextual Handovers
- Workflow Aggregation
- Persistent Conversations
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


# ---------------------------------------------------
# Workflow Renderer
# ---------------------------------------------------

def render_workflow(
    completed_agents,
):

    if completed_agents:

        st.markdown(
            "### Workflow Execution"
        )

        workflow_display = (
            " → ".join(
                [
                    (
                        agent
                        .replace(
                            "_agent",
                            ""
                        )
                        .replace(
                            "_",
                            " "
                        )
                        .title()
                    )
                    for agent in (
                        completed_agents
                    )
                ]
            )
        )

        st.info(
            workflow_display
        )


# ---------------------------------------------------
# Handover Renderer
# ---------------------------------------------------

def render_handover_count(
    handover_count,
):

    st.caption(
        (
            f"🔄 Handover Events: "
            f"{handover_count}"
        )
    )


# ---------------------------------------------------
# Agent Badge Renderer
# ---------------------------------------------------

def render_agent_badge(
    active_agent,
):

    agent_mapping = {

        "technical_agent":
            "🛠 Technical Agent",

        "billing_agent":
            "💳 Billing Agent",

        "escalation_agent":
            "🚨 Escalation Agent",

        "triage_agent":
            "🧠 Triage Agent",
    }

    badge = agent_mapping.get(
        active_agent,
        active_agent,
    )

    st.success(
        f"Active Agent: {badge}"
    )