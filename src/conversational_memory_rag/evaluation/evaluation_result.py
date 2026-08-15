from dataclasses import dataclass

from conversational_memory_rag.evaluation.evaluation_score import (
    EvaluationScore
)


@dataclass
class EvaluationResult:
    case_id: str
    case_name: str
    category: str
    expected_answer: str
    actual_answer: str
    evaluation_score: EvaluationScore | None = None