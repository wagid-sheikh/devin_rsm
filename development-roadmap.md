# TSV-RSM Development Roadmap

**Project:** TSV-RSM — Mobile-First Web Retail Store Billing System  
**Generated:** October 8, 2025  
**Based on:** SRS-v5.md  
**Approach:** Iterative, session-based development with testing at each milestone

---

## 📋 Executive Summary

This roadmap breaks down the TSV-RSM project into **manageable 2-3 hour sessions** across **8 phases**. Each session is independently testable, builds on previous work, and delivers incremental value.

**Total Estimated Sessions:** ~65-75 sessions  
**Recommended Schedule:** 2-3 sessions per week  
**Estimated Timeline:** 6-9 months for Phase 1 completion

---

## 🎯 Development Principles

1. **Test-Driven:** Every session includes testing before completion
2. **Incremental:** Each session adds working, tested functionality
3. **Branch-Based:** All work done in feature branches with PR reviews
4. **Documentation-First:** OpenAPI specs and SDK generation drive FE/BE sync
5. **Production-Ready:** Follow all NFRs (security, performance, async-only)

---

## 📦 Phase 0: Foundation & Infrastructure (Sessions 1-8)

### Session 0.1: Repository Setup & Project Structure
**Duration:** 2-3 hours  
**Goal:** Initialize backend and frontend repositories with proper structure

**Tasks:**
- Create backend directory structure (FastAPI + Poetry)
- Set up pyproject.toml with all core dependencies (FastAPI, SQLAlchemy async, asyncpg, Alembic, pydantic-settings)
- Create frontend directory structure (Vite + React + TypeScript)
- Set up package.json with core dependencies (React Router, TanStack Query, Zod, shadcn/ui)
- Configure .gitignore for both projects
- Create initial README files
- Set up pre-commit hooks (ruff, mypy for backend; eslint for frontend)

**Deliverables:**
- Clean directory structure
- Package manifests with all dependencies
- Pre-commit hooks configured

**Testing:**
- Verify project installs successfully
- Run linters (should pass on empty project)

---

### Session 0.2: Database Setup & Core Configuration
**Duration:** 2-3 hours  
**Goal:** Configure PostgreSQL connection and environment management

**Tasks:**
- Create Pydantic Settings class (database URL, JWT secrets, CORS origins)
- Set up async SQLAlchemy engine + session management
- Configure Alembic for migrations
- Create .env.example files
- Set up logging configuration (JSON structured logging)
- Create health and ready endpoints

**Deliverables:**
- `app/core/config.py` with Settings
- `app/db/session.py` with async DB session
- `alembic.ini` and initial migration structure
- `/health` and `/ready` endpoints

**Testing:**
- Verify database connection works
- Test health endpoints return 200

---

### Session 0.3: Authentication Foundation
**Duration:** 2-3 hours  
**Goal:** Implement OAuth2 JWT authentication system

**Tasks:**
- Create User model (id, email, phone, password_hash, first_name, last_name, status)
- Implement password hashing (bcrypt)
- Create JWT access + refresh token logic (15m access, 7d refresh)
- Build `/auth/login`, `/auth/refresh`, `/auth/logout` endpoints
- Implement token revocation list (Redis or DB)
- Create authentication dependencies for protected routes

**Deliverables:**
- User model and migration
- Auth router with login/logout/refresh
- JWT token utilities
- Auth dependency for route protection

**Testing:**
- Test login with valid/invalid credentials
- Verify token expiration
- Test refresh token flow
- Test logout invalidates tokens

---

### Session 0.4: RBAC Foundation (Roles & Permissions)
**Duration:** 2-3 hours  
**Goal:** Implement Role-Based Access Control foundation

**Tasks:**
- Create Role model (code, name, description)
- Create UserRole model (many-to-many)
- Seed default roles (PlatformAdmin, CompanyAdmin, AreaManager, StoreManager, Staff, Accountant, B2BSales)
- Create RBAC permission decorators/dependencies
- Implement `/me` endpoint (current user with roles)

**Deliverables:**
- Role and UserRole models + migrations
- Seed data for default roles
- RBAC decorators for route protection
- `/me` endpoint

**Testing:**
- Verify roles are seeded correctly
- Test role assignment to users
- Test `/me` returns user with roles
- Verify RBAC decorator blocks unauthorized access

---

### Session 0.5: Multi-Tenancy Foundation (Companies & Stores)
**Duration:** 2-3 hours  
**Goal:** Implement core multi-tenant structure

**Tasks:**
- Create Company model (legal_name, trade_name, gstin, pan, contacts)
- Create Store model (company_id, name, address, is_franchise, status, timezone, invoice_series_prefix)
- Create UserStoreAccess model (user_id, store_id, scope)
- Add tenant isolation middleware (inject company_id filter)
- Implement `/companies` and `/stores` CRUD endpoints (admin only)

**Deliverables:**
- Company and Store models + migrations
- Tenant isolation middleware
- Company and Store CRUD APIs
- UserStoreAccess model

**Testing:**
- Create companies and stores
- Verify tenant isolation (users only see their company data)
- Test store access control

---

### Session 0.6: Frontend Foundation (Auth & Dashboard Shell)
**Duration:** 2-3 hours  
**Goal:** Set up React app with authentication and routing

**Tasks:**
- Configure React Router with protected routes
- Set up TanStack Query client
- Create login page with form validation (Zod)
- Implement auth context (token storage, logout)
- Create dashboard shell with navigation menu
- Integrate logo (Secondary-White-Logo 3-01.png)
- Set up dark theme with toggle

