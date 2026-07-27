from conversational_memory_rag.application.memory_manager import MemoryManager

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message


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

        return conversation.messages[-self._max_messages:]