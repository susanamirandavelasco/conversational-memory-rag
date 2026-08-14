from dataclasses import dataclass


@dataclass
class EvaluationResult:
    case_id: str
    case_name: str
    category: str
    expected_answer: str
    actual_answer: str