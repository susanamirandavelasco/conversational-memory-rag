from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from conversational_memory_rag.domain.role import Role


@dataclass(frozen=True)
class Message:
    role: Role
    content: str

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )