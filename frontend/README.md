# TSV-RSM Frontend

Multi-tenant Retail Store Management System - Web Application

## Tech Stack
- React 18
- TypeScript
- Vite
- TanStack Query (React Query)
- React Router
- Tailwind CSS
- Zod (validation)
- shadcn/ui

## Setup

### Prerequisites
- Node.js 18+ LTS
- pnpm

### Installation
```bash
# Install dependencies
pnpm install

# Set up environment
cp .env.example .env
# Edit .env with your backend API URL

# Start development server
pnpm dev
```

## Development

### Running Tests
```bash
pnpm test
```

### Linting
```bash
pnpm lint
pnpm lint --fix
```

### Building
```bash
pnpm build
```

## Project Structure
```
frontend/
  src/
    main.tsx           # Entry point
    app/               # App configuration (router, auth, query client)
    components/ui/     # Reusable UI components
    pages/             # Page components
    hooks/             # Custom React hooks
    lib/               # Utilities
    styles/            # Global styles
    tests/             # Test files
```

## Features
- Mobile-first responsive design
- Role-based access control (RBAC)
- Multi-tenant support
- Real-time updates
- Offline support (planned)

## SDK Generation

This project uses automated TypeScript SDK generation from the FastAPI OpenAPI specification.

### Generate SDK Manually

To regenerate the SDK after backend API changes:

```bash
npm run generate:sdk
```

This will:
1. Export the OpenAPI spec from the backend (`backend/openapi.json`)
2. Generate TypeScript types and client in `src/lib/sdk/`

### Automated SDK Updates

The SDK is automatically regenerated via GitHub Actions when backend code changes are pushed to main. The workflow:
- Triggers on changes to `backend/app/**/*.py` or `backend/pyproject.toml`
- Exports the latest OpenAPI specification
- Regenerates the TypeScript SDK
- Creates a pull request with the updated SDK

### Using the SDK

The generated SDK is wrapped in `src/lib/apiClient.ts` for easier usage:

```typescript
import { ApiClient } from '@/lib/apiClient';

// Authentication
const response = await ApiClient.auth.login({ email, password });
const user = await ApiClient.auth.getMe();

// Companies
const companies = await ApiClient.companies.listCompanies();

// Stores
const stores = await ApiClient.stores.listStores();
```

The SDK provides:
- Full TypeScript types for all API requests and responses
- Automatic authentication token handling
- Type-safe error handling with `ApiError`
