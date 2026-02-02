# FastAPI Todo App Backend

A robust, async-ready FastAPI backend for a Todo application.

## Features
- **FastAPI** for high performance.
- **PostgreSQL** with **asyncpg** and **SQLAlchemy**.
- **Pydantic** for validation.
- **Docker** for database.
- **Alembic** for migrations.
- **JWT Authentication**.

## Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- `uv` (recommended)

### Installation
1. Install dependencies:
   ```bash
   uv sync
   ```
2. Create `.env` file (already created):
   ```bash
   cp .env.example .env
   ```
3. Start Database:
   ```bash
   docker-compose up -d
   ```

### Running the App
Use the provided script:
```bash
./run.sh
```
Or manually:
```bash
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

## API Documentation
Once running, visit:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure
- `app/`: Application source code.
- `app/routers/`: API endpoints.
- `app/crud/`: Database operations.
- `app/models/`: SQLAlchemy models.
- `app/schemas/`: Pydantic schemas.
- `tests/`: Tests (setup only).
