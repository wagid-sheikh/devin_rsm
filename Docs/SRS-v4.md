asa


# Software Requirements Specification (Consolidated)

**Project:** TSV-RSM — Mobile-First Web Retail Store Billing System
**Date:** 2025-10-07 10:45:46 (IST)
**Backend:** FastAPI (Python 3.11+) + PostgreSQL 15+ + Alembic (100% **async**)
**Frontend:** React (Vite) + TypeScript (generated SDK from OpenAPI)
**Infra:** Ubuntu servers (DEV/PROD), Docker on server (not on local Mac), GitHub Actions CI/CD, Secrets via Actions (no `.env` in repo)

---

## 0) Executive Intent

Deliver a **multi-tenant**, production-ready platform for laundry/dry-cleaning retail and B2B operations with: masters, **orders → invoices → payments**, rider pickup/drop with distance, expenses, **HR** (attendance → payroll), centralized documents, **WhatsApp** feedback/promotions, **bank reconciliation**, **franchise sales imports**, **reports/dashboards**, and now **Daily Store Closing**. The stack is **100% async**, FE↔BE sync is enforced by OpenAPI-driven **generated TypeScript SDK**, and ops safety is guaranteed via rate limiting, idempotency, and migration policies.

---

## 1) Scope

### 1.1 In Scope (Phase‑1)

- **Masters:** Cost Centers (global; replicated to tenant/store), Tenants/Companies, Stores (franchise vs independent; **targets**), Users, Roles, User↔Role, User↔Store access, Customers (multi-contacts & multi-addresses), Items, Item Rates (company base + customer override), Packages.
- **Operations:** Orders (per piece/kg) + **Order Tags**; **Orders → Invoices (PDF batch)**; Payments (cash/UPI/card/package; CSV/XLSX/PDF export).
- **Logistics:** Pickup/Drop with rider distance & settlement readiness.
- **Finance:** Company & Store expenses (recurring flag; attachments).
- **HR:** Attendance (cutoffs, auto half-day/absent, overrides), **Weekly Off (once/week; not Fri/Sat/Sun)**, Leaves, Reimburse → Payroll.
- **Documents:** Central document store (tags, role-based visibility, **download logs**).
- **Messaging:** WhatsApp feedback (post-delivery) and promotions (provider-agnostic).
- **Bank Reconciliation:** Import statements; rule engine; auto/manual match.
- **Franchise Sales Imports:** Adapters (TumbleDry/UClean/Other) with mapping JSON.
- **Reports & Dashboards:** Income, Sales, Expenses (daily/weekly/monthly/yearly); role dashboards (Owner/Area/Store).
- **Daily Store Closing:** end-of-day lock & variance reporting (see §6.12).
- **Engineering Constraints:** 100% async BE; OpenAPI-first; generated FE SDK; TDD; rate limiting; idempotency; migrations policy; zero-downtime deploy.

### 1.2 Out of Scope (Phase‑1)

Payment gateway settlement (stub only), GST e-invoice/GSP, native mobile apps, advanced ML analytics.

---

## 2) Non-Functional Requirements (NFRs)

- **Performance:** P95 < 300ms for CRUD; big exports as async jobs.
- **Availability:** 99.5% monthly; daily encrypted backups; PITR via WAL.
- **Security:** OAuth2 password flow; JWT access (15m) + rotating refresh (7d, HTTP-only) with revoke list; **RBAC**; tenant isolation; audit logs; headers: HSTS/CSP/Referrer/Frame/Strict-Transport.
- **Privacy/PII:** DPDP-friendly; never log raw credentials/refresh tokens; mask PII in logs.
- **Observability:** JSON logs, correlation id, health/ready endpoints, basic metrics.
- **Accessibility:** WCAG 2.1 AA; mobile-first UX.
- **Storage:** S3-ready adapter (server-side encryption), presigned URLs, lifecycle policies.

---

## 3) Personas & Roles

Platform Admin (SaaS), Company Admin, Area Manager, Store Manager, Staff (Counter/Rider/Wash/Iron), Accountant, B2B Sales, Customer (public invoice link).

**RBAC matrix** in §10.

---

## 4) Data Model (Authoritative)

> Conventions: `id uuid pk`, `company_id` everywhere (tenant scope), `created_at/updated_at timestamptz`, soft-delete via `deleted_at` where useful. Money `numeric(14,2)`; qty `numeric(12,3)`.

### 4.1 Masters

- **cost_center**(code unique, name, active)
- **company**(legal_name, trade_name, gstin, pan, billing_address, contacts…)
- **company_cost_center**(company_id, cost_center_id, is_default)
- **store**(company_id, name, address, gstin_opt, is_franchise, cost_center_id, targets_weekly_json, targets_monthly_json, phone, email, timezone, status, invoice_series_prefix)
- **user**(email unique, phone, password_hash, first_name, last_name, status)
- **role**(code, name) • **user_role**(user_id, role_id) • **user_store_access**(user_id, store_id, scope=view|edit|approve)
- **customer**(company_id, code?, name, phone_primary, email, notes, status) + **customer_contact**, **customer_address**(pickup/delivery defaults)
- **item**(company_id, sku, name, type=service|product, hsn_sac, uom=piece|kg, tax_rate)
- **item_rate**(company_id, item_id, rate_type=company_base|customer_override, customer_id?, price, effective_from, effective_to)

