from abc import ABC, abstractmethod

from conversational_memory_rag.evaluation.evaluation_result import (
    EvaluationResult
)

from conversational_memory_rag.evaluation.evaluation_score import (
    EvaluationScore
)


class Evaluator(ABC):

    @abstractmethod
    def evaluate(
        self,
        result: EvaluationResult
    ) -> EvaluationScore:
        pass