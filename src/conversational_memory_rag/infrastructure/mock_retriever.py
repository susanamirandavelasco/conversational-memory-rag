from conversational_memory_rag.application.retriever import Retriever
from conversational_memory_rag.domain.retrieval_result import RetrievalResult
from conversational_memory_rag.domain.retrieved_chunk import RetrievedChunk


class MockRetriever(Retriever):

    def retrieve(
        self,
        query: str
    ) -> RetrievalResult:

        return RetrievalResult(
            chunks=(
                RetrievedChunk(
                    content="Amazon Bedrock is a fully managed service... (This is a mock Retriever)",
                    source="bedrock.pdf",
                    chunk_number=12,
                    score=0.98
                ),
            )
        )