### 4.2 Packages

- **package**(customer_id, name, signup_date, value, balance, status)
- **package_txn**(package_id, type=topup|debit|adjust, amount, ref_invoice_id?, note)

### 4.3 Orders → Invoices → Payments

- **order**(store_id, customer_id, order_no, order_date, status, pickup_address_id?, delivery_address_id?, notes)
- **order_item**(order_id, item_id, service_type, qty, unit_price, line_amount, remarks)
- **order_tag**(order_id, tag_code, note)
- **invoice**(store_id, customer_id, invoice_no, invoice_date, status=draft|posted|cancelled, subtotal, tax_total, discount_total, grand_total, package_applied_total)
- **invoice_line**(invoice_id, order_item_id?, item_id, qty, price, tax_rate, line_tax, line_total)
- **payment**(invoice_id, mode=cash|upi|card|package_adjust, amount, txn_ref, notes)

### 4.4 Pickup/Drop & Rider

- **pickup_drop**(order_id, type=pickup|drop, rider_id, scheduled_at, arrived_at?, completed_at?, distance_km, geo_start, geo_end, payout_amount)

### 4.5 Expenses & Documents

- **expense**(company_id, store_id?, category, is_recurring, vendor, bill_no, amount, tax_amount, date, status=draft|approved|paid, payment_screenshot_url?)
- **document**(company_id, store_id?, entity_type, entity_id, file_url, mime_type, tags[], visibility_role_min, download_count)
- **document_download_log**(document_id, user_id, downloaded_at, ip)

### 4.6 WhatsApp (Provider‑agnostic)

- **whatsapp_template**(company_id, code, body, vars[], type=feedback|promo, is_active)
- **message_log**(company_id, to_phone, template_code?, body_rendered, context(order_id|invoice_id|campaign_id), status=queued|sent|failed, provider_msg_id?, error?)

### 4.7 Bank Reconciliation

- **bank_import_file**(company_id, filename, source_bank, statement_date_from, statement_date_to, status)
- **bank_txn**(company_id, import_file_id, posted_at, value_date, amount, direction=credit|debit, description, utr_ref, account_last4, raw)
- **recon_rule**(company_id, name, match_type=exact|contains|regex, pattern, map_to=invoice|payment|expense, field=utr_ref|description|amount|date, priority, active)
- **recon_match**(bank_txn_id, entity_type, entity_id, confidence, status=auto|manual|discarded, note)

### 4.8 Franchise Sales Imports

- **franchise_source**(company_id, name, format(csv|xlsx), mapping_json, active)
- **franchise_sales_import**(company_id, source_id, filename, period_month, status, rows_total, rows_ok, rows_failed)
- **franchise_sales_row**(import_id, store_hint, date, gross, net, tax, notes)

### 4.9 HR

- **attendance**(user_id, store_id, clock_in_at, clock_in_geo?, clock_out_at?, clock_out_geo?, status)
- **weekly_off**(user_id, weekday)
- **leave**(user_id, start_date, end_date, type, status)
- **reimburse**(user_id, date, category, amount, status, receipt_doc_id?)
- **payroll**(company_id, period_month, employee_id, earnings_total, deductions_total, net_pay, status)
- **payroll_component**(payroll_id, type=earning|deduction, code, amount)

### 4.10 B2B

- **b2b_lead**(company_id, org_name, contact_name, phone, email, stage, notes)
- **b2b_contract**(company_id, customer_id, rate_card_id?, start_date, end_date?, terms)
- **b2b_order** uses `order*` with `is_b2b=true`, `contract_id`

### 4.11 Analytics & Closing

- **daily_store_kpi**(company_id, store_id, date, orders, invoices, sales_gross, sales_net, receipts, new_customers, expenses_total)
- **daily_store_close**(company_id, store_id, close_date, cutoff_time_local, cash_opening_float, cash_from_sales, cash_petty_expense, cash_deposit_bank, cash_closing_expected, cash_counted, variance, digital_receipts_total, notes, status=closed|reopened, closed_by, closed_at, reopened_by?, reopened_at?, reopen_reason?)

---

## 5) Money, Tax & Numbering

- **Rounding:** Decimal math; per-line tax **half‑up**; totals from line sums; no binary float.
- **Invoice numbering:** `invoice_series` per store uses `SELECT … FOR UPDATE` to reserve numbers atomically.
- **Price snapshots:** Persist resolved `unit_price` & `tax_rate` on `order_item` at creation; never recompute retroactively.

---

## 6) Business Rules & Validations

