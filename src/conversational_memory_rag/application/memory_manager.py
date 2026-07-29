from abc import ABC, abstractmethod

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.message import Message


class MemoryManager(ABC):

    @abstractmethod
    def get_context(
        self,
        conversation: Conversation
    ) -> ConversationContext :
        pass