75 Days of Building: Agentic RAG
Day 1: Infrastructure & Backend Foundation
🎯 Overview
Welcome to Day 1 of building a production-grade Agentic Retrieval-Augmented Generation (RAG) system. The focus for today was entirely on establishing a robust, scalable infrastructure. Before diving into complex LLM orchestration and hybrid retrieval, we need a rock-solid environment to handle vector storage, caching, and async API requests.

🛠️ Tech Stack & Tools Deployed
Environment: WSL (Windows Subsystem for Linux)

Containerization: Docker & Docker Compose

Database (Vector & Relational): PostgreSQL extended with pgvector

Caching & Queueing: Redis

Backend Framework: FastAPI (Async Python)

✅ Milestones Achieved
1. Development Environment Setup
Configured WSL to ensure a native Linux development experience.

Established the base project directory and initialized version control.

2. Containerized Infrastructure (Docker)
Drafted the docker-compose.yml to orchestrate our core services.

Successfully spun up a PostgreSQL instance configured with the pgvector extension to handle our future document embeddings.

Deployed Redis to serve as our high-performance cache and message broker for background tasks.

3. FastAPI Project Scaffolding
Set up a modular, scalable project structure for the backend API.

Initialized the FastAPI application with basic routing.

Prepared the dependency management environment (ready for SQLAlchemy, Alembic, and Pydantic integration).

💻 Getting Started (Local Development)
To spin up the infrastructure established on Day 1, run the following commands:

1. Start the Docker Containers:

Bash
# This will start PostgreSQL (with pgvector) and Redis in the background
docker-compose up -d
2. Verify Containers are Running:

Bash
docker ps
3. Run the FastAPI Server:

Bash
# Navigate to the backend directory and start the dev server
fastapi dev main.py
The API documentation will be available at http://localhost:8000/docs.

⏭️ What's Next?
With the infrastructure running smoothly, upcoming days will focus on connecting the backend to our databases using SQLAlchemy, setting up database migrations with Alembic, and structuring our data validation using Pydantic.