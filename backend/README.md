# TSV-RSM Backend

Multi-tenant Retail Store Management System - Backend API

## Tech Stack
- FastAPI (Python 3.11+)
- PostgreSQL 15+ with AsyncPG
- SQLAlchemy 2.0 (Async ORM)
- Alembic (migrations)
- 100% async

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis

### Installation
```bash
# Install dependencies
poetry install

# Set up environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
poetry run alembic upgrade head

# Start development server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Development

### Running Tests
```bash
poetry run pytest
poetry run pytest --cov=app tests/
```

### Linting
```bash
poetry run ruff check .
poetry run ruff check . --fix
poetry run mypy .
```

## Project Structure
```
backend/
  app/
    main.py              # FastAPI application
    core/                # Core configuration
    db/                  # Database session and base
    models/              # SQLAlchemy models
    schemas/             # Pydantic schemas
    api/                 # API routes
      deps.py            # Dependencies
      routers/           # Route handlers
    services/            # Business logic
    tasks/               # Background jobs
  tests/                 # Test suite
  alembic/               # Database migrations
```

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
