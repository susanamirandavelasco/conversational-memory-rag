from abc import ABC, abstractmethod

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.retrieval_result import RetrievalResult


class PromptBuilder(ABC):

    @abstractmethod
    def build(
        self,
        conversation: Conversation,
        retrieval_result: RetrievalResult
    ) -> str:
        pass