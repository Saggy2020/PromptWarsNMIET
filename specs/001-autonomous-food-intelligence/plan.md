# Implementation Plan: Autonomous Household Food-Intelligence System (PantryPilot)

**Branch**: `001-autonomous-food-intelligence` | **Date**: 2026-10-23 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-autonomous-food-intelligence/spec.md`

---

## Summary

PantryPilot is an autonomous multi-agent household food-intelligence platform engineered to dramatically cut household food waste while enforcing deterministic dietary, allergen, and medical safety constraints across all household members. The system couples Gemini multimodal models on Vertex AI with dynamic model routing (Gemini Flash for rapid intake and categorization; Gemini Pro for complex multi-member constrained meal planning) alongside an uncompromised, deterministic Python-based Safety Guardian rule engine with absolute veto authority.

---

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript 5.4+ / Node.js 20+ (Frontend)  
**Primary Dependencies**:
- *Backend*: FastAPI, Pydantic v2, Google GenAI SDK (Vertex AI / Gemini 2.5), Uvicorn, httpx, python-multipart, pytest.
- *Frontend*: Next.js 14/15 (App Router), React 19, Tailwind CSS, Lucide React, Zod.  
**Storage**:
- Cloud Firestore (per-household data isolation) / In-memory & JSON file storage for standalone Demo Mode.
- Google Cloud Storage for receipt images with signed URLs and EXIF stripping.
- Google BigQuery for analytics events, waste reduction calculations, and agent telemetry.  
**Testing**: pytest (backend unit/integration/safety evals), Playwright (E2E flows), custom Golden Dataset eval harness.  
**Target Platform**: Google Cloud Run (Backend), Firebase Hosting / Vercel (Frontend), Desktop & Mobile Browsers (WCAG 2.2 AA).  
**Project Type**: Full-stack Web Application with autonomous multi-agent orchestration and deterministic safety micro-kernel.  
**Performance Goals**: p95 API response < 500 ms; p95 single-agent LLM operation < 8 s; UI LCP < 2.5 s.  
**Constraints**:
- Absolute zero false-negative allergen safety policy (deterministic engine vetoes any LLM output).
- 100% functional standalone Demo Mode without cloud credentials.
- Zero secrets committed to source control.  
**Scale/Scope**: Up to 6 members per household, hundreds of live pantry items, weekly meal planning, 50-receipt golden evaluation suite.

---

## Constitution Check

*GATE: All gates verified against project constitution at `.specify/memory/constitution.md`.*

| Constitution Principle | Gate Status | Architecture Compliance Mechanism |
|:---|:---|:---|
| **I. Security First** | PASSED | Schema validation via Pydantic v2; EXIF stripping on uploads; secrets in Secret Manager / env; OWASP LLM01–10 defenses. |
| **II. Safety Over Helpfulness** | PASSED | Deterministic Allergen Ontology & Medical Rule Engine has absolute veto power over LLM output. LLM cannot remove warnings. |
| **III. Human in the Loop** | PASSED | Ingestion, recipe approvals, shopping list finalization, and inventory deletion require explicit user confirmation. |
| **IV. Measurable Efficiency** | PASSED | Model routing (`gemini-flash` for extraction, `gemini-pro` for planning); per-call token, cost, and latency logging; food waste metrics. |
| **V. Performance Budgets** | PASSED | Non-LLM p95 < 500ms; LLM p95 < 8s; streaming UI agent status ticker; LCP < 2.5s. |
| **VI. Test-First & Eval Suite** | PASSED | Unit, integration, safety suite (100+ cases), golden eval dataset (50 receipts), adversarial injection benchmark (25 cases). |
| **VII. Privacy by Design** | PASSED | Household ID isolation; PII redaction layer prior to LLM prompts; 1-click Export and Delete data flows. |
| **VIII. Reliability & Graceful Degradation** | PASSED | Circuit breakers; deterministic heuristic fallback planner for offline/outage scenarios; idempotent writes. |
| **IX. Observability & Auditability** | PASSED | Correlation IDs on all traces; structured JSON logging; transparent "Why this recipe?" audit trail. |
| **X. Accessibility & Demo Mode** | PASSED | WCAG 2.2 AA compliant palette; responsive UI; zero-credential Demo Mode pre-seeded with realistic household. |
| **XI. Documentation & Originality** | PASSED | Original codebase; complete `DISCLOSURE.md`; architecture diagrams; threat models; `METRICS.md`. |

---

## Project Structure

```text
PromptWarsNMIET/
├── .specify/                         # Spec Kit configuration, memory, templates, scripts
├── specs/
│   └── 001-autonomous-food-intelligence/
│       ├── spec.md                   # Feature specification
│       ├── plan.md                   # Architectural implementation plan (this file)
│       ├── research.md               # Technical research & decisions
│       ├── data-model.md             # Pydantic v2 schemas and entity models
│       ├── quickstart.md             # Quick launch & demo evaluation guide
│       ├── contracts/
│       │   ├── agent-contracts.md    # Multi-agent interaction protocols
│       │   └── api-spec.json         # OpenAPI REST endpoint specifications
│       └── checklists/
│           └── requirements.md       # Specification quality checklist
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI entrypoint, middleware, error handlers
│   │   ├── config.py                 # Pydantic settings, env secrets, demo mode toggle
│   │   ├── models/                   # Core schemas (Pydantic v2)
│   │   │   ├── __init__.py
│   │   │   ├── household.py
│   │   │   ├── inventory.py
│   │   │   ├── meal_plan.py
│   │   │   └── telemetry.py
│   │   ├── safety/                   # DETERMINISTIC SAFETY ENGINE (Zero LLM Veto)
│   │   │   ├── __init__.py
│   │   │   ├── engine.py             # Deterministic allergen & medical constraint evaluator
│   │   │   ├── ontology.py           # 450+ allergen synonyms, cross-reactivity mapping
│   │   │   └── shelf_life.py         # Curated food shelf-life heuristics table
│   │   ├── agents/                   # MULTI-AGENT ORCHESTRATION (ADK / Gemini)
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py       # Intent router, human confirmation gatekeeper
│   │   │   ├── vision_intake.py      # Multimodal receipt & shelf extraction agent (Flash)
│   │   │   ├── meal_planner.py       # Constrained waste-minimizing planner agent (Pro)
│   │   │   ├── procurement.py        # Shopping list & substitution agent
│   │   │   ├── sustainability.py     # Waste avoided & CO2e emissions calculator
│   │   │   └── mock_provider.py      # Deterministic local mock provider for Demo Mode
│   │   ├── security/                 # SECURITY & PRIVACY CONTROLS
│   │   │   ├── __init__.py
│   │   │   ├── pii_redactor.py       # PII sanitizer before LLM prompts
│   │   │   ├── injection_guard.py    # Adversarial prompt injection defense filter
│   │   │   └── audit_logger.py       # Immutable agent decision audit trail
│   │   ├── api/                      # REST API ROUTERS
│   │   │   ├── __init__.py
│   │   │   ├── intake_routes.py
│   │   │   ├── inventory_routes.py
│   │   │   ├── plan_routes.py
│   │   │   ├── shopping_routes.py
│   │   │   ├── sustainability_routes.py
│   │   │   └── demo_routes.py
│   │   └── services/
│   │       ├── storage_service.py    # Firestore / Local file state store
│   │       └── telemetry_service.py  # Latency, token, and cost tracker
│   ├── tests/                        # AUTOMATED TEST SUITE
│   │   ├── test_safety_engine.py     # Deterministic allergen & synonym tests
│   │   ├── test_intake_agent.py      # Receipt extraction tests
│   │   ├── test_meal_planner.py      # Waste-priority planning tests
│   │   ├── test_injection_guard.py   # Adversarial prompt-injection tests
│   │   └── test_api_endpoints.py     # REST API route integration tests
│   ├── evals/                        # HACKATHON EVAL HARNESS
│   │   ├── run_safety_suite.py       # 100+ allergen test cases -> 0% false negative gate
│   │   ├── run_injection_suite.py    # 25 adversarial prompts -> 100% blocked gate
│   │   ├── run_golden_eval.py        # 50-receipt golden dataset -> F1 calculation
│   │   └── golden_data/              # Seed receipts and adversarial prompts
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/                      # Next.js App Router
│   │   │   ├── layout.tsx            # Global layout with theme provider & header
│   │   │   ├── page.tsx              # Main dashboard overview
│   │   │   ├── intake/page.tsx       # Receipt & pantry photo upload page
│   │   │   ├── inventory/page.tsx    # Live pantry with expiry countdown badges
│   │   │   ├── planner/page.tsx      # Multi-agent meal planning & safety veto UI
│   │   │   ├── shopping/page.tsx     # Aisle-grouped procurement list
│   │   │   └── impact/page.tsx       # Food waste, money saved, and CO2e dashboard
│   │   ├── components/               # Accessible UI components (Tailwind)
│   │   │   ├── AgentTicker.tsx       # Streaming multi-agent activity ticker
│   │   │   ├── SafetyVetoBanner.tsx  # Deterministic safety alert card
│   │   │   ├── ExpiryBadge.tsx       # Color-coded expiry countdown
│   │   │   ├── DemoBanner.tsx        # Zero-credential demo status banner
│   │   │   └── Navbar.tsx            # Navigation header
│   │   ├── lib/                      # API client, types, and mock demo seeds
│   │   │   ├── api.ts
│   │   │   └── demo_data.ts
│   ├── package.json
│   ├── tailwind.config.js
│   └── tsconfig.json
├── docs/
│   ├── architecture.md               # Mermaid architecture & data flow diagrams
│   ├── threat-model.md               # STRIDE threat model & defenses
│   └── adr/
│       ├── ADR-001-deterministic-safety-engine.md
│       ├── ADR-002-dual-model-routing.md
│       └── ADR-003-zero-credential-demo-mode.md
├── DISCLOSURE.md                     # Exhaustive library, model, and API disclosure
├── METRICS.md                        # Measured evaluation scores, latency, and costs
└── README.md                         # Comprehensive hackathon presentation & setup
```

---

## Complexity Tracking

| Architectural Component | Why Needed | Simpler Alternative Rejected Because |
|:---|:---|:---|
| **Deterministic Allergen Ontology** | Ensures 0% false negatives on hidden allergen synonyms | Relying on LLM prompting alone causes 6–12% dangerous false negatives |
| **Dual-Model Routing (Flash + Pro)** | Balances sub-second extraction with deep constrained planning | Using Pro for all tasks inflates costs 10x; using Flash alone fails complex constraints |
| **Zero-Credential Demo Mode** | Enables hackathon judges to verify the system immediately offline | Requiring judges to setup Google Cloud billing & API keys causes friction |
