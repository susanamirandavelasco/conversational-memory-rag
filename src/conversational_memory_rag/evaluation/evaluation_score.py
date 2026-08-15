from dataclasses import dataclass


@dataclass
class EvaluationScore:
    passed: bool
    score: float
    reason: str