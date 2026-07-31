import chromadb

from conversational_memory_rag.application.vector_store import VectorStore

from conversational_memory_rag.domain.retrieved_chunk import RetrievedChunk
from conversational_memory_rag.domain.retrieval_result import RetrievalResult


class ChromaVectorStore(VectorStore):

    def __init__(self):

        client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self._collection = client.get_or_create_collection(
            name="bedrock_docs"
        )

    def add(
        self,
        chunk_id: str,
        chunk_text: str,
        embedding: list[float],
        metadata: dict
    ) -> None:

        self._collection.add(
            ids=[chunk_id],
            documents=[chunk_text],
            embeddings=[embedding],
            metadatas=[metadata]
        )

    def search(
        self,
        embedding: list[float],
        n_results: int = 3
    ) -> RetrievalResult:

        results = self._collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )

        retrieved_chunks = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            retrieved_chunks.append(
                RetrievedChunk(
                    content=document,
                    metadata=metadata,
                    similarity=1 - distance
                )
            )

        return RetrievalResult(
            chunks=retrieved_chunks
        )