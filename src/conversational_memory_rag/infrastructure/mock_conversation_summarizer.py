from conversational_memory_rag.application.conversation_summarizer import (
    ConversationSummarizer
)

from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.summary import Summary


class MockConversationSummarizer(ConversationSummarizer):

    def summarize(
        self,
        conversation_context: ConversationContext
    ) -> Summary:

        return Summary(
            content="This is a mock conversation summary."
        )