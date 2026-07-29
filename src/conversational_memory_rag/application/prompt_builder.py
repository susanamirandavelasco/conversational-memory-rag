from abc import ABC, abstractmethod

from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.retrieval_result import RetrievalResult
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.prompt import Prompt



class PromptBuilder(ABC):

    @abstractmethod
    def build(
        self,
        conversation_context: ConversationContext,
        retrieval_result: RetrievalResult
    ) -> Prompt:
        pass