from conversational_memory_rag.application.conversation_engine import ConversationEngine

from conversational_memory_rag.application.default_prompt_builder import DefaultPromptBuilder

from conversational_memory_rag.infrastructure.mock_generator import MockGenerator
from conversational_memory_rag.infrastructure.mock_retriever import MockRetriever

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role


def main():

# This demo uses mock components to validate the architecture.
# Real implementations will be integrated in later sprints.

    conversation = Conversation()

    conversation.add_message(
        Message(
            role=Role.USER,
            content="What is Amazon Bedrock (This is a demo question)?"
        )
    )

    engine = ConversationEngine(
        retriever=MockRetriever(),
        prompt_builder=DefaultPromptBuilder(),
        generator=MockGenerator()
    )

    response = engine.ask(conversation)

    print("\nAssistant:\n")
    print(response)


if __name__ == "__main__":
    main()