**Deliverables:**
- Login page with working authentication
- Protected dashboard route
- Navigation shell
- Logo integrated
- Dark theme

**Testing:**
- Test login flow end-to-end
- Verify protected routes redirect to login
- Test logout clears session
- Verify theme toggle works

---

### Session 0.7: OpenAPI SDK Generation Pipeline
**Duration:** 2-3 hours  
**Goal:** Set up automated TypeScript SDK generation from OpenAPI

**Tasks:**
- Configure FastAPI OpenAPI export
- Set up openapi-typescript-codegen or similar
- Create backend CI workflow to publish OpenAPI spec
- Create npm package structure for SDK (@tsvcrm/api-types)
- Generate initial SDK from auth endpoints
- Configure frontend to use generated SDK

**Deliverables:**
- OpenAPI spec auto-generated
- SDK package with types and client
- Frontend using generated SDK for auth
- CI workflow for SDK publishing

**Testing:**
- Verify OpenAPI spec is generated correctly
- Test generated SDK works in frontend
- Verify type safety in frontend

---

### Session 0.8: CI/CD Foundation
**Duration:** 2-3 hours  
**Goal:** Set up automated testing and deployment workflows

**Tasks:**
- Create backend-ci.yml (lint → typecheck → pytest → async guard)
- Create frontend-ci.yml (lint → typecheck → vitest → build)
- Set up pytest with async support
- Create vitest configuration
- Add async guard script (fails if sync routes detected)
- Configure coverage reporting

**Deliverables:**
- GitHub Actions workflows
- Test frameworks configured
- Async guard in place
- Coverage reporting

**Testing:**
- Push code and verify CI runs
- Verify async guard catches sync routes
- Check coverage reports generate

---

## 📚 Phase 1: Master Data Management (Sessions 1.1-1.8)

### Session 1.1: Cost Centers Master
**Duration:** 2-3 hours  
**Goal:** Implement cost center management

**Tasks:**
- Create CostCenter model (code unique, name, active)
- Create CompanyCostCenter model (company_id, cost_center_id, is_default)
- Seed default cost centers (UN3668, KN3817, SC3567, SL1610, TSV001)
- Implement `/cost-centers` CRUD endpoints
- Create CompanyCostCenter assignment API
- Build frontend pages for cost center management

**Deliverables:**
- CostCenter models + migrations
- Seed data
- Backend APIs
- Frontend CRUD pages

**Testing:**
- Test CRUD operations
- Verify company-specific cost center assignment
- Test default cost center logic

---

### Session 1.2: Users & Role Management UI
**Duration:** 2-3 hours  
**Goal:** Build user management interface

**Tasks:**
- Create `/users` CRUD endpoints
- Implement `/users/{id}/roles` assignment endpoint
- Build Users list page with search/filter
- Create User create/edit forms
- Add role assignment interface
- Implement user status toggle (active/inactive)

**Deliverables:**
- User CRUD APIs
- Role assignment API
- User management UI

**Testing:**
- Test user creation with role assignment
- Verify search and filters work
- Test status changes

---

### Session 1.3: Store Access Control
**Duration:** 2-3 hours  
**Goal:** Implement store-level access control

**Tasks:**
- Implement `/users/{id}/stores` assignment endpoint
- Create StoreAccess management UI
- Add scope validation (view/edit/approve)
- Create store selector component for multi-store users
- Implement store context in frontend

**Deliverables:**
- Store access APIs
- Store assignment UI
- Store selector component
- Store context

**Testing:**
- Test store assignment to users
- Verify scope-based permissions
- Test multi-store user experience

---

### Session 1.4: Customer Master (Part 1: Basic CRUD)
**Duration:** 2-3 hours  
**Goal:** Implement customer management foundation

**Tasks:**
- Create Customer model (company_id, code, name, phone_primary, email, notes, status)
- Create CustomerContact model (customer_id, contact_person, phone, email, is_primary)
- Create CustomerAddress model (customer_id, type, address, is_pickup_default, is_delivery_default)
- Implement `/customers` CRUD endpoints
- Build customer list page with search

**Deliverables:**
- Customer models + migrations
- Customer CRUD APIs
- Customer list UI

**Testing:**
- Test customer creation
- Verify multi-tenant isolation
- Test search functionality

---

### Session 1.5: Customer Master (Part 2: Contacts & Addresses)
**Duration:** 2-3 hours  
**Goal:** Complete customer management with contacts and addresses

**Tasks:**
- Implement `/customers/{id}/contacts` endpoints
- Implement `/customers/{id}/addresses` endpoints
- Build customer detail page
- Create contact and address management UI
- Add default contact/address selection

**Deliverables:**
- Contact and address APIs
- Customer detail page
- Contact/address management UI

**Testing:**
- Test adding multiple contacts
- Test adding multiple addresses
- Verify default selection works

---

### Session 1.6: Item Master & Service Types
**Duration:** 2-3 hours  
**Goal:** Implement item catalog and service types

**Tasks:**
- Create Item model (company_id, sku, name, type, hsn_sac, uom, tax_rate)
- Create ServiceType model (code, name, description, active)
- Seed service types (Wash & Fold, Premium Wash, Premium Wash & Iron, Iron, Dry Cleaning)
- Implement `/items` CRUD endpoints
- Build item management UI

**Deliverables:**
- Item and ServiceType models + migrations
- Service type seed data
- Item CRUD APIs and UI

**Testing:**
- Test item creation
- Verify service types are seeded
- Test item listing and search

---

