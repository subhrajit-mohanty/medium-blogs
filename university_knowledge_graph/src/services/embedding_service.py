from openai import OpenAI
from src.config import OPENAI_API_KEY

class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_embedding(self, text):
        response = self.client.embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding