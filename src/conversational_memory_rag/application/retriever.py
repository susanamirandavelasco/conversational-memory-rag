from abc import ABC, abstractmethod

from conversational_memory_rag.domain.retrieval_result import RetrievalResult


class Retriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query: str
    ) -> RetrievalResult:
        pass