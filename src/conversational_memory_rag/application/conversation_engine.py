from conversational_memory_rag.application.generator import Generator
from conversational_memory_rag.application.prompt_builder import PromptBuilder
from conversational_memory_rag.application.default_prompt_builder import DefaultPromptBuilder

from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role
from conversational_memory_rag.domain.conversation import Conversation


class ConversationEngine:

    def __init__(
        self,
        prompt_builder: PromptBuilder,
        generator: Generator
    ):
        self._prompt_builder = prompt_builder
        self._generator = generator

    def ask(
        self,
        conversation: Conversation
    ) -> str:

        prompt = self._prompt_builder.build(conversation)

        response = self._generator.generate(prompt)

        conversation.add_message(
            Message(
                role=Role.ASSISTANT,
                content=response
            )
        )

        return response