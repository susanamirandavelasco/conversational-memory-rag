from conversational_memory_rag.application.ingestion_service import IngestionService

from conversational_memory_rag.infrastructure.embedding_service import EmbeddingService
from conversational_memory_rag.infrastructure.chroma_vector_store import ChromaVectorStore


def main():

    embedding_service = EmbeddingService()

    vector_store = ChromaVectorStore()

    ingestion_service = IngestionService(
        embedding_service=embedding_service,
        vector_store=vector_store
    )

    ingestion_service.ingest(
        pdf_path="data/bedrock-ug.pdf",
        start_page=2500,
        end_page=2900
    )


if __name__ == "__main__":
    main()