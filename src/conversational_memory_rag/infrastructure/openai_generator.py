import os

from openai import OpenAI
from dotenv import load_dotenv

from conversational_memory_rag.application.generator import Generator
from conversational_memory_rag.domain.prompt import Prompt

from conversational_memory_rag.config import DEFAULT_MODEL


class OpenAIGenerator(Generator):

    def __init__(self):

        load_dotenv()
        
        self._client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate(
        self,
        prompt: Prompt
    ) -> str:

        response = self._client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt.content
                }
            ]
        )

        return response.choices[0].message.content