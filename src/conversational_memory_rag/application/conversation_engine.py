from conversational_memory_rag.application.generator import Generator
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role
from conversational_memory_rag.domain.conversation import Conversation


class ConversationEngine:

    def __init__(self, generator: Generator):

        self._generator = generator

    def ask(
        self,
        conversation: Conversation
    ) -> str:

        user_message = conversation.get_last_message()

        response = self._generator.generate(
            prompt=user_message.content
        )

        conversation.add_message(
            Message(
                role=Role.ASSISTANT,
                content=response
            )
        )

        return response