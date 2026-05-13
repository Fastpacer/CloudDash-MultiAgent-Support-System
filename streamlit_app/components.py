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
            "with Multi-Agent Orchestration, "
            "Hybrid Retrieval, Guardrails, "
            "Persistent Memory, and Workflow Visibility"
        )
    )

    st.divider()


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

def render_sidebar():

    with st.sidebar:

        st.header(
            "System Architecture"
        )

        st.markdown(
            """
### Core Capabilities
- Multi-Agent Orchestration
- Hybrid Retrieval Pipeline
- BM25 + Dense Search
- Contextual Handovers
- Workflow Aggregation
- Guardrails
- Persistent Conversations
- Observability + Tracing
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
- Escalation Management
"""
        )

        st.divider()

        st.subheader(
            "Workflow Engine"
        )

        st.markdown(
            """
- Multi-Intent Detection
- Sequential Agent Execution
- Shared Workflow State
- Context Preservation
- Workflow Synthesis
"""
        )

        st.divider()

        st.caption(
            (
                "Built with LangGraph, "
                "Hybrid RAG, and "
                "Multi-Agent Routing"
            )
        )


# ---------------------------------------------------
# Escalation Banner
# ---------------------------------------------------

def render_escalation_banner():

    st.error(
        (
            "⚠️ Escalation Required\n\n"
            "This request may require "
            "human support intervention."
        )
    )


# ---------------------------------------------------
# Workflow Renderer
# ---------------------------------------------------

def render_workflow(
    completed_agents,
):

    if not completed_agents:

        return

    formatted_agents = []

    for agent in completed_agents:

        cleaned_agent = (
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

        formatted_agents.append(
            cleaned_agent
        )

    workflow_display = (
        " → ".join(
            formatted_agents
        )
    )

    with st.expander(
        "Workflow Execution",
        expanded=False,
    ):

        st.info(
            workflow_display
        )


# ---------------------------------------------------
# Agents Invoked Renderer
# ---------------------------------------------------

def render_agents_used(
    completed_agents,
):

    if not completed_agents:

        return

    with st.expander(
        "Agents Invoked",
        expanded=False,
    ):

        for agent in completed_agents:

            cleaned_agent = (
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

            st.markdown(
                f"- {cleaned_agent}"
            )


# ---------------------------------------------------
# Citation Renderer
# ---------------------------------------------------

def render_citations(
    citations,
):

    if not citations:

        return

    unique_citations = sorted(
        list(set(citations))
    )

    with st.expander(
        "Sources",
        expanded=False,
    ):

        for citation in (
            unique_citations
        ):

            st.markdown(
                f"- {citation}"
            )


# ---------------------------------------------------
# Trace Information
# ---------------------------------------------------

def render_trace_id(
    trace_id: str,
):

    if not trace_id:

        return

    st.caption(
        f"Trace ID: {trace_id}"
    )


# ---------------------------------------------------
# Handover Renderer
# ---------------------------------------------------

def render_handover_count(
    handover_count,
):

    if (
        handover_count
        is None
    ):

        return

    st.caption(
        (
            f"🔄 Workflow Handovers: "
            f"{handover_count}"
        )
    )


# ---------------------------------------------------
# Agent Badge Renderer
# ---------------------------------------------------

def render_agent_badge(
    active_agent,
):

    if not active_agent:

        return

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

    badge = (
        agent_mapping.get(
            active_agent,
            active_agent,
        )
    )

    st.success(
        f"Primary Agent: {badge}"
    )


# ---------------------------------------------------
# Workflow Metrics Renderer
# ---------------------------------------------------

def render_workflow_metrics(
    total_agents,
    total_handovers,
):

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Agents Invoked",
            total_agents,
        )

    with col2:

        st.metric(
            "Handovers",
            total_handovers,
        )


# ---------------------------------------------------
# Divider Renderer
# ---------------------------------------------------

def render_response_divider():

    st.divider()