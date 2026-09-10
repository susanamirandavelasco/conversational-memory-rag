from unittest.mock import Mock

from conversational_memory_rag.application.conversation_engine import ConversationEngine
from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.prompt import Prompt
from conversational_memory_rag.domain.retrieval_result import RetrievalResult
from conversational_memory_rag.domain.role import Role


def test_engine_orchestrates_pipeline_and_stores_answer():
    conversation = Conversation()
    conversation.add_message(Message(role=Role.USER, content="What is Bedrock?"))
    initial_context = ConversationContext(messages=conversation.messages)
    rewritten_context = ConversationContext(
        messages=conversation.messages,
        rewritten_question="What is Amazon Bedrock?",
    )
    retrieval_result = RetrievalResult(chunks=())
    prompt = Prompt("answer using context")

    memory_manager = Mock()
    memory_manager.get_context.return_value = initial_context
    question_rewriter = Mock()
    question_rewriter.rewrite.return_value = rewritten_context
    retriever = Mock()
    retriever.retrieve.return_value = retrieval_result
    prompt_builder = Mock()
    prompt_builder.build.return_value = prompt
    generator = Mock()
    generator.generate.return_value = "A managed foundation-model service."

    engine = ConversationEngine(
        memory_manager=memory_manager,
        prompt_builder=prompt_builder,
        generator=generator,
        retriever=retriever,
        question_rewriter=question_rewriter,
        n_results=5,
    )

    response = engine.ask(conversation)

    assert response == "A managed foundation-model service."
    assert conversation.get_last_message().role is Role.ASSISTANT
    assert conversation.get_last_message().content == response
    memory_manager.get_context.assert_called_once_with(conversation)
    question_rewriter.rewrite.assert_called_once_with(initial_context)
    retriever.retrieve.assert_called_once_with(rewritten_context, n_results=5)
    prompt_builder.build.assert_called_once_with(
        conversation_context=rewritten_context,
        retrieval_result=retrieval_result,
    )
    generator.generate.assert_called_once_with(prompt)
