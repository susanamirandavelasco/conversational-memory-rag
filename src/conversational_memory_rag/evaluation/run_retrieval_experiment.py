from conversational_memory_rag.evaluation.engine_factory import build_engine
from conversational_memory_rag.evaluation.evaluation_runner import EvaluationRunner
from conversational_memory_rag.evaluation.llm_judge_evaluator import LLMJudgeEvaluator
from conversational_memory_rag.evaluation.retrieval_cases import (
    get_retrieval_evaluation_cases
)


def main():

    configurations = [3, 5, 10, 20]

    for n_results in configurations:

        print("\n" + "=" * 80)
        print(f"N_RESULTS = {n_results}")
        print("=" * 80)

        engine = build_engine(
            n_results=n_results
        )

        runner = EvaluationRunner(
            engine=engine,
            evaluator=LLMJudgeEvaluator()
        )

        cases = get_retrieval_evaluation_cases()

        results = runner.run(cases)

        for result in results:

            score = result.evaluation_score

            print(
                f"\n{result.case_id}"
                f" | Passed: {score.passed}"
                f" | Score: {score.score}"
            )

            print(f"Answer: {result.actual_answer}")
            print(f"Reason: {score.reason}")


if __name__ == "__main__":
    main()