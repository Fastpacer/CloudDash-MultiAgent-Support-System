# CloudDash Multi-Agent Support System

A production-ready multi-agent customer support system for CloudDash, a B2B SaaS cloud infrastructure monitoring platform. The system intelligently routes customer queries to specialized agents, retrieves relevant knowledge base articles, and seamlessly hands over context between agents when conversations cross domain boundaries.

## Overview

This system demonstrates advanced AI/ML engineering patterns including:
- **Multi-agent orchestration** using LangGraph state machines
- **Retrieval-Augmented Generation (RAG)** with hybrid search capabilities
- **Intelligent agent handover** with full context preservation
- **Production-grade observability** with structured JSON logging
- **Safety guardrails** for input validation and output quality checks
- **Extensible architecture** for adding new agents without modifying core logic

## Features

### ✨ Core Capabilities

- **Intent Classification**: Automatically routes customer queries to appropriate specialists
- **Knowledge Base Retrieval**: Grounds responses in verified documentation with citation tracking
- **Agent Specialization**: Four specialized agents (Triage, Technical, Billing, Escalation) handling distinct domains
- **Seamless Handover**: Transfers context, entities, and conversation history between agents
- **Graceful Escalation**: Routes complex issues to human operators with structured context
- **Hybrid Search**: Combines dense (vector) and sparse (BM25) retrieval for comprehensive results
- **Re-ranking**: Prioritizes most relevant documents using contextual re-ranking

### 🛡️ Safety & Quality

- **Input Guardrails**: Detects and blocks prompt injection attempts
- **Output Guardrails**: Ensures responses cite sources and avoid fabrication
- **Structured State**: Typed Pydantic models for conversation state, preventing data corruption
- **Error Handling**: Comprehensive error recovery with fallback strategies
- **Audit Logging**: Full trace of every handover with timestamp, source, target, and reason

### 📊 Observability

- **Structured Logging**: JSON-formatted logs with trace IDs connecting all events for a session
- **Metrics Tracking**: Counters and gauges for agent invocations, retrieval operations, handovers
- **Distributed Tracing**: Each conversation has a unique trace ID propagated through the system
- **Integration-Ready**: Compatible with Langfuse, LangSmith, and Arize Phoenix

### 🔧 Interfaces

- **REST API**: Full-featured FastAPI endpoints for programmatic integration
- **Streamlit UI**: Interactive web interface for visual demonstration and testing
- **Extensible**: Easy to add CLI, webhook, or other custom interfaces

## Quick Start

### Prerequisites

- Python 3.10+
- pip or poetry
- (Optional) API keys for LLM providers (Groq, OpenAI, etc.)

### Installation

1. **Clone and navigate to the project**:
```bash
cd Clouddash_MultiAgent_Support_System
```

