from conversational_memory_rag.application.conversation_engine import ConversationEngine

from conversational_memory_rag.infrastructure.mock_generator import MockGenerator

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role

conversation = Conversation()

conversation.add_message(
    Message(
        role=Role.USER,
        content="What is Amazon Bedrock?"
    )
)

engine = ConversationEngine(
    generator=MockGenerator()
)

response = engine.ask(conversation)

print(response)

for message in conversation.messages:
    print(message.role.value, message.content)