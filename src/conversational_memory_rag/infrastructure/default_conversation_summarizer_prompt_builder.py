from conversational_memory_rag.application.conversation_summarizer_prompt_builder import (
    ConversationSummarizerPromptBuilder
)

from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.prompt import Prompt


class DefaultConversationSummarizerPromptBuilder(
    ConversationSummarizerPromptBuilder
):

    def build(
        self,
        conversation_context: ConversationContext
    ) -> Prompt:

        conversation = "\n".join(
            f"{message.role.name}: {message.content}"
            for message in conversation_context.messages
        )

        content = f"""
            Summarize the following conversation.

            Capture the important facts, decisions, preferences,
            and information that may be relevant to future questions.

            Do not invent information.

            Conversation:

            {conversation}
            """

        return Prompt(content=content)