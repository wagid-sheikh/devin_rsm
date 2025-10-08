# TSV-RSM - Retail Store Management System

Multi-tenant, mobile-first web billing system for laundry/dry-cleaning retail and B2B operations.

## Project Structure

- `/backend` - FastAPI backend (Python 3.11+)
- `/frontend` - React frontend (Vite + TypeScript)
- `/development-roadmap.md` - Detailed session-by-session development plan
- `/SRS-v5.md` - Software Requirements Specification

## Quick Start

### Backend
```bash
cd backend
poetry install
cp .env.example .env
# Configure .env with database credentials
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
pnpm install
cp .env.example .env
pnpm dev
```

## Documentation

- Backend API: http://localhost:8000/docs
- Frontend: http://localhost:5173
- Development Roadmap: [development-roadmap.md](./development-roadmap.md)
- Requirements: [SRS-v5.md](./SRS-v5.md)

## Tech Stack

### Backend
- FastAPI (Python 3.11+)
- PostgreSQL 15+ (AsyncPG)
- SQLAlchemy 2.0 (Async ORM)
- Alembic (migrations)
- 100% async

### Frontend
- React 18 + TypeScript
- Vite
- TanStack Query
- React Router
- Tailwind CSS
- Zod validation

## Development

See [development-roadmap.md](./development-roadmap.md) for the complete development plan across 65-75 sessions.

Current Progress: Phase 0, Session 0.1 ✅