1. **Weekly Off:** exactly one per week; **Fri/Sat/Sun disallowed**.
2. **Attendance:** cutoff & lateness policy; missing clock‑out → auto absent by T+1; manager overrides audited.
3. **Pricing:** resolve customer override (effective) → else company base; **snapshot** on order item.
4. **Packages:** prevent negative balance; atomic decrement on invoice posting; `package_txn` trail.
5. **Invoicing:** unique series per store; line‑tax rounding; grand_total = subtotal + tax − discounts − package.
6. **Logistics:** distance via haversine(geo_start, geo_end); manual override + reason; payout rule (₹/km).
7. **Expenses:** recurring schedule; attachments required above threshold.
8. **Documents:** presigned downloads; **download logs**; min role visibility.
9. **Bank Recon:** rule priority; exact UTR > regex; conflicts → manual; provenance kept.
10. **Franchise Imports:** idempotent by (source, period); mapping JSON; failed rows captured.
11. **WhatsApp:** template vars; 1 feedback/order; promo respects opt‑out.
12. **Daily Store Closing (EoD):**

- Each **store** has a local **cutoff time** (default 23:59, recommend 05:00 local).
- Store Manager runs **/closing**: system compiles cash & digital takings, petty expenses, deposits, rider settlements due, unposted invoices, and package adjustments.
- Manager enters **cash counted**; system computes **variance**. Variance > threshold requires **Area Manager** approval.
- On **Close**: create `daily_store_close` row; lock the day for that store:
  - No edits to **posted invoices/payments** on that date.
  - New back‑dated invoices/payments require approver + audit.
  - Petty cash entries post to next day unless approved.
- **Reopen Day**: Company/Area Manager only, with reason; full audit.
- **Outputs**: EoD PDF (cash summary, digital receipts, petty cash, deposits, variances) and snapshot KPIs.

---

## 7) 100% Async Backend & Jobs

- **Async only:** FastAPI `async def` everywhere; SQLAlchemy **Async ORM** + `asyncpg`; httpx AsyncClient; aiofiles; arq (Redis) for jobs.
- **CI guard:** build fails if any sync route (`def`) is detected; forbid sync DB drivers.
- **Streaming:** exports via `StreamingResponse`; large uploads chunked.
- **Jobs:** 202 + `jobId`; poll `/tasks/{id}`; idempotent handlers; cancel token; DLQ.

---

## 8) API Design & FE/BE Sync

- **OpenAPI** is the contract; **camelCase** JSON; RFC7807 errors; cursor pagination (`limit`, `cursor` → `meta.nextCursor`).
- **Generated SDK:** BE builds and publishes `@tsvcrm/api-types@X.Y.Z` (types + client/hooks). FE imports only this SDK (no hand‑written fetch).
- **Versioning:** `/api/v1`; MAJOR bump for breaking changes; deprecations carry `Sunset` header; FE pinned range.
- **Idempotency:** `Idempotency-Key` header for POST/PUT on payments/imports/broadcasts/closing.
- **Optimistic locking:** `version` column + ETag/`If‑Match` on mutable resources.

**Key Endpoints (representative):**