2. **Create and activate a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration (LLM API keys, settings, etc.)
```

5. **Initialize the knowledge base**:
```bash
python -m app.retrieval.ingest
```

### Running the System

#### Option 1: REST API (Recommended)
```bash
uvicorn app.main:app --reload --port 8000
```

Access the API:
- **Root**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

#### Option 2: Streamlit UI
```bash
streamlit run streamlit_app/app.py
```

Access the UI: http://localhost:8501

## API Documentation

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### 2. Start Conversation
```http
POST /conversation/start
```

**Response**:
```json
{
  "conversation_id": "conv-123e4567-e89b-12d3-a456-426614174000",
  "trace_id": "trace-987f6543-e21a-98d7-b654-321987654321",
  "message": "Conversation initialized. How can I help you today?"
}
```

#### 3. Send Message
```http
POST /conversation/message
```

**Request Body**:
```json
{
  "conversation_id": "conv-123e4567-e89b-12d3-a456-426614174000",
  "user_message": "My alerts stopped firing after updating AWS credentials"
}
```

**Response**:
```json
{
  "conversation_id": "conv-123e4567-e89b-12d3-a456-426614174000",
  "agent": "technical_agent",
  "response": "Let me help you troubleshoot your AWS integration issue...",
  "citations": [
    {
      "content": "To fix AWS integration issues...",
      "source": "knowledge_base/troubleshooting/aws_alerts_not_firing.md"
    }
  ],
  "retrieved_docs": ["aws_alerts_not_firing.md", "alert_configuration.md"],
  "escalation_required": false
}
```

#### 4. Get Conversation History
```http
GET /conversation/{conversation_id}
```

**Response**:
```json
{
  "conversation_id": "conv-123e4567-e89b-12d3-a456-426614174000",
  "trace_id": "trace-987f6543-e21a-98d7-b654-321987654321",
  "messages": [
    {
      "role": "user",
      "content": "My alerts stopped firing after updating AWS credentials",
      "timestamp": "2026-04-15T10:30:00Z"
    },
    {
      "role": "assistant",
      "content": "Let me help you troubleshoot...",
      "timestamp": "2026-04-15T10:30:05Z"
    }
  ]
}
```

## Knowledge Base Structure

The system ingests Markdown documents organized by category:

```
knowledge_base/
├── faqs/
│   ├── reset_api_key.md
│   ├── supported_cloud_providers.md
│   └── ...
├── troubleshooting/
│   ├── aws_alerts_not_firing.md
│   ├── dashboard_loading_slowly.md
│   └── ...
├── billing/
│   ├── invoice_explanation.md
│   ├── refund_policy.md
│   └── ...
├── api_docs/
│   ├── authentication.md
│   ├── rate_limits.md
│   └── ...
└── account_access/
    ├── sso_setup.md
    ├── rbac_roles.md
    └── ...
```

### Document Format

Each KB article should be a Markdown file with YAML frontmatter:

```markdown
---
title: How to Configure Alert Thresholds
category: troubleshooting
tags: [alerts, configuration, thresholds]
applies_to: [Pro, Enterprise]
last_updated: 2026-04-15
---

## Step 1: Navigate to Alerts

...detailed content...
```

## Configuration

### Agent Configuration (`app/config/agents.yaml`)

Define agent capabilities, system prompts, and tools:

```yaml
triage_agent:
  name: "Triage Agent"
  description: "First point of contact for query classification"
  tools:
    - intent_classifier
    - entity_extractor

technical_agent:
  name: "Technical Support Agent"
  description: "Handles technical issues and troubleshooting"
  tools:
    - kb_retriever
    - code_generator

billing_agent:
  name: "Billing Agent"
  description: "Handles billing and subscription inquiries"
  tools:
    - account_lookup
    - plan_comparison

escalation_agent:
  name: "Escalation Agent"
  description: "Routes to human support with context"
  tools:
    - context_summarizer
    - priority_classifier
```

### Routing Configuration (`app/config/routing.yaml`)

Define intent-to-agent routing rules:

```yaml
routing_rules:
  technical:
    intents:
      - alerts
      - integrations
      - api
      - dashboard
      - sync_failures
    target_agent: technical_agent

  billing:
    intents:
      - invoices
      - refunds
      - subscriptions
      - payments
    target_agent: billing_agent

  escalation:
    intents:
      - legal
      - production_outage
      - high_priority
    target_agent: escalation_agent
```

### Application Settings (`app/config/settings.yaml`)

```yaml
app:
  name: "CloudDash AI Support"
  version: "1.0.0"
  debug: false

llm:
  provider: "groq"  # or openai, anthropic, etc.
  model: "mixtral-8x7b-32768"
  temperature: 0.7
  max_tokens: 1024

retrieval:
  vector_store: "chroma"
  chunk_size: 500
  chunk_overlap: 100
  top_k: 4
  rerank: true
  hybrid_search: true

logging:
  level: "INFO"
  format: "json"
  trace_enabled: true

guardrails:
  input_validation: true
  output_validation: true
  pii_redaction: false
