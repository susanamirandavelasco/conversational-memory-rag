from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class RetrievedChunk:
    content: str
    source: str
    page_range: str
    chunk_number: int
    score: float