- **Auth & Users:** `/auth/login`, `/auth/refresh`, `/auth/logout`, `/me`, `/users` CRUD, `/roles`, `/users/{id}/stores`
- **Masters:** `/companies`, `/stores`, `/cost-centers`, `/customers`, `/items`, `/rates`, `/pricing/resolve`
- **Ops:** `/orders` (CRUD), `/orders/{id}/tags`, `/orders/export.pdf?ids=…`
- **Invoices:** `/invoices/from-orders`, `/invoices/{id}/post`, `/invoices/export.pdf?ids=…`
- **Payments:** `/payments` CRUD, `/payments/export.{csv|xlsx|pdf}`
- **Logistics:** `/logistics/assign`, `/logistics/track/{id}`, `/logistics/settle/{id}`
- **Finance/Docs:** `/expenses` CRUD/approve/pay/export `, `/documents` upload/list/download/audit
- **WhatsApp:** `/whatsapp/templates`, `/whatsapp/send-feedback?order_id=…`, `/whatsapp/broadcast`, `/whatsapp/callback/provider`
- **Recon:** `/recon/import`, `/recon/rules`, `/recon/auto-match?file_id=…`, `/recon/manual-match`, `/recon/summary`
- **Franchise:** `/franchise/sources`, `/franchise/import`, `/franchise/import/{id}/review|commit`
- **HR:** `/attendance/clock-in|clock-out`, `/weekly-off`, `/leave`, `/reimburse`, `/payroll/run`, `/payroll/{id}/publish`
- **Reports/Analytics:** `/reports/income|sales|expenses`, `/analytics/owner|area|store`
- **Closing:** `/closing/preview?storeId&date`, `/closing/commit` (idempotent), `/closing/{id}/reopen`

---

## 9) Rate Limiting & Throttling

- **General API:** 60 req/min/IP (burst 120); 600 req/5min/user.
- **Auth:** 5 req/min/IP; 10 login attempts/hour/user; backoff + CAPTCHA.
- **Heavy reports:** 3 req/min/user; `limit ≤ 200` rows or use export job.
- **Exports:** ≤ 2 concurrent/user; ≤ 10 concurrent/company; ≤ 200/day/company.
- **Uploads:** 5 imports/hour/company; ≤ 25MB/file.
- **WhatsApp:** 1 campaign/min/company; ≤ 20 msgs/sec/company; ≤ 1 promo/week/recipient.
- **Webhooks:** 10 req/sec/company + HMAC; allowlist.
- **Docs downloads:** 60/min/IP.
- **Headers on 429:** Retry‑After, X‑RateLimit‑Limit/Remaining/Reset.

Implementation: Redis token bucket (async), optional edge (Nginx/Cloudflare). FE: exponential backoff + retries on 429/503; use idempotency keys.

---

## 10) RBAC Matrix (Excerpt)

| Module                        | Actions                            | Roles                                                                |
| ----------------------------- | ---------------------------------- | -------------------------------------------------------------------- |
| Companies/Stores/Cost Centers | CRUD                               | PlatformAdmin, CompanyAdmin                                          |
| Users/Roles/Store Access      | CRUD, assign                       | CompanyAdmin                                                         |
| Customers                     | CRUD                               | StoreManager, CompanyAdmin                                           |
| Items & Rates                 | CRUD                               | CompanyAdmin; StoreManager (if allowed)                              |
| Orders                        | CRUD, tags, export                 | StoreManager, Staff (limited)                                        |
| Invoices/Payments             | Post/Export                        | StoreManager, Accountant                                             |
| Logistics                     | assign/track/settle                | StoreManager                                                         |
| Expenses                      | CRUD/approve/pay/export            | Accountant, StoreManager                                             |
| Documents                     | upload/download/audit              | CompanyAdmin, StoreManager                                           |
| WhatsApp                      | templates/broadcast                | CompanyAdmin, StoreManager                                           |
| Recon                         | import/rules/match                 | Accountant                                                           |
| Franchise Imports             | source/import/commit               | CompanyAdmin                                                         |
| HR                            | attendance/leave/reimburse/payroll | StoreManager approve; Staff apply                                    |
| Analytics                     | view                               | per role scope                                                       |
| **Daily Store Closing**       | preview/commit/reopen              | StoreManager (commit), Area/Company Admin (reopen/variance override) |

---

## 11) Testing Strategy (TDD)

- **Backend:** pytest unit + API contract; Schemathesis/Dredd contract tests; migration test (`alembic upgrade head` on clean DB); rule engine tests (weekly‑off/pricing/packages/recon/closing); coverage ≥ 80%.
- **Frontend:** vitest + testing‑library; route guards; zod form tests; generated SDK in use (no hand‑written fetch).
- **E2E:** Playwright smoke: login → order → invoice → payment → export → WhatsApp feedback → **closing commit**.
- **Perf:** k6 on `/orders`, `/invoices/from-orders`, `/recon/auto-match`, `/closing/commit`.

---

## 12) Deployment & Migrations

- **Repos:** backend & frontend independent; Dockerfiles + compose (server).
- **Local (Mac, no Docker):** Python venv + `asyncpg`; Homebrew Postgres; `alembic upgrade head`; Node LTS + pnpm.
- **CI/CD:** BE publishes OpenAPI + **SDK package**; FE pins SDK version; CI fails on async violations and FE/BE version drift.
- **Zero‑downtime rule:** backward‑compatible migrations first → rollout; two‑step column renames; rollback plan documented.
- **Backups:** nightly pg_dump + WAL; retention DEV 7d / PROD 30d; restore runbook.

---

## 13) Directory Trees

**Backend**

```
backend/
  pyproject.toml
  alembic.ini
  docker/{Dockerfile,entrypoint.sh}
  app/
    main.py
    core/{config.py,security.py,logging.py}
    db/{session.py,base.py,migrations/}
    models/*.py
    schemas/*.py
    api/
      deps.py
      routers/  # auth, companies, stores, cost_centers, users, roles,
                # customers, items, rates, packages, orders, invoices,
                # payments, logistics, expenses, documents,
                # whatsapp, recon, franchise, hr, analytics, reports, closing
    services/{pricing.py,pdf.py,export.py,storage.py,rider.py,whatsapp.py,recon.py,franchise.py,payroll.py,closing.py}
    tasks/{queue.py}
    tests/{unit/,api/,e2e/}
```

**Frontend**

```
frontend/
  package.json
  vite.config.ts
  src/
    main.tsx
    app/{router.tsx,auth.ts,queryClient.ts,store.ts}
    components/ui/...
    pages/
      Dashboard.tsx
      masters/{Companies.tsx,Stores.tsx,CostCenters.tsx,Users.tsx,Roles.tsx,Customers.tsx,Items.tsx,Rates.tsx}
      ops/{Orders.tsx,Invoices.tsx,Payments.tsx,Logistics.tsx}
      finance/{Expenses.tsx,Documents.tsx,Reconciliation.tsx,FranchiseImports.tsx}
      hr/{Attendance.tsx,WeeklyOff.tsx,Leaves.tsx,Reimburse.tsx,Payroll.tsx}
      whatsapp/{Templates.tsx,Broadcasts.tsx}
      analytics/{Owner.tsx,Area.tsx,Store.tsx}
      closing/{DailyClose.tsx, CloseReport.tsx}
    hooks/, lib/, styles/, tests/
```

---

## 14) Rate/Quota & Consent Policies

- Per‑company monthly API quota; per‑company storage quota; alerts at 80%, cap at 100%.
- WhatsApp promo consent & **per‑recipient frequency cap** (≤ 1/week).

---

## 15) Retention, Locks & Periods

- **Daily Store Closing lock** (see §6.12) and **Monthly financial close**. Closed periods are read‑only; changes via reversal entries only.
- Retention: logs 90d; WhatsApp logs 180d; bank imports 18m; documents configurable; archival to cold storage after expiry.

---

## 16) Acceptance Criteria (UAT Excerpts)

1) Create order (piece+kg) → convert to invoice → debit package → UPI remainder → invoice PDF totals exact to paise.
2) Weekly off: Friday rejected; Wednesday accepted; payroll excludes weekly off.
3) Recon: import CSV; rules auto‑match by UTR; manual completes; summary tallies.
4) Franchise: monthly XLSX; mapping; fix fails; commit; monthly sales merged.
5) WhatsApp: feedback sent on delivery; status logged; retries handled.
6) Documents: upload GST cert; signed URL download; access logged.
7) Dashboards: Owner 30‑day KPIs; Store today’s tiles.
8) **Daily Store Closing:** preview shows takings; variance threshold enforces approval; commit locks day; reopen audited.

---

## 17) Risks & Mitigations

- Provider API variability → adapter pattern + mocks.
- CSV/XLSX diversity → mapping JSON + strict error rows.
- Data growth → partitioning candidates (bank_txn, message_log, download_log).
- Human error at closing → variance thresholds + reopen with audit.

---

## 18) Seeds & Fixtures

- Seed roles (PlatformAdmin, CompanyAdmin, AreaManager, StoreManager, Staff, Accountant, B2BSales).
- DEV admin with random password printed once.
- Demo company/store, sample items & rates, packages, recon rules, WhatsApp templates.

---

## 19) Feature Flags & Kill‑Switches

- Flags for WhatsApp sends, recon auto‑match, franchise adapters.
- Kill‑switch for messaging & jobs in admin panel + env override.

---

## 20) Compliance & Headers

- DPDP: consent record for promos; easy opt‑out.
- Security headers: HSTS, CSP (allow‑list), X‑Frame‑Options, Referrer‑Policy, SameSite=strict.

---

**End of SRS**


---

# 🔁 Addendum & Enhancements — SRS v2 (2025‑10‑07 Update)

This version merges all user‑requested additions, improvements, and seed initialization logic into a cohesive upgrade from v1.

## 21) Additional Reports

### 21.1 Pending Deliveries Report
- **Purpose:** Identify all orders not yet delivered.
- **Filters:** Store, Customer, Rider, Date Range, Process Stage.
- **Columns:** Order ID, Customer Name, Rider, Stage, QC Status, Delivery Mode, Days Pending.
- **Exports:** CSV, XLSX, PDF.

### 21.2 Pending Payments Report
- **Purpose:** Show invoices where payment < grand_total.
- **Filters:** Store, Date Range, Customer, Aging Buckets (0‑7, 8‑15, 16‑30, 30+ days).
- **Columns:** Invoice No, Invoice Date, Customer, Store, Grand Total, Payments Received, Balance, Days Outstanding.
- **Exports:** CSV, XLSX, PDF.

---

## 22) Customer Compensation & Claims

### 22.1 New Table — `customer_claim`
| Column            | Type                                              | Description                          |
| ----------------- | ------------------------------------------------- | ------------------------------------ |
| id                | uuid pk                                           |                                      |
| order_id          | uuid fk                                           | Reference to the order               |
| customer_id       | uuid fk                                           |                                      |
| article_tag_code  | text                                              | Optional, for per‑article issues     |
| reason_code       | text                                              | Defined in reason master             |
| description       | text                                              | Customer description                 |
| claim_type        | enum(`compensation`, `refund`, `redo`)            |                                      |
| amount_claimed    | numeric(14,2)                                     |                                      |
| amount_approved   | numeric(14,2)                                     |                                      |
| status            | enum(`open`, `approved`, `rejected`, `settled`)   |                                      |
| settlement_method | enum(`discount`, `refund`, `credit_note`, `redo`) |                                      |
| settlement_ref_id | uuid?                                             | Optional reference to related entity |
| created_by        | uuid fk user                                      |                                      |
| approved_by       | uuid?                                             |                                      |
| settled_at        | timestamptz?                                      |                                      |
| notes             | text                                              |                                      |

### 22.2 Rules
- QC failure may trigger a claim record.
- Approval by Area/Company Admin.
- Settlements audited; linked to next invoice if discount/credit note.

---

## 23) Dry‑Cleaning / Laundry Process Workflow (a–k)

### 23.1 New Tables
- **service_type**(code, name, description, active)
- **order_article**(order_id, article_tag_code, item_id?, service_type_id?, pre_qc_photos_doc_id?, post_qc_photos_doc_id?, qc_result=`full_fail|partial_fail|pass`, qc_notes)
- **order_stage_event**(order_id, stage_code, occurred_at, user_id, note)
- **order_delivery**(order_id, mode=`customer_pickup|store_drop`, rider_id?, delivered_at, delivered_by_user_id?, delivery_address_id?, proof_doc_id?)

### 23.2 Process Stages (Enforced Sequentially)
1. **Order Prepared Request** — may not yet contain articles (customer requests pickup).  
2. **Order Received at Store** — physically received.  
3. **Articles Recorded** — articles listed; `service_type` selected (Wash & Fold / Premium Wash / Premium Wash & Iron / Iron / Dry Cleaning).  
4. **Tags Printed** — per‑article tag generated.  
5. **Pre‑QC Photos Uploaded** — as ZIP document.  
6. **Processing** — active service stage.  
7. **QC Completed** — each article evaluated: full fail, partial fail, or pass.  
8. **Post‑QC Photos Uploaded** — allowed only if QC = pass.  
9. **Packed** — marked ready for delivery.  
10. **Delivered** — mode required (`customer_pickup` or `store_drop`); rider optional.  
11. **Settlement** — if customer has package balance → debit package, else record payment.

### 23.3 Workflow Enforcement
- Each stage write is **idempotent** (Idempotency‑Key required).
- Final stage updates `order.process_stage`.
- QC failures spawn optional customer claim.
- Stage changes logged in `order_stage_event`.

---

## 24) Store Staff Penalties & Recoveries

### 24.1 Table — `staff_adjustment`
| Column               | Type                                    | Description |
| -------------------- | --------------------------------------- | ----------- |
| id                   | uuid pk                                 |             |
| user_id              | uuid fk                                 | Employee    |
| date                 | date                                    |             |
| type                 | enum(`penalty`, `recovery`)             |             |
| reason_code          | text                                    |             |
| amount               | numeric(14,2)                           |             |
| status               | enum(`applied`, `approved`, `rejected`) |             |
| payroll_component_id | uuid?                                   |             |
| created_by           | uuid                                    |             |
| approved_by          | uuid?                                   |             |

### 24.2 Rules
- Created by Store/Area Manager, approved by Company Admin.  
- Applied to payroll deductions.  
- Net pay cannot be negative (carry forward remainder).

---

## 25) Seeds & Initial Data

### 25.1 Default Entities
**Company:** The Shaw Ventures (`TSV001`)  
**Cost Centers:**  
- UN3668 — Uttam Nagar  
- KN3817 — Kirti Nagar  
- SC3567 — Sector 56  
- SL1610 — Sushant Lok 1  
- TSV001 — The Shaw Ventures (HQ)

**Admin Login:**  
- Email: `wagid.sheikh@gmail.com`  
- Password: `Timbak2t#` (hashed & forced reset on first login; defined by `SEED_ADMIN_PASSWORD` env)

**Service Types (Pre‑seeded):**  
Wash & Fold, Premium Wash, Premium Wash & Iron, Iron, Dry Cleaning.

### 25.2 Safety
- Password printed once in DEV logs, never stored raw.  
- PROD must inject password via GitHub Secret, not repo.  

---

## 26) Engineering Standards Additions

### 26.1 Commenting Standards
- **Backend:** Docstrings on every public function/class + key inline comments. Enforced via `pydocstyle` (≥ 90 % coverage).  
- **Frontend:** JSDoc required for all exported functions/components (`eslint‑plugin‑jsdoc`).  
- **CI rule:** Build fails if missing required doc coverage.

### 26.2 `.gitignore` (Expanded)
Python, Node, OS/editor, Docker, and secret artifacts ignored:  
`__pycache__/`, `.venv/`, `node_modules/`, `.vite/`, `.DS_Store`, `.idea/`, `.vscode/`, `volumes/logs`, `*.env`, `*.pem`, `*.zip`, `*.tar.gz`, `*.log`, `secrets/`.

### 26.3 `.github/workflows`
- **backend‑ci.yml:** lint (ruff) → typecheck (mypy) → pytest → async guard → OpenAPI export → SDK publish → Docker build & deploy on tag.  
- **frontend‑ci.yml:** eslint → typecheck (tsc) → vitest → SDK version check → build → deploy static.  
- Codecov + environment‑based secrets + gated prod deploys.

### 26.4 Single Source of Truth (SSOT)
- Pydantic `Settings` is authoritative config.  
- `GET /config` exposes enums/constants (stages, service types, statuses).  
- Generated `@tsvcrm/constants` & `@tsvcrm/api‑types` consumed by FE.  
- No hard‑coded status/service strings in UI.

---

**End of SRS v2**


---

# 🧩 Review Annexures — Multi-Role Validation of SRS v2

## 1️⃣ CEO — *The Shaw Ventures (TSV)*

**Focus:** Business continuity, ROI, scalability.  

- The SRS aligns with TSV’s long-term SaaS roadmap — modular, multi-tenant, brand-agnostic (TumbleDry, UClean, Laundryfi).  
- Ensure **data ownership and portability clauses** are explicit for franchised vs company-owned stores.  
- Add a “Business Continuity & Disaster Recovery Plan” section (Recovery Time Objective ≤ 4 hrs, Recovery Point Objective ≤ 30 min).  
- Financial & operational dashboards should include a **“Company-wide consolidated view”** across cost centers.  
- Include an annual **“Technology Audit & Security Review”** milestone to ensure compliance and performance.  

🟢 *Verdict:* SRS is board-ready. Add BC/DR and data-ownership clarifications.

---

## 2️⃣ Area Manager

**Focus:** Multi-store supervision, staff discipline, store-wise analytics.  

- Add quick filters for **store performance comparison** (sales vs target, attendance, QC fails, customer claims).  
- Include an **exception dashboard** (late closing, unapproved variances, pending claims > 7 days).  
- Introduce **geo-tagged attendance and delivery maps** for verification.  
- Require **monthly store health score** auto-computed from KPIs (sales achievement, QC %, complaints).  

🟢 *Verdict:* Needs “Exception Dashboard” & “Store Health Scoring” modules for field control.

---

## 3️⃣ Marketing Manager

**Focus:** Campaign planning, ROI tracking, customer retention.  

- Add **lead source tracking** (Google, Instagram, Referral, Walk-in) in Customer & Order modules.  
- Integrate **coupon/promo codes** and link to campaigns.  
- WhatsApp broadcast logs should support **open/click metrics** (when provider allows).  
- Create **Campaign Performance Report:** spend, leads, conversions, revenue impact.  
- Ensure data export for CRM integration (HubSpot, Zoho).  

🟢 *Verdict:* Marketing layer solid but needs analytics hooks for ROI measurement and source tagging.

---

## 4️⃣ Sales Manager

**Focus:** Customer growth, package renewals, cross-selling.  

- Add **“Upcoming Package Expiry”** and **“Dormant Customer”** reports.  
- Need visibility of **claim history per customer** before renewals.  
- Integrate **auto-reminders** for follow-ups on estimates/quotations.  
- Include a **“Customer Segment”** field (Retail, Corporate, Society) for focused sales tracking.  
- Exportable customer ledger with package balance + pending payments.  

🟢 *Verdict:* Include renewal automation and segmentation to close sales loop.

---

## 5️⃣ CFO

**Focus:** Financial controls, reconciliation, cost tracking.  

- Require **Cost Center Ledger** auto-generated monthly with Income, Expenses, Royalty, Variance.  
- Add **Journal Entries & Adjustments module** (internal corrections, round-off, write-offs).  
- Pending Payments report should integrate **aging buckets with alert thresholds**.  
- Payroll integration must post GL-ready summary for accounting.  
- Add **audit trail of all monetary edits** (amount, tax, payment mode).  

🟢 *Verdict:* System must output GL-ready ledgers & audit logs for finance closure.

---

## 6️⃣ Store Manager

**Focus:** Daily operations, order flow, staff, and customer satisfaction.  

- Need **mobile-friendly EoD dashboard**: pending deliveries, pending payments, QC failures, and claims.  
- Add **staff attendance anomaly alerts** (late, missing punch).  
- Include **ready-to-print tag sheets** and **QR code-based article tracking**.  
- Simplify claim creation (auto-prefill from order & photos).  
- Ensure **offline sync buffer** (in case of network drop).  

🟢 *Verdict:* Feature-rich, but must emphasize mobile usability and offline fallback.

---

## 7️⃣ Washerman

**Focus:** Workload clarity, tagging, and QC visibility.  

- Need **daily job sheet** auto-generated with order no, item, service type, due date.  
- Include **color-coded QC status** in job list (pending/fail/pass).  
- Add photo reference before/after cleaning for clarity.  
- Enable feedback to mark articles requiring special treatment or stains.  

🟢 *Verdict:* Excellent workflow base; ensure handheld-friendly job sheet & visual QC interface.

---

## 8️⃣ Rider

**Focus:** Efficient pickups/deliveries & payout accuracy.  

- Must have **geo-tracked pickup/drop logs** and map integration.  
- Need **daily route plan** and “deliveries pending today” list.  
- Auto-calculate payout (₹ 3/km) visible in rider’s app summary.  
- Add **digital proof of delivery (photo/signature)**.  

🟢 *Verdict:* Add route optimization & digital PoD; strong payout structure already defined.

---

## 9️⃣ Product Architect

**Focus:** Scalability, modularity, maintainability.  

- Data model consistent; ensure **schema versioning** and backward compatibility (Alembic migration policy enforced).  
- Recommend defining **shared enums library** to avoid FE/BE drift.  
- Add **service mesh readiness** (if scaled micro-services later).  
- Maintain test coverage report as CI artifact.  
- Consider **event sourcing for order_stage_event** to allow replay/audit.  

🟢 *Verdict:* Architecture solid; future-proof with event sourcing and service-mesh notes.

---

## 🔟 Senior Developer

**Focus:** Codebase clarity, CI/CD efficiency.  

- Great use of async & TDD; add **pre-commit hooks** (ruff, mypy, pytest).  
- Ensure **OpenAPI schema diff tests** in CI.  
- Create **developer onboarding script** (clone → setup → test).  
- Define strict **type hint enforcement** (mypy strict mode).  
- Add **test data factories** for seeding test DB.  

🟢 *Verdict:* Add automation around schema diffing & local setup for dev velocity.

---

## 11️⃣ UI Developer

**Focus:** Component consistency, design system.  

- Define **UI kit tokens** (colors, spacing, typography).  
- Include **loading/skeleton states** for all pages.  
- Require **form validations via Zod** in all forms.  
- Add **accessibility checklist (WCAG 2.1 AA)** enforcement.  
- Confirm **component library** (shadcn/ui) used consistently.  

🟢 *Verdict:* Need design tokens & Zod validation consistency to prevent UI drift.

---

## 12️⃣ QA / QC Developer

**Focus:** Functional coverage, regression prevention.  

- Expand **E2E test suite** to cover claims, penalties, and QC workflow.  
- Add **test data reset scripts** for repeatable QA runs.  
- Include **visual regression snapshots** for UI.  
- Build **smoke test on deploy** step in GitHub Actions.  
- Maintain **traceability matrix** mapping test cases → requirements.  

🟢 *Verdict:* QA process sound; extend coverage to new claim/penalty modules.

---

## 13️⃣ System Administrator

**Focus:** Server stability, monitoring, backups.  

- Add section for **infrastructure monitoring** (CPU, RAM, Disk, Uptime, Docker healthchecks).  
- Implement **SSL renewal monitor** & **container restart policy (always)**.  
- Backup policy: daily full + 30-day WAL retention confirmed.  
- Logs: centralize to `/var/log/tsv-rsm/` and rotate weekly.  
- Security: disable password SSH; only key-based login; limit sudoers.  

🟢 *Verdict:* Infra strong; document backup verify & SSL renewal scripts.

---

# ✅ Summary — Gap Closure Plan

| Role              | Key Additions Proposed                  |
| ----------------- | --------------------------------------- |
| CEO               | BC/DR plan & data ownership             |
| Area Manager      | Exception dashboard, store health score |
| Marketing         | Lead source, campaign ROI               |
| Sales             | Renewal reminders, segmentation         |
| CFO               | Cost center ledger, GL audit trail      |
| Store Manager     | Mobile EoD view, offline mode           |
| Washerman         | Job sheet & QC color codes              |
| Rider             | Route plan, PoD                         |
| Product Architect | Event sourcing, service mesh note       |
| Senior Dev        | Pre-commit hooks, schema diff           |
| UI Dev            | Design tokens, accessibility            |
| QA                | Regression coverage on new modules      |
| SysAdmin          | Monitoring & SSL renewal policy         |

---

# 27) Business Continuity & Data Ownership Policy (NEW in v4)

### 27.1 Business Continuity / Disaster Recovery (BC/DR)

| Objective                          | Target                                                                         | Notes                                                    |
| ---------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------- |
| **Recovery Time Objective (RTO)**  | ≤ 4 hours                                                                      | Time to restore full operations after a critical outage. |
| **Recovery Point Objective (RPO)** | ≤ 30 minutes                                                                   | Maximum acceptable data loss window.                     |
| **Backups**                        | Nightly `pg_dump` + continuous WAL stream; retention 30 days (PROD).           |
| **Verification**                   | Automated restore test weekly; checksum validation on each backup.             |
| **Infra Redundancy**               | Dual VM snapshots with off-site object storage (S3 region-replicated).         |
| **Incident Response**              | On-call rotation (24×7); incident report within 2 hours of outage.             |
| **Dependencies**                   | Docker healthchecks, SSL renewal monitor, container restart policy (`always`). |

**DR Runbook:**  
1. Identify failure (scope → service → VM).  
2. Spin up standby VM from snapshot or compose stack from latest images.  
3. Restore PostgreSQL backup + replay WAL files.  
4. Run `alembic upgrade head`; verify integrity via E2E smoke suite.  
5. Notify stakeholders and resume CI/CD pipelines.  

---

### 27.2 Data Ownership & Portability

- Each **tenant (company)** retains ownership of its data (orders, customers, financials).  
- Platform admin acts as data processor only under tenant contract.  
- Tenants can export their complete dataset (JSON + XLSX + PDF) on demand without platform intervention.  
- Deletion requests honored within 15 days; audit log retained for legal compliance.  
- All backups encrypted (AES-256) and access-controlled via IAM policies.  
- On termination, tenant data is archived for 90 days then securely purged.  
- Data transfers use TLS 1.3 only; no cross-tenant data visibility.  

---

### 27.3 Security Audit & Compliance Schedule

| Audit Type                            | Frequency                    | Owner                     |
| ------------------------------------- | ---------------------------- | ------------------------- |
| **Technology & Performance Audit**    | Annually                     | CTO / Product Architect   |
| **Security & Vulnerability Scan**     | Quarterly                    | System Administrator      |
| **Data Protection Impact Assessment** | Annually or on major release | CISO / Compliance Officer |
| **Disaster Recovery Drill**           | Semi-annual                  | Infra Team Lead           |
| **Pen-Test / External Review**        | Yearly                       | 3rd-Party Security Firm   |

Reports are retained for 7 years and reviewed in board meetings.

---

**End of SRS v4 (Approved Baseline)**

---

### Sign-Off Checklist

| Role                 | Name / Title | Signature | Date |
| -------------------- | ------------ | --------- | ---- |
| CEO                  |              |           |      |
| CFO                  |              |           |      |
| Product Architect    |              |           |      |
| Senior Developer     |              |           |      |
| QA / QC Lead         |              |           |      |
| System Administrator |              |           |      |

---

*Prepared & Audited by:*  
**Document Auditor (ChatGPT – GPT-5)** on behalf of *The Shaw Ventures*  
*Revision lineage:* v1 → v2 (+modules) → v3 (+multi-role reviews) → v4 (+BC/DR & Data Ownership finalization).  
*All prior content preserved verbatim.*