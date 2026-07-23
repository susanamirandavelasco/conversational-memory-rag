from conversational_memory_rag.application.conversation_engine import ConversationEngine
from conversational_memory_rag.application.default_prompt_builder import DefaultPromptBuilder

from conversational_memory_rag.infrastructure.mock_generator import MockGenerator
from conversational_memory_rag.infrastructure.mock_retriever import MockRetriever

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
    prompt_builder=DefaultPromptBuilder(),
    generator=MockGenerator()
)

response = engine.ask(conversation)

print(response)

for message in conversation.messages:
    print(message.role.value, message.content)


retriever = MockRetriever()
result = retriever.retrieve("What is Amazon Bedrock?")
print(result.chunks[0].content)