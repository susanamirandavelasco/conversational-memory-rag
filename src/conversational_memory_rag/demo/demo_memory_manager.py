from conversational_memory_rag.infrastructure.last_messages_memory_manager import (
    LastMessagesMemoryManager,
)

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role


def main():

    conversation = Conversation()

    conversation.add_message(
        Message(Role.USER, "Hi")
    )

    conversation.add_message(
        Message(Role.ASSISTANT, "Hello!")
    )

    conversation.add_message(
        Message(Role.USER, "What is Amazon Bedrock?")
    )

    conversation.add_message(
        Message(Role.ASSISTANT, "Amazon Bedrock is...")
    )

    conversation.add_message(
        Message(Role.USER, "Does it support Claude?")
    )

    memory = LastMessagesMemoryManager(
        max_messages=3
    )

    conversation_context = memory.get_context(conversation)

    print()

    for message in conversation_context:
        print(f"{message.role.name}: {message.content}")


if __name__ == "__main__":
    main()