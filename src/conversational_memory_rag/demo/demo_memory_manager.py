from conversational_memory_rag.infrastructure.last_messages_memory_manager import (
    LastMessagesMemoryManager,
)
from conversational_memory_rag.infrastructure.mock_conversation_summarizer import (
    MockConversationSummarizer,
)

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role


def main():

    conversation = Conversation()

    summarizer = MockConversationSummarizer()

    memory = LastMessagesMemoryManager(
        summarizer=summarizer,
        max_messages=5
    )

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

    conversation.add_message(
        Message(Role.ASSISTANT, "Yes, of course...")
    )

    conversation.add_message(
        Message(Role.USER, "How much is it?")
    )

    conversation.add_message(
        Message(Role.ASSISTANT, "It depends...")
    )

    conversation.add_message(
        Message(Role.USER, "Is it easy to integrate?")
    )

    conversation.add_message(
        Message(Role.ASSISTANT, "Yes of course, but it depends on...")
    )

    conversation_context = memory.get_context(conversation)

    print()

    for message in conversation_context.messages:
        print(f"{message.role.name}: {message.content}")

    if conversation_context.summary:
        print(conversation_context.summary.content)
    else:
        print("No summary")


if __name__ == "__main__":
    main()