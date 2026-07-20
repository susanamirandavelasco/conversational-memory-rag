from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from conversational_memory_rag.domain.message import Message


@dataclass
class Conversation:

    id: UUID = field(default_factory=uuid4)

    _messages: list[Message] = field(default_factory=list)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    def add_message(self, message: Message) -> None:
        self._messages.append(message)

    @property
    def messages(self) -> tuple[Message, ...]:
        return tuple(self._messages)