import json

from openai import OpenAI

from conversational_memory_rag.config import Settings
from conversational_memory_rag.evaluation.evaluation_result import EvaluationResult
from conversational_memory_rag.evaluation.evaluation_score import EvaluationScore
from conversational_memory_rag.evaluation.evaluator import Evaluator


class LLMJudgeEvaluator(Evaluator):
    def __init__(self, client: OpenAI | None = None, model: str | None = None):
        settings = Settings.from_env()
        self._client = client or OpenAI(
            timeout=settings.openai_timeout_seconds,
            max_retries=settings.openai_max_retries,
        )
        self._model = model or settings.evaluator_model

    def evaluate(self, result: EvaluationResult) -> EvaluationScore:

        prompt = f"""
            You are evaluating the correctness of an AI system response.

            Expected answer:
            {result.expected_answer}

            Actual answer:
            {result.actual_answer}

            Determine whether the actual answer correctly satisfies the expected answer.

            Return ONLY valid JSON with this exact structure:

            {{
            "passed": true,
            "score": 1.0,
            "reason": "Short explanation"
            }}

            Rules:
            - passed must be true or false.
            - score must be between 0.0 and 1.0.
            - Semantic equivalence is acceptable.
            - Do not require exact wording.
            - Do not reward answers that contradict the expected answer.
            """

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content.strip()

        data = json.loads(content)

        return EvaluationScore(
            passed=data["passed"], score=data["score"], reason=data["reason"]
        )
