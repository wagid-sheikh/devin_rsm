
# TSV-RSM — Full-Code Delivery Plan (Based on SRS-v5)

This plan ensures FULL backend & frontend code delivery with zero placeholders, validated against a living SRS Compliance Matrix and enforced by CI test gates.

## Guardrails
1. SRS Compliance Matrix — every capability maps to OpenAPI paths, DB entities/migrations, E2E scenarios, observability, and tests.
2. Contract-first OpenAPI — the spec is the single source of truth for FE + BE.
3. Definition of Done (DoD) per row:
   - Code + migrations + seed
   - OpenAPI docs
   - Unit + contract + E2E tests
   - Lint/typing clean (ruff/mypy)
4. CI gates — ruff, mypy, pytest, schemathesis, (Playwright later).
5. Versioned data shape — Alembic migrations + fixtures.

## Delivery Batches (no stubs inside a batch)
A. Platform Core — Tenancy, Auth, Users/Roles/RBAC, Config, Logging/Metrics.
B. Commercial Core — Items & Rates, Customers & Addresses, Orders (with tags), Pricing.
C. Billing — Invoices & Lines, Payments, Packages, Tax calc.
D. Ops — Logistics (pickup/drop, rider payout), Closing, Documents, Expenses.
E. Finance & QA — Bank Import + Recon, Franchise Imports, Claims & Feedback, Exports (XLSX/PDF).
F. Frontends — Admin Web (React+Vite+Tailwind+shadcn) with Playwright tests.

Each batch is independently shippable with all DoD boxes ticked.
