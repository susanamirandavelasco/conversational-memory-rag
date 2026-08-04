from abc import ABC, abstractmethod

from conversational_memory_rag.domain.retrieval_result import RetrievalResult
from conversational_memory_rag.domain.conversation_context import ConversationContext


class Retriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        conversation_context: ConversationContext,
        n_results: int
    ) -> RetrievalResult:
        pass