### Session 1.7: Pricing & Rate Management (Part 1: Company Base Rates)
**Duration:** 2-3 hours  
**Goal:** Implement company-level pricing

**Tasks:**
- Create ItemRate model (company_id, item_id, rate_type, customer_id?, price, effective_from, effective_to)
- Implement `/rates` CRUD endpoints for company base rates
- Create pricing service to resolve effective rate
- Build rate management UI

**Deliverables:**
- ItemRate model + migration
- Rate CRUD APIs
- Pricing resolution service
- Rate management UI

**Testing:**
- Test company base rate creation
- Verify effective date logic
- Test rate resolution service

---

### Session 1.8: Pricing & Rate Management (Part 2: Customer Overrides)
**Duration:** 2-3 hours  
**Goal:** Implement customer-specific pricing overrides

**Tasks:**
- Implement customer rate override APIs
- Create `/pricing/resolve` endpoint (item_id, customer_id, date → resolved price)
- Build customer rate override UI
- Add rate preview in customer detail

**Deliverables:**
- Customer override APIs
- Price resolution endpoint
- Customer pricing UI

**Testing:**
- Test customer override creation
- Verify override takes precedence over base rate
- Test price resolution with effective dates

---

## 🛒 Phase 2: Order Management (Sessions 2.1-2.6)

### Session 2.1: Order Foundation (Basic Order Creation)
**Duration:** 2-3 hours  
**Goal:** Implement basic order creation

**Tasks:**
- Create Order model (store_id, customer_id, order_no, order_date, status, notes)
- Create OrderItem model (order_id, item_id, service_type, qty, unit_price, line_amount, remarks)
- Implement order number generation (per store)
- Create `/orders` POST endpoint
- Build order creation form

**Deliverables:**
- Order models + migrations
- Order creation API
- Order creation UI

**Testing:**
- Test order creation with items
- Verify order numbering
- Test price snapshot on order items

---

### Session 2.2: Order CRUD & Listing
**Duration:** 2-3 hours  
**Goal:** Complete order management

**Tasks:**
- Implement `/orders` GET (list with filters), GET /{id}, PUT, DELETE
- Add order status management
- Create order list page with filters (date, customer, status)
- Build order detail/edit page
- Add pickup/delivery address selection

**Deliverables:**
- Order CRUD APIs
- Order list and detail UI
- Status management

**Testing:**
- Test order listing with filters
- Test order updates
- Verify address selection works

---

### Session 2.3: Order Tags & Article Tracking
**Duration:** 2-3 hours  
**Goal:** Implement order tagging and article tracking

**Tasks:**
- Create OrderTag model (order_id, tag_code, note)
- Create OrderArticle model (order_id, article_tag_code, item_id, service_type_id, qc_result, notes)
- Implement `/orders/{id}/tags` endpoints
- Implement article tracking APIs
- Build tag management UI
- Create article list/add UI

**Deliverables:**
- Tag and article models + migrations
- Tag and article APIs
- Tag and article management UI

**Testing:**
- Test tag creation
- Test article tracking
- Verify article-level data

---

### Session 2.4: Order Process Workflow (Stages a-k)
**Duration:** 2-3 hours  
**Goal:** Implement order stage progression

**Tasks:**
- Create OrderStageEvent model (order_id, stage_code, occurred_at, user_id, note)
- Implement stage progression logic (11 stages from SRS §23)
- Create `/orders/{id}/advance-stage` endpoint with idempotency
- Add stage validation (sequential enforcement)
- Build stage progression UI

**Deliverables:**
- OrderStageEvent model + migration
- Stage progression APIs
- Stage enforcement logic
- Stage UI

**Testing:**
- Test stage progression
- Verify sequential enforcement
- Test idempotency

---

### Session 2.5: Pre/Post QC Photo Upload
**Duration:** 2-3 hours  
**Goal:** Implement QC photo management

**Tasks:**
- Set up S3-compatible storage adapter
- Create document upload service
- Implement `/orders/{id}/upload-pre-qc-photos` endpoint (ZIP)
- Implement `/orders/{id}/upload-post-qc-photos` endpoint (ZIP)
- Link photos to articles
- Build photo upload UI
- Create photo viewer

**Deliverables:**
- Storage adapter
- Photo upload APIs
- Photo upload and viewer UI

**Testing:**
- Test ZIP upload
- Verify photo storage
- Test photo viewing

---

### Session 2.6: Order Export (PDF)
**Duration:** 2-3 hours  
**Goal:** Implement order PDF export

**Tasks:**
- Set up PDF generation library (reportlab or weasyprint)
- Create order PDF template
- Implement `/orders/export.pdf?ids=...` endpoint
- Add batch export functionality
- Create export UI (select multiple orders)

**Deliverables:**
- PDF generation service
- Order PDF template
- Export endpoint
- Export UI

**Testing:**
- Test single order PDF
- Test batch export
- Verify PDF formatting

---

## 💰 Phase 3: Invoicing & Payments (Sessions 3.1-3.5)

### Session 3.1: Invoice Generation from Orders
**Duration:** 2-3 hours  
**Goal:** Implement invoice creation from orders

**Tasks:**
- Create Invoice model (store_id, customer_id, invoice_no, invoice_date, status, subtotal, tax_total, discount_total, grand_total, package_applied_total)
- Create InvoiceLine model (invoice_id, order_item_id, item_id, qty, price, tax_rate, line_tax, line_total)
- Implement `/invoices/from-orders` POST endpoint
- Add invoice number generation (per store series)
- Create invoice generation logic with tax calculation
- Build invoice creation UI

**Deliverables:**
- Invoice models + migrations
- Invoice generation API
- Invoice numbering
- Invoice creation UI

**Testing:**
- Test invoice generation from orders
- Verify tax calculations
- Test invoice numbering

---

### Session 3.2: Invoice Posting & Status Management
**Duration:** 2-3 hours  
**Goal:** Implement invoice lifecycle management

**Tasks:**
- Implement `/invoices/{id}/post` endpoint (draft → posted)
- Add invoice cancellation logic
- Create invoice status transitions
- Build invoice list page with filters
- Create invoice detail page

**Deliverables:**
- Invoice posting API
- Status management
- Invoice list and detail UI

**Testing:**
- Test invoice posting
- Test cancellation
- Verify status transitions

---

### Session 3.3: Payment Recording (Cash/UPI/Card)
**Duration:** 2-3 hours  
**Goal:** Implement payment recording

**Tasks:**
- Create Payment model (invoice_id, mode, amount, txn_ref, notes)
- Implement `/payments` POST endpoint
- Add payment validation (amount ≤ invoice balance)
- Create payment recording UI
- Add payment history view

**Deliverables:**
- Payment model + migration
- Payment recording API
- Payment UI

**Testing:**
- Test payment recording
- Verify payment modes
- Test overpayment prevention

---

### Session 3.4: Package System (Prepaid Balances)
**Duration:** 2-3 hours  
**Goal:** Implement customer package management

**Tasks:**
- Create Package model (customer_id, name, signup_date, value, balance, status)
- Create PackageTxn model (package_id, type, amount, ref_invoice_id, note)
- Implement `/packages` CRUD endpoints
- Add package balance check and debit logic
- Integrate package debit in invoice posting
- Build package management UI

**Deliverables:**
- Package models + migrations
- Package CRUD APIs
- Package debit logic
- Package UI

**Testing:**
- Test package creation
- Test package debit on invoice
- Verify negative balance prevention

---

### Session 3.5: Payment & Invoice Export (CSV/XLSX/PDF)
**Duration:** 2-3 hours  
**Goal:** Implement payment and invoice exports

**Tasks:**
- Implement `/payments/export.{csv|xlsx|pdf}` endpoints
- Implement `/invoices/export.pdf?ids=...` endpoint
- Create invoice PDF template
- Build export UI with filters
- Add async job support for large exports

**Deliverables:**
- Export endpoints
- PDF templates
- Export UI
- Async job handling

**Testing:**
- Test CSV/XLSX exports
- Test PDF invoice generation
- Test large exports

---

## 🚚 Phase 4: Logistics & Pickup/Drop (Sessions 4.1-4.3)

### Session 4.1: Pickup/Drop Recording
**Duration:** 2-3 hours  
**Goal:** Implement pickup and delivery tracking

**Tasks:**
- Create PickupDrop model (order_id, type, rider_id, scheduled_at, arrived_at, completed_at, distance_km, geo_start, geo_end, payout_amount)
- Implement `/logistics/assign` endpoint
- Add distance calculation (haversine formula)
- Create pickup/drop recording APIs
- Build logistics management UI

**Deliverables:**
- PickupDrop model + migration
- Logistics APIs
- Distance calculation
- Logistics UI

**Testing:**
- Test pickup assignment
- Test delivery recording
- Verify distance calculation

---

### Session 4.2: Rider Management & Payout Calculation
**Duration:** 2-3 hours  
**Goal:** Implement rider tracking and payout logic

**Tasks:**
- Add rider role to User model
- Implement vehicle type tracking (fuel/EV)
- Create payout calculation service (Rs. 3/km fuel, Rs. 2/km EV)
- Implement `/logistics/settle/{id}` endpoint
- Build rider payout UI
- Create rider settlement summary

**Deliverables:**
- Rider management
- Payout calculation
- Settlement APIs
- Rider payout UI

**Testing:**
- Test rider assignment
- Verify payout calculations
- Test settlement process

---

### Session 4.3: Delivery Modes & Proof of Delivery
**Duration:** 2-3 hours  
**Goal:** Complete delivery workflow

**Tasks:**
- Create OrderDelivery model (order_id, mode, rider_id, delivered_at, delivered_by_user_id, delivery_address_id, proof_doc_id)
- Implement delivery mode selection (customer_pickup vs store_drop)
- Add proof of delivery upload (photo/signature)
- Integrate with order stage progression
- Build delivery completion UI

**Deliverables:**
- OrderDelivery model + migration
- Delivery mode selection
- PoD upload
- Delivery UI

**Testing:**
- Test both delivery modes
- Test PoD upload
- Verify order status updates

---

## 💼 Phase 5: Finance & HR (Sessions 5.1-5.8)

### Session 5.1: Expense Management (Part 1: CRUD)
**Duration:** 2-3 hours  
**Goal:** Implement expense recording

**Tasks:**
- Create Expense model (company_id, store_id, category, is_recurring, vendor, bill_no, amount, tax_amount, date, status, payment_screenshot_url)
- Implement `/expenses` CRUD endpoints
- Add expense categories
- Create expense entry form
- Build expense list page

**Deliverables:**
- Expense model + migration
- Expense CRUD APIs
- Expense UI

**Testing:**
- Test expense creation
- Test recurring flag
- Verify multi-tenant isolation

---

### Session 5.2: Expense Management (Part 2: Approval & Payment)
**Duration:** 2-3 hours  
**Goal:** Complete expense workflow

**Tasks:**
- Implement expense approval workflow
- Add `/expenses/{id}/approve` endpoint
- Implement `/expenses/{id}/mark-paid` endpoint
- Add payment screenshot upload
- Build approval and payment UI

