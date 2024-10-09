import uuid
from src.database.neo4j_client import Neo4jClient
from src.database.qdrant_client import QdrantClientWrapper
from src.services.embedding_service import EmbeddingService

class DataLoader:
    def __init__(self):
        self.neo4j_client = Neo4jClient()
        self.qdrant_client = QdrantClientWrapper()
        self.embedding_service = EmbeddingService()

    def load_entities(self, entity_type, entities):
        for entity in entities:
            entity['id'] = str(uuid.uuid4())
            
            self.neo4j_client.add_entity(entity_type, entity)
            self.neo4j_client.create_relationships(entity_type, entity)

            entity_text = " ".join([f"{k}: {v}" for k, v in entity.items() if k != 'id'])
            embedding = self.embedding_service.generate_embedding(entity_text)
            self.qdrant_client.add_entity(entity_type, entity, embedding)