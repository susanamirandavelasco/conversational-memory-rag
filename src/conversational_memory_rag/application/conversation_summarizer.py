from abc import ABC, abstractmethod

from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.summary import Summary


class ConversationSummarizer(ABC):

    @abstractmethod
    def summarize(
        self,
        conversation_context: ConversationContext
    ) -> Summary:
        pass