**Deliverables:**
- Approval workflow
- Payment tracking
- Approval UI

**Testing:**
- Test approval flow
- Test payment marking
- Verify RBAC for approvals

---

### Session 5.3: Document Management & Central Repository
**Duration:** 2-3 hours  
**Goal:** Implement centralized document store

**Tasks:**
- Create Document model (company_id, store_id, entity_type, entity_id, file_url, mime_type, tags, visibility_role_min, download_count)
- Create DocumentDownloadLog model (document_id, user_id, downloaded_at, ip)
- Implement `/documents` upload/list/download endpoints
- Add presigned URL generation
- Build document management UI
- Create download logging

**Deliverables:**
- Document models + migrations
- Document APIs
- Presigned URLs
- Document UI
- Download logging

**Testing:**
- Test document upload
- Test presigned downloads
- Verify download logging
- Test role-based visibility

---

### Session 5.4: Attendance Management (Clock In/Out)
**Duration:** 2-3 hours  
**Goal:** Implement attendance tracking

**Tasks:**
- Create Attendance model (user_id, store_id, clock_in_at, clock_in_geo, clock_out_at, clock_out_geo, status)
- Implement `/attendance/clock-in` endpoint
- Implement `/attendance/clock-out` endpoint
- Add geo-tracking
- Create attendance UI (mobile-friendly)
- Build attendance list/report

**Deliverables:**
- Attendance model + migration
- Clock in/out APIs
- Geo-tracking
- Attendance UI

**Testing:**
- Test clock in/out flow
- Verify geo coordinates
- Test missing clock-out handling

---

### Session 5.5: Weekly Off & Leave Management
**Duration:** 2-3 hours  
**Goal:** Implement weekly off and leave tracking

**Tasks:**
- Create WeeklyOff model (user_id, weekday)
- Create Leave model (user_id, start_date, end_date, type, status)
- Implement weekly off validation (one per week, no Fri/Sat/Sun)
- Implement `/weekly-off` and `/leave` CRUD endpoints
- Build weekly off and leave management UI

**Deliverables:**
- WeeklyOff and Leave models + migrations
- Weekly off validation
- Leave APIs
- UI for both

**Testing:**
- Test weekly off validation
- Test leave request flow
- Verify Fri/Sat/Sun restriction

---

### Session 5.6: Reimbursements
**Duration:** 2-3 hours  
**Goal:** Implement employee reimbursement tracking

**Tasks:**
- Create Reimburse model (user_id, date, category, amount, status, receipt_doc_id)
- Implement `/reimburse` CRUD endpoints
- Add approval workflow
- Link to document repository for receipts
- Build reimbursement UI

**Deliverables:**
- Reimburse model + migration
- Reimbursement APIs
- Approval workflow
- Reimbursement UI

**Testing:**
- Test reimbursement submission
- Test approval flow
- Verify receipt attachment

---

### Session 5.7: Payroll Calculation (Indian Retail Standards)
**Duration:** 2-3 hours  
**Goal:** Implement payroll calculation engine

**Tasks:**
- Create Payroll model (company_id, period_month, employee_id, earnings_total, deductions_total, net_pay, status)
- Create PayrollComponent model (payroll_id, type, code, amount)
- Implement payroll calculation service (Basic, HRA, Special Allowance, PF, ESI, PT, TDS)
- Create `/payroll/run` endpoint
- Integrate attendance, leaves, weekly offs
- Build payroll calculation UI

**Deliverables:**
- Payroll models + migrations
- Payroll calculation engine
- Indian retail standards implementation
- Payroll UI

**Testing:**
- Test payroll calculation
- Verify component calculations
- Test attendance integration

---

### Session 5.8: Staff Penalties & Recoveries
**Duration:** 2-3 hours  
**Goal:** Implement staff adjustment tracking

**Tasks:**
- Create StaffAdjustment model (user_id, date, type, reason_code, amount, status, payroll_component_id)
- Implement `/staff-adjustments` CRUD endpoints
- Add approval workflow
- Integrate with payroll deductions
- Add net pay negative prevention
- Build staff adjustment UI

**Deliverables:**
- StaffAdjustment model + migration
- Adjustment APIs
- Payroll integration
- Adjustment UI

**Testing:**
- Test penalty creation
- Test recovery recording
- Verify payroll integration
- Test net pay protection

---

## 📱 Phase 6: WhatsApp & Messaging (Sessions 6.1-6.3)

### Session 6.1: WhatsApp Template Management
**Duration:** 2-3 hours  
**Goal:** Implement WhatsApp template system

**Tasks:**
- Create WhatsAppTemplate model (company_id, code, body, vars, type, is_active)
- Seed default templates (feedback, promo)
- Implement `/whatsapp/templates` CRUD endpoints
- Build template management UI
- Add variable substitution preview

**Deliverables:**
- WhatsAppTemplate model + migration
- Template seed data
- Template CRUD APIs
- Template UI

**Testing:**
- Test template creation
- Test variable substitution
- Verify template activation

---

### Session 6.2: WhatsApp Integration & Message Sending
**Duration:** 2-3 hours  
**Goal:** Implement custom WhatsApp integration

**Tasks:**
- Create MessageLog model (company_id, to_phone, template_code, body_rendered, context, status, provider_msg_id, error)
- Implement WhatsApp provider adapter (based on SRS specs)
- Create `/whatsapp/send-feedback` endpoint (post-delivery)
- Implement message queue (async job)
- Add retry logic
- Build message log viewer

