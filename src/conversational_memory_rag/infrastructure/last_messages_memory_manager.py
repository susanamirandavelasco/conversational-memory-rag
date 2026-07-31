from conversational_memory_rag.application.memory_manager import MemoryManager

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.conversation_context import ConversationContext



class LastMessagesMemoryManager(MemoryManager):

    def __init__(
        self,
        max_messages: int = 5
    ):
        self._max_messages = max_messages

    def get_context(
        self,
        conversation: Conversation
    ) -> tuple[Message, ...]:

        return ConversationContext(
            messages=tuple(
            conversation.messages[-self._max_messages:]
            )
        )