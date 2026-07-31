import os

from openai import OpenAI

from dotenv import load_dotenv

class EmbeddingService:

    def __init__(self):
        
        load_dotenv()

        self._client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate(
        self,
        text: str
    ) -> list[float]:

        response = self._client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding