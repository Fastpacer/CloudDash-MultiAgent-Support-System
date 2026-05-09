from app.agents.triage_agent import TriageAgent
from app.agents.technical_agent import TechnicalAgent
from app.agents.billing_agent import BillingAgent
from app.agents.escalation_agent import EscalationAgent


agent_registry = {
    "triage_agent": TriageAgent(),
    "technical_agent": TechnicalAgent(),
    "billing_agent": BillingAgent(),
    "escalation_agent": EscalationAgent(),
}