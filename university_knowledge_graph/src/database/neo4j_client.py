from neo4j import GraphDatabase
from src.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def add_entity(self, entity_type, entity):
        with self.driver.session() as session:
            session.execute_write(self._add_entity_tx, entity_type, entity)

    @staticmethod
    def _add_entity_tx(tx, entity_type, entity):
        query = (
            f"CREATE (e:{entity_type} {{id: $id}}) "
            f"SET e += $properties "
            "RETURN e"
        )
        tx.run(query, id=entity['id'], properties=entity)

    def create_relationships(self, entity_type, entity):
        with self.driver.session() as session:
            session.execute_write(self._create_relationships_tx, entity_type, entity)

    @staticmethod
    def _create_relationships_tx(tx, entity_type, entity):
        if entity_type == "Student":
            for course_code in entity.get('enrolled_courses', []):
                tx.run(
                    "MATCH (s:Student {id: $student_id}), (c:Course {course_code: $course_code}) "
                    "MERGE (s)-[:ENROLLED_IN]->(c)",
                    student_id=entity['id'], course_code=course_code
                )
        elif entity_type == "Course":
            tx.run(
                "MATCH (p:Professor {name: $instructor}), (c:Course {id: $course_id}) "
                "MERGE (p)-[:TEACHES]->(c)",
                instructor=entity['instructor'], course_id=entity['id']
            )

    def execute_query(self, query):
        with self.driver.session() as session:
            return session.run(query).data()