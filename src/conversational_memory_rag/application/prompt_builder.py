from abc import ABC, abstractmethod

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.retrieval_result import RetrievalResult
from conversational_memory_rag.domain.message import Message


class PromptBuilder(ABC):

    @abstractmethod
    def build(
        self,
        conversation_context: tuple[Message, ...],
        retrieval_result: RetrievalResult
    ) -> str:
        pass