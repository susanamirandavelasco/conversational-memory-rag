from conversational_memory_rag.application.conversation_engine import (
    ConversationEngine
)

from conversational_memory_rag.application.default_prompt_builder import (
    DefaultPromptBuilder
)

from conversational_memory_rag.application.default_question_rewriter_prompt_builder import (
    DefaultQuestionRewriterPromptBuilder
)

from conversational_memory_rag.infrastructure.embedding_service import (
    EmbeddingService
)

from conversational_memory_rag.infrastructure.chroma_vector_store import (
    ChromaVectorStore
)

from conversational_memory_rag.infrastructure.chroma_retriever import (
    ChromaRetriever
)

from conversational_memory_rag.infrastructure.last_messages_memory_manager import (
    LastMessagesMemoryManager
)

from conversational_memory_rag.infrastructure.openai_generator import (
    OpenAIGenerator
)

from conversational_memory_rag.infrastructure.openai_question_rewriter import (
    OpenAIQuestionRewriter
)

from conversational_memory_rag.infrastructure.openai_conversation_summarizer import (
    OpenAIConversationSummarizer
)

from conversational_memory_rag.infrastructure.default_conversation_summarizer_prompt_builder import (
    DefaultConversationSummarizerPromptBuilder
)

from conversational_memory_rag.evaluation.evaluation_runner import (
    EvaluationRunner
)

from conversational_memory_rag.evaluation.memory_cases import (
    get_memory_evaluation_cases
)

from conversational_memory_rag.evaluation.llm_judge_evaluator import (
    LLMJudgeEvaluator
)


def build_engine() -> ConversationEngine:

    embedding_service = EmbeddingService()

    vector_store = ChromaVectorStore()

    summarizer = OpenAIConversationSummarizer(
        prompt_builder=DefaultConversationSummarizerPromptBuilder()
    )

    memory_manager = LastMessagesMemoryManager(
        summarizer=summarizer,
        max_messages=5
    )

    question_rewriter = OpenAIQuestionRewriter(
        prompt_builder=DefaultQuestionRewriterPromptBuilder()
    )

    retriever = ChromaRetriever(
        embedding_service=embedding_service,
        vector_store=vector_store
    )

    return ConversationEngine(
        memory_manager=memory_manager,
        prompt_builder=DefaultPromptBuilder(),
        generator=OpenAIGenerator(),
        retriever=retriever,
        question_rewriter=question_rewriter
    )


def main():

    engine = build_engine()

    runner = EvaluationRunner(
        engine=engine,
        evaluator=LLMJudgeEvaluator()
        )

    cases = get_memory_evaluation_cases()

    results = runner.run(cases)

    for result in results:

        print("\n" + "=" * 80)

        print(
            f"{result.case_id} - {result.case_name}"
        )

        print(
            f"Category: {result.category}"
        )

        print(
            f"\nExpected:\n{result.expected_answer}"
        )

        print(
            f"\nActual:\n{result.actual_answer}"
        )

        score = result.evaluation_score

        print(
            f"\nPassed: {score.passed}"
        )

        print(
            f"Score: {score.score}"
        )

        print(
            f"Reason: {score.reason}"
        )

    passed = sum(
        1
        for result in results
        if result.evaluation_score
        and result.evaluation_score.passed
    )

    total = len(results)

    average_score = sum(
        result.evaluation_score.score
        for result in results
        if result.evaluation_score
    ) / total

    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print(f"Passed: {passed}/{total}")
    print(f"Average score: {average_score:.2f}")
 


if __name__ == "__main__":
    main()