from abc import ABC, abstractmethod

from conversational_memory_rag.domain.conversation import Conversation


class PromptBuilder(ABC):

    @abstractmethod
    def build(
        self,
        conversation: Conversation
    ) -> str:
        pass