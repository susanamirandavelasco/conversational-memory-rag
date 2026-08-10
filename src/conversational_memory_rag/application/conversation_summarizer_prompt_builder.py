from abc import ABC, abstractmethod

from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.prompt import Prompt

class ConversationSummarizerPromptBuilder(ABC):

    @abstractmethod
    def build(
        self,
        conversation_context: ConversationContext
    ) -> Prompt:
        pass