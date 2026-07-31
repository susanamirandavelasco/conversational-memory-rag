from abc import ABC, abstractmethod

from conversational_memory_rag.domain.retrieval_result import RetrievalResult


class VectorStore(ABC):

    @abstractmethod
    def add(
        self,
        chunk_id: str,
        chunk_text: str,
        embedding: list[float],
        metadata: dict
    ) -> None:
        pass

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        n_results: int = 3
    ) -> RetrievalResult:
        pass