from conversational_memory_rag.infrastructure.embedding_service import EmbeddingService
from conversational_memory_rag.application.vector_store import VectorStore

from conversational_memory_rag.ingestion.document_loader import load_pdf_pages
from conversational_memory_rag.ingestion.chunker import chunk_text


class IngestionService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore
    ):

        self._embedding_service = embedding_service
        self._vector_store = vector_store

    def ingest(
        self,
        pdf_path: str,
        start_page: int,
        end_page: int
    ) -> None:

        print("Loading PDF...")

        text = load_pdf_pages(
            pdf_path,
            start_page=start_page,
            end_page=end_page
        )

        print("Generating chunks...")

        chunks = chunk_text(text)

        print(f"Chunks generated: {len(chunks)}")

        for index, chunk in enumerate(chunks):

            print(f"Processing chunk {index}")

            embedding = self._embedding_service.generate(
                chunk
            )

            self._vector_store.add(
                chunk_id=f"chunk_{index}",
                chunk_text=chunk,
                embedding=embedding,
                metadata={
                    "source": pdf_path,
                    "chunk_number": index,
                    "page_range": f"{start_page}-{end_page}"
                }
            )

        print("Ingestion completed.")