**Deliverables:**
- MessageLog model + migration
- WhatsApp adapter
- Send feedback API
- Async message queue
- Message log UI

**Testing:**
- Test feedback sending
- Verify message queuing
- Test retry logic
- Check message status updates

---

### Session 6.3: WhatsApp Broadcasts & Opt-Out
**Duration:** 2-3 hours  
**Goal:** Implement promotional broadcasts

**Tasks:**
- Implement `/whatsapp/broadcast` endpoint
- Add opt-out management
- Implement frequency cap (1 promo/week/recipient)
- Add campaign tracking
- Build broadcast UI
- Create opt-out management UI

**Deliverables:**
- Broadcast API
- Opt-out tracking
- Frequency cap enforcement
- Broadcast UI

**Testing:**
- Test broadcast creation
- Verify frequency cap
- Test opt-out functionality

---

## 🏦 Phase 7: Banking & Reconciliation (Sessions 7.1-7.4)

### Session 7.1: Bank Statement Import
**Duration:** 2-3 hours  
**Goal:** Implement bank statement upload

**Tasks:**
- Create BankImportFile model (company_id, filename, source_bank, statement_date_from, statement_date_to, status)
- Create BankTxn model (company_id, import_file_id, posted_at, value_date, amount, direction, description, utr_ref, account_last4, raw)
- Implement `/recon/import` endpoint (CSV/XLSX)
- Add file parsing logic
- Build import UI

**Deliverables:**
- Bank models + migrations
- Import parser
- Import API
- Import UI

**Testing:**
- Test CSV import
- Test XLSX import
- Verify transaction parsing

---

### Session 7.2: Reconciliation Rules Engine
**Duration:** 2-3 hours  
**Goal:** Implement rule-based matching

**Tasks:**
- Create ReconRule model (company_id, name, match_type, pattern, map_to, field, priority, active)
- Seed default rules
- Implement rule matching engine
- Create `/recon/rules` CRUD endpoints
- Build rule management UI

**Deliverables:**
- ReconRule model + migration
- Rule seed data
- Matching engine
- Rule CRUD APIs
- Rule UI

**Testing:**
- Test rule matching (exact, contains, regex)
- Test priority ordering
- Verify rule activation

---

### Session 7.3: Auto & Manual Matching
**Duration:** 2-3 hours  
**Goal:** Complete reconciliation workflow

**Tasks:**
- Create ReconMatch model (bank_txn_id, entity_type, entity_id, confidence, status, note)
- Implement `/recon/auto-match` endpoint
- Implement `/recon/manual-match` endpoint
- Add conflict detection
- Build matching UI
- Create match review interface

**Deliverables:**
- ReconMatch model + migration
- Auto-match API
- Manual match API
- Matching UI

**Testing:**
- Test auto-matching
- Test manual matching
- Verify conflict handling

---

### Session 7.4: Reconciliation Summary & Reports
**Duration:** 2-3 hours  
**Goal:** Implement reconciliation reporting

**Tasks:**
- Implement `/recon/summary` endpoint
- Create reconciliation dashboard
- Add match statistics
- Build unmatched transactions report
- Create reconciliation audit trail

**Deliverables:**
- Summary API
- Reconciliation dashboard
- Reports
- Audit trail

**Testing:**
- Test summary calculation
- Verify dashboard data
- Test report generation

---

## 🏢 Phase 8: Franchise, Claims & Analytics (Sessions 8.1-8.10)

### Session 8.1: Franchise Source Configuration
**Duration:** 2-3 hours  
**Goal:** Implement franchise import setup

**Tasks:**
- Create FranchiseSource model (company_id, name, format, mapping_json, active)
- Create adapters for TumbleDry, UClean, Other
- Implement `/franchise/sources` CRUD endpoints
- Build source configuration UI
- Add mapping JSON editor

**Deliverables:**
- FranchiseSource model + migration
- Adapter framework
- Source CRUD APIs
- Configuration UI

**Testing:**
- Test source creation
- Test mapping configuration
- Verify adapter selection

---

### Session 8.2: Franchise Sales Import
**Duration:** 2-3 hours  
**Goal:** Implement franchise sales data import

**Tasks:**
- Create FranchiseSalesImport model (company_id, source_id, filename, period_month, status, rows_total, rows_ok, rows_failed)
- Create FranchiseSalesRow model (import_id, store_hint, date, gross, net, tax, notes)
- Implement `/franchise/import` endpoint
- Add file parsing and validation
- Build import UI

**Deliverables:**
- Import models + migrations
- Import parser
- Import API
- Import UI

**Testing:**
- Test file upload
- Test parsing logic
- Verify error row capture

---

### Session 8.3: Franchise Import Review & Commit
**Duration:** 2-3 hours  
**Goal:** Complete franchise import workflow

**Tasks:**
- Implement `/franchise/import/{id}/review` endpoint
- Implement `/franchise/import/{id}/commit` endpoint
- Add idempotency (by source + period)
- Build review UI
- Create commit confirmation flow

**Deliverables:**
- Review and commit APIs
- Review UI
- Idempotency handling

**Testing:**
- Test review process
- Test commit operation
- Verify idempotency

---

### Session 8.4: Customer Claims (Compensation & Refunds)
**Duration:** 2-3 hours  
**Goal:** Implement customer claim management

**Tasks:**
- Create CustomerClaim model (order_id, customer_id, article_tag_code, reason_code, description, claim_type, amount_claimed, amount_approved, status, settlement_method, settlement_ref_id)
- Implement `/claims` CRUD endpoints
- Add approval workflow
- Link to QC failures
- Build claim management UI

