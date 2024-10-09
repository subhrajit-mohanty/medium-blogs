from qdrant_client import QdrantClient
from qdrant_client.http import models
from src.config import QDRANT_URL, QDRANT_API_KEY, COLLECTIONS

class QdrantClientWrapper:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    def setup_collections(self):
        for collection in COLLECTIONS:
            self.client.recreate_collection(
                collection_name=collection,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )

    def add_entity(self, entity_type, entity, embedding):
        self.client.upsert(
            collection_name=entity_type,
            points=[
                models.PointStruct(
                    id=entity['id'],
                    vector=embedding,
                    payload=entity
                )
            ]
        )

    def search(self, query_vector, limit=5):
        results = []
        for collection in COLLECTIONS:
            search_result = self.client.search(
                collection_name=collection,
                query_vector=query_vector,
                limit=limit
            )
            results.extend(search_result)
        return sorted(results, key=lambda x: x.score, reverse=True)