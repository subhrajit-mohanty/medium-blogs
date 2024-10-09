from src.database.neo4j_client import Neo4jClient
from src.database.qdrant_client import QdrantClientWrapper
from src.services.embedding_service import EmbeddingService
from openai import OpenAI
from src.config import OPENAI_API_KEY

class QueryService:
    def __init__(self):
        self.neo4j_client = Neo4jClient()
        self.qdrant_client = QdrantClientWrapper()
        self.embedding_service = EmbeddingService()
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

    def query_knowledge_graph(self, question):
        question_embedding = self.embedding_service.generate_embedding(question)
        
        results = self.qdrant_client.search(question_embedding)
        context = [f"{result.payload}" for result in results[:3]]
        
        cypher_query = self._generate_cypher_query(question)
        neo4j_result = self.neo4j_client.execute_query(cypher_query)
        
        combined_context = context + [str(neo4j_result)]
        
        return self._generate_answer(question, combined_context)

    def _generate_cypher_query(self, question):
        cypher_prompt = (
            "Generate a Cypher query to extract relevant information from a Neo4j graph database "
            "representing a university knowledge graph. The query should address the following question: "
            f"'{question}'\n\nProvide ONLY the Cypher query, without any explanations or additional text."
        )
        completion = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Cypher query generator. Respond with only the Cypher query, no explanations."},
                {"role": "user", "content": cypher_prompt}
            ]
        )
        return completion.choices[0].message.content.strip()

    def _generate_answer(self, question, context):
        answer_prompt = f"Based on the following context from a university knowledge graph, provide a human-readable answer to the question: '{question}'\n\nContext: {context}"
        completion = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                {"role": "user", "content": answer_prompt}
            ]
        )
        return completion.choices[0].message.content.strip()