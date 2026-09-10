import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    generation_model: str = "gpt-5"
    question_rewriter_model: str = "gpt-4.1-mini"
    summarizer_model: str = "gpt-4.1-mini"
    evaluator_model: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-3-small"
    chroma_path: str = "./chroma_db"
    chroma_collection: str = "bedrock_docs"
    openai_timeout_seconds: float = 30.0
    openai_max_retries: int = 2

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            generation_model=os.getenv("GENERATION_MODEL", cls.generation_model),
            question_rewriter_model=os.getenv(
                "QUESTION_REWRITER_MODEL", cls.question_rewriter_model
            ),
            summarizer_model=os.getenv("SUMMARIZER_MODEL", cls.summarizer_model),
            evaluator_model=os.getenv("EVALUATOR_MODEL", cls.evaluator_model),
            embedding_model=os.getenv("EMBEDDING_MODEL", cls.embedding_model),
            chroma_path=os.getenv("CHROMA_PATH", cls.chroma_path),
            chroma_collection=os.getenv("CHROMA_COLLECTION", cls.chroma_collection),
            openai_timeout_seconds=float(
                os.getenv("OPENAI_TIMEOUT_SECONDS", cls.openai_timeout_seconds)
            ),
            openai_max_retries=int(
                os.getenv("OPENAI_MAX_RETRIES", cls.openai_max_retries)
            ),
        )


DEFAULT_MODEL = Settings.generation_model
