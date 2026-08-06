from conversational_memory_rag.application.conversation_engine import ConversationEngine
from conversational_memory_rag.application.default_prompt_builder import DefaultPromptBuilder
from conversational_memory_rag.application.default_question_rewriter_prompt_builder import DefaultQuestionRewriterPromptBuilder


from conversational_memory_rag.infrastructure.embedding_service import EmbeddingService
from conversational_memory_rag.infrastructure.chroma_vector_store import ChromaVectorStore
from conversational_memory_rag.infrastructure.chroma_retriever import ChromaRetriever
from conversational_memory_rag.infrastructure.last_messages_memory_manager import (
    LastMessagesMemoryManager,)
from conversational_memory_rag.infrastructure.openai_generator import OpenAIGenerator
from conversational_memory_rag.infrastructure.openai_question_rewriter import OpenAIQuestionRewriter


from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role
from conversational_memory_rag.domain.conversation_context import ConversationContext



def main():

# This demo uses mock components to validate the architecture.
# Real implementations will be integrated in later sprints.

    conversation = Conversation()

    conversation.add_message(
        Message(
            role=Role.USER,
            content="What is Amazon Bedrock ?"
        )
    )

    conversation.add_message(
        Message(
            role=Role.USER,
            content="Does it support Claude ?"
        )
    )

    conversation.add_message(
        Message(
            role=Role.USER,
            content="How much is it ?"
        )
    )

    embedding_service = EmbeddingService()

    vector_store = ChromaVectorStore()

    engine = ConversationEngine(
        memory_manager=LastMessagesMemoryManager(),
        prompt_builder=DefaultPromptBuilder(),
        generator=OpenAIGenerator(),
        retriever = ChromaRetriever(
            embedding_service=embedding_service,
            vector_store=vector_store
            ),
        question_rewriter = OpenAIQuestionRewriter(
            prompt_builder=DefaultQuestionRewriterPromptBuilder()
            )
        )

    response = engine.ask(conversation)

    print("\nAssistant:\n")
    print(response)


if __name__ == "__main__":
    main()