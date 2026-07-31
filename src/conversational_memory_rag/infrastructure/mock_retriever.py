from conversational_memory_rag.application.retriever import Retriever

from conversational_memory_rag.domain.retrieval_result import RetrievalResult
from conversational_memory_rag.domain.retrieved_chunk import RetrievedChunk
from conversational_memory_rag.domain.conversation_context import ConversationContext



class MockRetriever(Retriever):

    def retrieve(
        self,
        conversation_context: ConversationContext
    ) -> RetrievalResult:

        query = conversation_context.get_last_user_message().content

        print(f"USER QUERY: {query}")

        return RetrievalResult(
            chunks=(
                RetrievedChunk(
                    content="Amazon Bedrock is a funny, interesting, happy and fully managed service... (This is a mock Retriever)",
                    source="bedrock.pdf",
                    chunk_number=12,
                    score=0.98
                ),
            )
        )