**Deliverables:**
- CustomerClaim model + migration
- Claim CRUD APIs
- Approval workflow
- Claim UI

**Testing:**
- Test claim creation
- Test approval flow
- Verify settlement tracking

---

### Session 8.5: Daily Store Closing (Part 1: Preview & Variance)
**Duration:** 2-3 hours  
**Goal:** Implement daily closing preview

**Tasks:**
- Create DailyStoreClose model (company_id, store_id, close_date, cutoff_time_local, cash_opening_float, cash_from_sales, cash_petty_expense, cash_deposit_bank, cash_closing_expected, cash_counted, variance, digital_receipts_total, notes, status, closed_by, closed_at)
- Implement `/closing/preview` endpoint
- Add variance calculation
- Create cash tally UI
- Build variance report

**Deliverables:**
- DailyStoreClose model + migration
- Preview API
- Variance calculation
- Preview UI

**Testing:**
- Test preview generation
- Verify variance calculation
- Test cash tally

---

### Session 8.6: Daily Store Closing (Part 2: Commit & Lock)
**Duration:** 2-3 hours  
**Goal:** Implement closing commit and day locking

**Tasks:**
- Implement `/closing/commit` endpoint (idempotent)
- Add day lock logic (prevent edits to posted invoices/payments)
- Implement variance threshold approval
- Generate EoD PDF
- Build commit UI with approval flow

**Deliverables:**
- Commit API
- Day lock enforcement
- Approval logic
- EoD PDF generation
- Commit UI

**Testing:**
- Test closing commit
- Verify day lock
- Test variance approval
- Check PDF generation

---

### Session 8.7: Daily Store Closing (Part 3: Reopen & Audit)
**Duration:** 2-3 hours  
**Goal:** Complete closing workflow with reopen

**Tasks:**
- Implement `/closing/{id}/reopen` endpoint
- Add reopen authorization (Area/Company Admin only)
- Implement reopen audit trail
- Build reopen UI
- Create closing history view

**Deliverables:**
- Reopen API
- Authorization check
- Audit trail
- Reopen UI
- History view

**Testing:**
- Test reopen flow
- Verify authorization
- Check audit logging

---

### Session 8.8: Analytics & Reports (Income, Sales, Expenses)
**Duration:** 2-3 hours  
**Goal:** Implement financial reports

**Tasks:**
- Create DailyStoreKPI model (company_id, store_id, date, orders, invoices, sales_gross, sales_net, receipts, new_customers, expenses_total)
- Implement KPI aggregation job
- Create `/reports/income`, `/reports/sales`, `/reports/expenses` endpoints
- Add filters (daily/weekly/monthly/yearly)
- Build report UI with charts

**Deliverables:**
- DailyStoreKPI model + migration
- KPI aggregation
- Report APIs
- Report UI with visualizations

**Testing:**
- Test KPI calculation
- Test report generation
- Verify time period filters

---

### Session 8.9: Role-Based Dashboards (Owner/Area/Store)
**Duration:** 2-3 hours  
**Goal:** Implement role-specific dashboards

**Tasks:**
- Implement `/analytics/owner` endpoint
- Implement `/analytics/area` endpoint
- Implement `/analytics/store` endpoint
- Create dashboard widgets (KPIs, charts, alerts)
- Build role-based dashboard UI

**Deliverables:**
- Analytics APIs
- Dashboard widgets
- Role-based dashboards

**Testing:**
- Test each role's dashboard
- Verify data filtering by role
- Test widget interactions

---

### Session 8.10: Pending Deliveries & Pending Payments Reports
**Duration:** 2-3 hours  
**Goal:** Complete operational reports

**Tasks:**
- Implement `/reports/pending-deliveries` endpoint
- Implement `/reports/pending-payments` endpoint
- Add aging bucket logic
- Create report UI with filters
- Add export functionality

**Deliverables:**
- Report APIs
- Aging logic
- Report UI
- Export functionality

**Testing:**
- Test pending deliveries report
- Test pending payments with aging
- Verify filters and exports

---

## 🔧 Phase 9: Production Readiness (Sessions 9.1-9.5)

### Session 9.1: Rate Limiting & Throttling
**Duration:** 2-3 hours  
**Goal:** Implement comprehensive rate limiting

**Tasks:**
- Set up Redis for rate limiting
- Implement token bucket algorithm
- Add rate limiters per SRS §9 (general, auth, exports, WhatsApp, etc.)
- Create rate limit middleware
- Add 429 response headers

**Deliverables:**
- Redis configuration
- Rate limiting middleware
- All rate limits from SRS

**Testing:**
- Test rate limit enforcement
- Verify 429 responses
- Test rate limit headers

---

### Session 9.2: Logging & Monitoring (Loki/Promtail/Grafana)
**Duration:** 2-3 hours  
**Goal:** Set up centralized logging

**Tasks:**
- Configure JSON structured logging
- Set up Promtail log shipping
- Configure Loki log storage
- Set up Grafana dashboards
- Add correlation IDs
- Implement PII masking

**Deliverables:**
- Structured logging
- Loki/Promtail/Grafana stack
- Dashboards
- PII masking

**Testing:**
- Test log ingestion
- Verify PII masking
- Test dashboard queries

---

### Session 9.3: Health Checks & Metrics
**Duration:** 2-3 hours  
**Goal:** Implement monitoring endpoints

**Tasks:**
- Enhance `/health` and `/ready` endpoints
- Add `/metrics` Prometheus endpoint
- Configure key metrics (latency, error rate, queue depth)
- Set up alerting rules
- Create alert notifications