```

## Testing

### Run Unit Tests
```bash
pytest tests/unit/ -v
```

### Run Integration Tests
```bash
pytest tests/integration/ -v
```

### Run Specific Test
```bash
pytest tests/unit/test_agents.py::test_triage_routing -v
```

## Test Scenarios

The system is designed to handle the following scenarios:

### Scenario 1: Single-Agent Resolution
**Input**: "My CloudDash alerts stopped firing after I updated my AWS integration credentials yesterday. I'm on the Pro plan."

**Expected Flow**: 
- Triage → Technical Support → KB retrieval → Step-by-step resolution with citations

### Scenario 2: Cross-Agent Handover
**Input**: "I want to upgrade from Pro to Enterprise, but first can you check if the SSO integration issue I reported last week has been resolved?"

**Expected Flow**: 
- Triage → Technical Support (SSO issue) → Handover to Billing (upgrade) → Full context preserved

### Scenario 3: Escalation to Human
**Input**: "I've been charged twice for April. I need an immediate refund and I want to speak to a manager."

**Expected Flow**: 
- Triage → Billing → Escalation Agent → Human handover with structured context

### Scenario 4: KB Retrieval Failure
**Input**: "Does CloudDash support integration with Datadog for cross-platform alerting?"

**Expected Flow**: 
- Agent searches KB → No relevant article found → Transparently acknowledges limitation → Offers escalation

## Project Structure

```
.
├── README.md                    # This file
├── ARCHITECTURE.md              # Detailed architecture documentation
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
│
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── agents/                  # Agent implementations
│   │   ├── base_agent.py        # Abstract base class
│   │   ├── triage_agent.py      # Intent classification & routing
│   │   ├── technical_agent.py   # Technical issue resolution
│   │   ├── billing_agent.py     # Billing & subscription handling
│   │   └── escalation_agent.py  # Human handover
│   ├── api/                     # REST API layer
│   │   ├── routes.py            # Endpoint definitions
│   │   └── schemas.py           # Pydantic request/response models
│   ├── config/                  # Configuration files
│   │   ├── agents.yaml          # Agent definitions
│   │   ├── routing.yaml         # Intent-to-agent routing
│   │   └── settings.yaml        # Application settings
│   ├── orchestration/           # Agent orchestration
│   │   ├── graph.py             # LangGraph state machine
│   │   ├── state.py             # Conversation state model
│   │   ├── router.py            # Intent-based routing logic
│   │   └── transitions.py       # State transitions
│   ├── retrieval/               # RAG pipeline
│   │   ├── ingest.py            # KB document loading & chunking
│   │   ├── vector_store.py      # Chroma vector store setup
│   │   ├── retriever.py         # Dense & sparse retrieval
│   │   ├── hybrid_search.py     # BM25 keyword search
│   │   ├── reranker.py          # Re-ranking logic
│   │   └── query_rewriter.py    # Query expansion & rewriting
│   ├── handover/                # Agent handover protocol
│   │   ├── protocol.py          # Handover payload definition
│   │   ├── context_builder.py   # Context summarization
│   │   ├── audit_logger.py      # Handover event logging
│   │   └── summarizer.py        # Conversation summarization
│   ├── memory/                  # Conversation memory
│   │   ├── conversation_store.py # In-memory conversation storage
│   │   └── session_manager.py   # Session lifecycle management
│   ├── guardrails/              # Safety & quality checks
│   │   ├── input_guard.py       # Prompt injection detection
│   │   ├── output_guard.py      # Response validation & citation check
│   │   └── hallucination_checker.py # Fact-checking against KB
│   ├── observability/           # Logging, metrics, tracing
│   │   ├── logger.py            # Structured JSON logging setup
│   │   ├── metrics.py           # Metrics collection
│   │   └── tracing.py           # Distributed tracing
│   └── utils/
│       ├── config_loader.py     # Configuration loading
│       ├── llm_factory.py       # LLM provider initialization
│       ├── exceptions.py        # Custom exceptions
│       └── helpers.py           # Utility functions
│
├── streamlit_app/               # Streamlit web UI
│   ├── app.py                   # Main Streamlit app
│   ├── chat_ui.py               # Chat interface components
│   ├── components.py            # Reusable UI components
│   ├── session_manager.py       # Streamlit session management
│   └── config.toml              # Streamlit configuration
│
├── knowledge_base/              # KB documents (ingested into vector store)
│   ├── faqs/
│   ├── troubleshooting/
│   ├── billing/
│   ├── api_docs/
│   └── account_access/
│
├── chroma_db/                   # Persisted Chroma vector store
│
├── logs/                        # Application logs directory
│
├── tests/
│   ├── unit/                    # Unit tests
│   │   ├── test_agents.py
│   │   ├── test_handover.py
│   │   └── test_rag.py
│   └── integration/             # Integration tests
│       └── test_api.py
```

## Architecture Highlights

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

### Key Design Decisions

1. **LangGraph for Orchestration**: Provides declarative state machine for agent routing and transitions
2. **Hybrid Retrieval**: Combines vector embeddings (semantic) with BM25 (keyword) for comprehensive search
3. **Structured State**: Pydantic models enforce type safety across agent boundaries
4. **In-Memory Conversation Store**: Fast development-grade storage (upgrade to persistent DB for production)
5. **Configuration-Driven Agents**: YAML-based routing and agent definitions for extensibility
6. **Structured JSON Logging**: Integration-ready for observability platforms

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
# LLM Configuration
LLM_PROVIDER=groq
LLM_API_KEY=your_groq_api_key_here
LLM_MODEL=mixtral-8x7b-32768

# Application Settings
APP_NAME=CloudDash AI Support
APP_VERSION=1.0.0
DEBUG=false

# Vector Store
VECTOR_STORE_PATH=./chroma_db

# Observability
LOG_LEVEL=INFO
TRACE_ENABLED=true

# Optional: LLM Observability
# LANGFUSE_PUBLIC_KEY=your_key
# LANGFUSE_SECRET_KEY=your_secret
# LANGSMITH_API_KEY=your_key
```

