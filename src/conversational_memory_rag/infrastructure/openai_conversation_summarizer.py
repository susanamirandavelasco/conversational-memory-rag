from openai import OpenAI

from dotenv import load_dotenv

from conversational_memory_rag.application.conversation_summarizer import (
    ConversationSummarizer
)

from conversational_memory_rag.application.conversation_summarizer_prompt_builder import (
    ConversationSummarizerPromptBuilder
)

from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.summary import Summary


class OpenAIConversationSummarizer(ConversationSummarizer):

    def __init__(
        self,
        prompt_builder: ConversationSummarizerPromptBuilder
    ):
        load_dotenv()
        
        self._client = OpenAI()
        self._prompt_builder = prompt_builder

    def summarize(
        self,
        conversation_context: ConversationContext
    ) -> Summary:

        prompt = self._prompt_builder.build(
            conversation_context
        )

        response = self._client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt.content
                }
            ],
            temperature=0
        )

        summary = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        return Summary(
            content=summary
        )