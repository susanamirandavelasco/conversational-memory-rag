from dataclasses import dataclass, field
from typing import Any

from conversational_memory_rag.domain.retrieved_chunk import RetrievedChunk


@dataclass(frozen=True)
class RetrievalResult:
    chunks: tuple[RetrievedChunk, ...]