## Deployment

### Development
```bash
uvicorn app.main:app --reload --port 8000
```

### Production
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --port 8000
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

To add a new agent type:

1. Create a new agent class inheriting from `BaseAgent` in `app/agents/`
2. Implement the `process()` method with your agent logic
3. Add the agent to `app/orchestration/graph.py`
4. Update `app/config/agents.yaml` with agent definition
5. Update `app/config/routing.yaml` with routing rules

The core orchestration logic remains unchanged—no need to modify existing code.

## Troubleshooting

### KB Documents Not Found
- Ensure knowledge base files are in `knowledge_base/` directory as Markdown files
- Run `python -m app.retrieval.ingest` to reload documents
- Check logs for ingestion errors

### Agent Handover Failing
- Check `HandoverPayload` structure in `app/handover/protocol.py`
- Verify target agent is registered in `app/orchestration/graph.py`
- Check audit logs in structured JSON output

### Low Retrieval Quality
- Increase `chunk_size` and `chunk_overlap` in settings
- Enable hybrid search (vector + BM25) for better recall
- Add more diverse KB documents covering edge cases
- Implement query rewriting for better embeddings

## Performance Considerations

- **Batch Processing**: Implement conversation batching for high throughput
- **Caching**: Add Redis cache for frequent KB queries
- **Async Processing**: Use FastAPI's async/await for I/O-bound operations
- **Rate Limiting**: Implement token bucket or sliding window rate limits
- **Database**: Upgrade from in-memory to PostgreSQL/MongoDB for persistence


## Future Improvements

- Conversation-aware retrieval using historical context
- Long-term memory summarization
- Redis-backed persistent memory
- Streaming token responses
- Advanced hallucination detection
- Feedback-driven retrieval optimization
- Human-in-the-loop escalation workflows
- Multi-tenant session isolation
- Analytics dashboard for observability metrics
- Role-aware contextual retrieval

## License

Confidential - AI Engineering Internship Assessment

## Support

For questions or issues, please refer to the detailed [ARCHITECTURE.md](ARCHITECTURE.md) documentation or open an issue in the repository.
