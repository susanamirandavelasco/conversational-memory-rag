from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role


def main():

    conversation = Conversation()

    conversation.add_message(
        Message(
            role=Role.USER,
            content="What is Amazon Bedrock?"
        )
    )

    conversation.add_message(
        Message(
            role=Role.ASSISTANT,
            content="Amazon Bedrock is..."
        )
    )

    print()

    for message in conversation.messages:
        print(f"{message.role.value}: {message.content}")


if __name__ == "__main__":
    main()