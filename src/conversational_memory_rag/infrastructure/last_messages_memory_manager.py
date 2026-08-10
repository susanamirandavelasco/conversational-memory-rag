from conversational_memory_rag.application.memory_manager import MemoryManager
from conversational_memory_rag.application.conversation_summarizer import (
    ConversationSummarizer
)

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.conversation_context import ConversationContext



class LastMessagesMemoryManager(MemoryManager):

    def __init__(
        self,
        summarizer: ConversationSummarizer,
        max_messages: int = 5
    ):
        self._summarizer = summarizer
        self._max_messages = max_messages

    def get_context(
        self,
        conversation: Conversation
    ) -> ConversationContext:

        messages = tuple(
            conversation.messages[-self._max_messages:]
        )

        summary = None

        if len(conversation.messages) > self._max_messages:

            context_for_summary = ConversationContext(
                messages=tuple(conversation.messages)
            )

            summary = self._summarizer.summarize(
                context_for_summary
            )

        return ConversationContext(
            messages=messages,
            summary=summary
        )