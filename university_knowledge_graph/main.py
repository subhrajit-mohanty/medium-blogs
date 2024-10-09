from src.database.qdrant_client import QdrantClientWrapper
from src.utils.data_loader import DataLoader
from src.services.query_service import QueryService

def main():
    # Setup Qdrant collections
    qdrant_client = QdrantClientWrapper()
    qdrant_client.setup_collections()

    # Load sample data
    data_loader = DataLoader()

    students = [
        {"name": "Alice Smith", "student_id": "S001", "major": "Computer Science", "enrolled_courses": ["CS101", "CS201", "MATH201"], "gpa": 3.8, "year": "Junior"},
        {"name": "Bob Johnson", "student_id": "S002", "major": "Physics", "enrolled_courses": ["PHY101", "MATH201", "CS101"], "gpa": 3.5, "year": "Sophomore"},
        {"name": "Charlie Brown", "student_id": "S003", "major": "Mathematics", "enrolled_courses": ["MATH201", "MATH301", "PHY101"], "gpa": 3.9, "year": "Senior"},
        {"name": "Diana Prince", "student_id": "S004", "major": "Computer Science", "enrolled_courses": ["CS101", "CS301", "AI401"], "gpa": 4.0, "year": "Senior"},
        {"name": "Ethan Hunt", "student_id": "S005", "major": "Data Science", "enrolled_courses": ["CS101", "STAT301", "AI401"], "gpa": 3.7, "year": "Junior"}
    ]

    professors = [
        {"name": "Dr. Jane Doe", "department": "Computer Science", "research_areas": ["Machine Learning", "AI", "Computer Vision"], "courses_taught": ["CS101", "AI401"]},
        {"name": "Dr. John Smith", "department": "Physics", "research_areas": ["Quantum Mechanics", "Astrophysics"], "courses_taught": ["PHY101", "PHY301"]},
        {"name": "Dr. Emily Brown", "department": "Mathematics", "research_areas": ["Number Theory", "Cryptography"], "courses_taught": ["MATH201", "MATH301"]},
        {"name": "Dr. Michael Johnson", "department": "Computer Science", "research_areas": ["Databases", "Data Mining"], "courses_taught": ["CS201", "CS301"]},
        {"name": "Dr. Sarah Lee", "department": "Statistics", "research_areas": ["Bayesian Statistics", "Machine Learning"], "courses_taught": ["STAT301"]}
    ]

    courses = [
        {"name": "Introduction to Programming", "course_code": "CS101", "department": "Computer Science", "instructor": "Dr. Jane Doe", "credits": 3, "capacity": 100},
        {"name": "Data Structures", "course_code": "CS201", "department": "Computer Science", "instructor": "Dr. Michael Johnson", "credits": 4, "capacity": 80},
        {"name": "Introduction to Physics", "course_code": "PHY101", "department": "Physics", "instructor": "Dr. John Smith", "credits": 4, "capacity": 120},
        {"name": "Advanced Mathematics", "course_code": "MATH201", "department": "Mathematics", "instructor": "Dr. Emily Brown", "credits": 3, "capacity": 60},
        {"name": "Artificial Intelligence", "course_code": "AI401", "department": "Computer Science", "instructor": "Dr. Jane Doe", "credits": 4, "capacity": 50},
        {"name": "Database Systems", "course_code": "CS301", "department": "Computer Science", "instructor": "Dr. Michael Johnson", "credits": 3, "capacity": 70},
        {"name": "Statistical Methods", "course_code": "STAT301", "department": "Statistics", "instructor": "Dr. Sarah Lee", "credits": 3, "capacity": 90},
        {"name": "Abstract Algebra", "course_code": "MATH301", "department": "Mathematics", "instructor": "Dr. Emily Brown", "credits": 4, "capacity": 40}
    ]

    data_loader.load_entities("Student", students)
    data_loader.load_entities("Professor", professors)
    data_loader.load_entities("Course", courses)

    # Query the knowledge graph
    query_service = QueryService()

    questions = [
        "What courses does Dr. Jane Doe teach, and who are the students in these courses?",
        "Which professors are involved in AI-related research, and what courses do they teach?",
        "Who are the top-performing students in the Computer Science department?",
        "What is the most popular course based on enrollment, and who teaches it?",
        "Are there any potential collaborations between Physics and Computer Science departments based on course overlap?"
    ]

    for question in questions:
        answer = query_service.query_knowledge_graph(question)
        print(f"Question: {question}")
        print(f"Answer: {answer}\n")

if __name__ == "__main__":
    main()