**Deliverables:**
- Enhanced health checks
- Prometheus metrics
- Alert rules
- Notifications

**Testing:**
- Test health endpoints
- Verify metrics collection
- Test alert triggering

---

### Session 9.4: Security Hardening & Headers
**Duration:** 2-3 hours  
**Goal:** Implement security best practices

**Tasks:**
- Add security headers (HSTS, CSP, X-Frame-Options, Referrer-Policy)
- Implement CORS properly
- Add request validation
- Set up HTTPS only
- Configure session security

**Deliverables:**
- Security headers
- CORS configuration
- Request validation
- HTTPS enforcement

**Testing:**
- Test security headers
- Verify CORS
- Test HTTPS redirect

---

### Session 9.5: Backup & Disaster Recovery
**Duration:** 2-3 hours  
**Goal:** Set up backup and DR procedures

**Tasks:**
- Configure automated PostgreSQL backups
- Set up WAL archiving
- Create backup verification script
- Document restore procedure
- Test DR runbook

**Deliverables:**
- Backup automation
- WAL archiving
- Verification script
- DR documentation

**Testing:**
- Test backup creation
- Test restore process
- Verify backup integrity

---

## 📝 Phase 10: Testing & Documentation (Sessions 10.1-10.4)

### Session 10.1: Unit Test Coverage (Backend)
**Duration:** 2-3 hours  
**Goal:** Achieve 80%+ backend test coverage

**Tasks:**
- Write unit tests for all services
- Test business logic (pricing, payroll, closing, etc.)
- Test validation rules
- Add test fixtures and factories
- Generate coverage report

**Deliverables:**
- Comprehensive test suite
- 80%+ coverage
- Test factories

**Testing:**
- Run full test suite
- Verify coverage report

---

### Session 10.2: API Contract Tests
**Duration:** 2-3 hours  
**Goal:** Implement contract testing

**Tasks:**
- Set up Schemathesis or Dredd
- Create contract tests for all endpoints
- Test OpenAPI spec compliance
- Add schema validation tests
- Integrate into CI

**Deliverables:**
- Contract test suite
- OpenAPI validation
- CI integration

**Testing:**
- Run contract tests
- Verify spec compliance

---

### Session 10.3: E2E Test Suite (Playwright)
**Duration:** 2-3 hours  
**Goal:** Implement end-to-end tests

**Tasks:**
- Set up Playwright
- Write E2E tests for critical flows:
  - Login → Order → Invoice → Payment
  - Closing workflow
  - WhatsApp feedback
  - Reconciliation
- Add visual regression tests
- Integrate into CI

**Deliverables:**
- Playwright configuration
- E2E test suite
- CI integration

**Testing:**
- Run E2E tests
- Verify all flows pass

---

### Session 10.4: Documentation & API Docs
**Duration:** 2-3 hours  
**Goal:** Complete project documentation

**Tasks:**
- Enhance OpenAPI documentation
- Create developer onboarding guide
- Document deployment procedures
- Create user guides
- Document API usage examples

**Deliverables:**
- Complete API documentation
- Developer guide
- Deployment guide
- User documentation

**Testing:**
- Review documentation completeness
- Test following guides as new developer

---

## 🚀 Phase 11: Deployment & Launch (Sessions 11.1-11.3)

### Session 11.1: Production Environment Setup
**Duration:** 2-3 hours  
**Goal:** Set up production infrastructure

**Tasks:**
- Configure production servers
- Set up PostgreSQL production instance
- Configure Redis
- Set up SSL certificates
- Configure environment variables
- Set up monitoring

**Deliverables:**
- Production infrastructure
- SSL certificates
- Environment configuration

**Testing:**
- Test server connectivity
- Verify SSL
- Test database connection

---

### Session 11.2: Production Deployment
**Duration:** 2-3 hours  
**Goal:** Deploy to production

**Tasks:**
- Run production migrations
- Deploy backend
- Deploy frontend
- Configure reverse proxy
- Test production deployment
- Verify all services

**Deliverables:**
- Production deployment
- Running application

**Testing:**
- Smoke test all critical flows
- Verify monitoring
- Test backups

---

### Session 11.3: User Acceptance Testing & Launch
**Duration:** 2-3 hours  
**Goal:** Final UAT and launch

**Tasks:**
- Conduct UAT with stakeholders
- Address any issues found
- Create admin user
- Load seed data
- Official launch
- Monitor initial usage

**Deliverables:**
- UAT sign-off
- Production launch
- Initial user accounts

**Testing:**
- Complete UAT checklist
- Monitor production metrics
- Verify user access

---

## 📊 Summary

**Total Sessions:** ~65-75 sessions  
**Estimated Duration:** 6-9 months at 2-3 sessions/week  
**Phased Approach:** 11 major phases from foundation to launch

### Key Success Factors

1. **Iterative Development:** Each session delivers working, tested functionality
2. **Testing Focus:** Every session includes testing before completion
3. **PR Reviews:** All code reviewed before merge
4. **Incremental Value:** Features usable as they're completed
5. **Flexibility:** Sessions can be reordered within phases as needed

### Next Steps

1. **Review this roadmap** with stakeholders
2. **Start with Phase 0, Session 0.1** - Repository setup
3. **Maintain session log** to track progress
4. **Adjust as needed** based on findings and feedback

---

*Roadmap prepared for TSV-RSM project*  
*Based on SRS-v5.md dated 2025-10-07*  
*Generated: October 8, 2025*
