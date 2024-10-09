# Folder Structure
```
│
├── .env
├── requirements.txt
├── main.py
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── neo4j_client.py
│   │   └── qdrant_client.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── student.py
│   │   ├── professor.py
│   │   └── course.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embedding_service.py
│   │   └── query_service.py
│   └── utils/
│       ├── __init__.py
│       └── data_loader.py
│
└── tests/
    ├── __init__.py
    ├── test_neo4j_client.py
    ├── test_qdrant_client.py
    └── test_query_service.py
```
