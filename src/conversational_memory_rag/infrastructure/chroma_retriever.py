from conversational_memory_rag.application.retriever import Retriever

from conversational_memory_rag.infrastructure.embedding_service import EmbeddingService

from conversational_memory_rag.application.vector_store import VectorStore

from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.retrieval_result import RetrievalResult


class ChromaRetriever(Retriever):

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore
    ):

        self._embedding_service = embedding_service
        self._vector_store = vector_store

    def retrieve(
        self,
        conversation_context: ConversationContext,
        n_results: int

    ) -> RetrievalResult:

        print(">>> RETRIEVER CALLED <<<")

        #query = conversation_context.get_last_user_message().content
        query = conversation_context.rewritten_question

        embedding = self._embedding_service.generate(
            query
        )

        print(len(embedding))
        print(embedding[:5])

        return self._vector_store.search(
            embedding=embedding,
            n_results=n_results
        )