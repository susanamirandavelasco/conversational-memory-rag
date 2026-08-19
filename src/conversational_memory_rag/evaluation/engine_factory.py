from conversational_memory_rag.infrastructure.embedding_service import (
    EmbeddingService
)

from conversational_memory_rag.infrastructure.chroma_vector_store import (
    ChromaVectorStore
)

from conversational_memory_rag.infrastructure.chroma_retriever import (
    ChromaRetriever
)

from conversational_memory_rag.infrastructure.last_messages_memory_manager import (
    LastMessagesMemoryManager
)

from conversational_memory_rag.infrastructure.openai_generator import (
    OpenAIGenerator
)

from conversational_memory_rag.infrastructure.openai_question_rewriter import (
    OpenAIQuestionRewriter
)

from conversational_memory_rag.infrastructure.openai_conversation_summarizer import (
    OpenAIConversationSummarizer
)

from conversational_memory_rag.infrastructure.default_conversation_summarizer_prompt_builder import (
    DefaultConversationSummarizerPromptBuilder
)

from conversational_memory_rag.infrastructure.no_op_question_rewriter import (
    NoOpQuestionRewriter
)

from conversational_memory_rag.infrastructure.no_op_conversation_summarizer import (
    NoOpConversationSummarizer
)

from conversational_memory_rag.application.conversation_engine import ConversationEngine

from conversational_memory_rag.application.default_question_rewriter_prompt_builder import (
    DefaultQuestionRewriterPromptBuilder
)

from conversational_memory_rag.application.default_prompt_builder import (
    DefaultPromptBuilder
)

def build_engine(
    n_results: int = 3,
    use_question_rewriter: bool = True,
    use_summary: bool = True
    ) -> ConversationEngine:

        embedding_service = EmbeddingService()

        vector_store = ChromaVectorStore()

        if use_summary:
            summarizer = OpenAIConversationSummarizer(
                prompt_builder=DefaultConversationSummarizerPromptBuilder()
            )
        else:
            summarizer = NoOpConversationSummarizer()

        memory_manager = LastMessagesMemoryManager(
            summarizer=summarizer,
            max_messages=5
        )

        if use_question_rewriter:
            question_rewriter = OpenAIQuestionRewriter(
                prompt_builder=DefaultQuestionRewriterPromptBuilder()
            )
        else:
            question_rewriter = NoOpQuestionRewriter()
            
        retriever = ChromaRetriever(
            embedding_service=embedding_service,
            vector_store=vector_store
        )

        return ConversationEngine(
            memory_manager=memory_manager,
            prompt_builder=DefaultPromptBuilder(),
            generator=OpenAIGenerator(),
            retriever=retriever,
            question_rewriter=question_rewriter,
            n_results=n_results
        )