from dataclasses import dataclass, field

from conversational_memory_rag.domain.message import Message

class ConversationContext:

    def __init__(
        self,
        messages: tuple[Message, ...]
    ):
        self._messages = messages

    @property
    def messages(self) -> tuple[Message, ...]:
        return self._messages