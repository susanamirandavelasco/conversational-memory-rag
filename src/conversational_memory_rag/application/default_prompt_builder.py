from conversational_memory_rag.application.prompt_builder import PromptBuilder

from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.retrieval_result import RetrievalResult
from conversational_memory_rag.domain.prompt import Prompt


SYSTEM_PROMPT = """
    You are an AWS Bedrock expert.

    Answer only using the provided context.
    """

class DefaultPromptBuilder(PromptBuilder):

    def build(
        self,
        conversation_context: ConversationContext,
        retrieval_result: RetrievalResult
    ) -> Prompt:

        history = "\n".join(
            f"{message.role.name}: {message.content}"
            for message in conversation_context.messages
        )

        summary = (
            conversation_context.summary.content
            if conversation_context.summary
            else "No previous conversation summary."
        )

        retrieved_context = "\n\n".join(
            chunk.content
            for chunk in retrieval_result.chunks
        )

        return Prompt(
                content=f"""
                    {SYSTEM_PROMPT}
                    Conversation:
                    {history}
                    Retrieved Context:
                    {retrieved_context}
                    Conversation Summary:
                    {summary}
                    Assistant:
                    """
                    )