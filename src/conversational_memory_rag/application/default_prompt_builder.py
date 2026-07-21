from conversational_memory_rag.application.prompt_builder import PromptBuilder
from conversational_memory_rag.domain.conversation import Conversation


class DefaultPromptBuilder(PromptBuilder):

    def build(
        self,
        conversation: Conversation
    ) -> str:

        last_message = conversation.get_last_message()

        return f"""
            You are a helpful AI assistant.

            User question:

            {last_message.content}

            Answer:
            """