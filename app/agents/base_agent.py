from abc import ABC, abstractmethod

from app.orchestration.state import ConversationState


class BaseAgent(ABC):

    def __init__(
        self,
        agent_name: str,
    ):

        self.agent_name = agent_name

    @abstractmethod
    def process(
        self,
        state: ConversationState,
    ) -> ConversationState:
        """
        Process conversation state
        and return updated state.
        """
        pass