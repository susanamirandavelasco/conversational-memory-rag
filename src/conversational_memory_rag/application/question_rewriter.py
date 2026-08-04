from abc import ABC, abstractmethod

from conversational_memory_rag.domain.conversation_context import ConversationContext


class QuestionRewriter(ABC):

    @abstractmethod
    def rewrite(
        self,
        conversation_context: ConversationContext
    ) -> ConversationContext:
        pass