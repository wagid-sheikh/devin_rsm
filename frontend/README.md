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
