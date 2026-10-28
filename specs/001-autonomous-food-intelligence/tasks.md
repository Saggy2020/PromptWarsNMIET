# Tasks: Autonomous Household Food-Intelligence System (PantryPilot)

**Input**: Design documents from `/specs/001-autonomous-food-intelligence/`  
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `.specify/memory/constitution.md`

## Format: `- [X] [ID] [P?] [Story?] Description with exact file path`

---

## Phase 1: Setup & Repository Scaffold

- [X] T001 Scaffold backend and frontend directories per plan in `backend/` and `frontend/`
- [X] T002 [P] Configure backend dependencies and lockfile in `backend/requirements.txt`
- [X] T003 [P] Configure frontend Next.js App Router, Tailwind CSS, and Lucide icons in `frontend/package.json`
- [X] T004 [P] Setup environment configuration and secrets template in `.env.example` and `backend/app/config.py`
- [X] T005 [P] Setup GitHub Actions CI workflow (linting, pytest, typecheck, eval gate) in `.github/workflows/ci.yml`

---

## Phase 2: Foundational Infrastructure & Security Baseline

- [X] T006 Implement core Pydantic v2 schemas (Household, Member, Allergy, Severity) in `backend/app/models/household.py`
- [X] T007 [P] Implement inventory schemas and shelf-life enums in `backend/app/models/inventory.py`
- [X] T008 [P] Implement meal planning, recipe, and verdict schemas in `backend/app/models/meal_plan.py`
- [X] T009 [P] Implement telemetry and audit log schemas in `backend/app/models/telemetry.py`
- [X] T010 Implement curated food shelf-life lookup table in `backend/app/safety/shelf_life.py`
- [X] T011 Implement 450+ allergen synonym and cross-reactivity ontology in `backend/app/safety/ontology.py`
- [X] T012 Implement DETERMINISTIC Safety Guardian Rule Engine (Zero-LLM Veto) in `backend/app/safety/engine.py`
- [X] T013 [P] Implement PII Sanitizer and Redaction Engine in `backend/app/security/pii_redactor.py`
- [X] T014 [P] Implement Prompt-Injection Defense Filter and Delimiter Guard in `backend/app/security/injection_guard.py`
- [X] T015 [P] Implement Telemetry, Token Cost, and Audit Logger in `backend/app/security/audit_logger.py`
- [X] T016 Implement In-Memory / File-based State Store with Demo Mode toggle in `backend/app/services/storage_service.py`
- [X] T017 Implement Mock LLM Provider for offline Zero-Credential execution in `backend/app/agents/mock_provider.py`
- [X] T018 Setup FastAPI application, CORS, security headers, and router wiring in `backend/app/main.py`
- [X] T019 Implement baseline unit tests for Deterministic Safety Engine in `backend/tests/test_safety_engine.py`

---

## Phase 3: User Story 1 - Multimodal Intake & Live Inventory (Priority: P1)

- [X] T020 [P] [US1] Unit test for intake extraction and shelf-life matching in `backend/tests/test_api_endpoints.py`
- [X] T021 [US1] Implement Vision Intake Agent with Gemini Flash / Mock Provider in `backend/app/agents/vision_intake.py`
- [X] T022 [US1] Implement Intake API endpoints (POST `/api/intake/receipt`, POST `/api/intake/approve`) in `backend/app/api/intake_routes.py`
- [X] T023 [US1] Implement Live Inventory API endpoints (GET/POST/PUT/DELETE `/api/inventory`) in `backend/app/api/inventory_routes.py`
- [X] T024 [P] [US1] Build accessible Expiry Countdown Badge component in `frontend/src/components/ExpiryBadge.tsx`
- [X] T025 [US1] Build Grocery Intake & Receipt Review page in `frontend/src/app/intake/page.tsx`
- [X] T026 [US1] Build Live Pantry Inventory view with countdown filters in `frontend/src/app/inventory/page.tsx`

---

## Phase 4: User Story 2 - Household Profiles & Deterministic Safety Veto (Priority: P1)

- [X] T027 [P] [US2] Safety integration tests (14 allergen classes, medical sodium limits) in `backend/tests/test_safety_engine.py`
- [X] T028 [US2] Implement Household Profile API routes in `backend/app/api/household_routes.py`
- [X] T029 [US2] Implement Safety Veto API endpoint (POST `/api/safety/veto-check`) in `backend/app/api/safety_routes.py`
- [X] T030 [P] [US2] Build Safety Veto Alert Banner component in `frontend/src/components/SafetyVetoBanner.tsx`
- [X] T031 [US2] Build Household Profiles & Dietary Constraints UI in `frontend/src/app/profiles/page.tsx`

---

## Phase 5: User Story 3 - Autonomous Waste-Minimizing Meal Planner & Re-planning (Priority: P1)

- [X] T032 [P] [US3] Unit tests for waste-prioritizing recipe optimizer in `backend/tests/test_api_endpoints.py`
- [X] T033 [US3] Implement Constrained Meal Planner Agent (Gemini Pro / Mock) with explainability in `backend/app/agents/meal_planner.py`
- [X] T034 [US3] Implement Re-Planning Agent triggered by inventory deltas in `backend/app/agents/replanner.py`
- [X] T035 [US3] Implement Meal Planning API endpoints in `backend/app/api/plan_routes.py`
- [X] T036 [P] [US3] Build Agent Streaming Telemetry Activity Ticker in `frontend/src/components/AgentTicker.tsx`
- [X] T037 [US3] Build Interactive Meal Planner & Recipe Explainability page in `frontend/src/app/planner/page.tsx`

---

## Phase 6: User Story 4 - Smart Procurement & Shopping List (Priority: P2)

- [X] T038 [P] [US4] Unit test for inventory diffing and safe substitutions in `backend/tests/test_api_endpoints.py`
- [X] T039 [US4] Implement Procurement Agent in `backend/app/agents/procurement.py`
- [X] T040 [US4] Implement Shopping List API endpoints in `backend/app/api/shopping_routes.py`
- [X] T041 [US4] Build Aisle-Grouped Smart Shopping List UI with approval gate in `frontend/src/app/shopping/page.tsx`

---

## Phase 7: User Story 5 - Sustainability & Financial Impact Dashboard (Priority: P2)

- [X] T042 [P] [US5] Unit test for CO2e and financial calculation logic in `backend/tests/test_api_endpoints.py`
- [X] T043 [US5] Implement Sustainability Analyst Agent in `backend/app/agents/sustainability.py`
- [X] T044 [US5] Implement Sustainability API endpoints in `backend/app/api/sustainability_routes.py`
- [X] T045 [US5] Build Sustainability & Financial Impact Dashboard in `frontend/src/app/impact/page.tsx`

---

## Phase 8: User Story 6 - Conversational Assistant with Action Guardrails (Priority: P2)

- [X] T046 [P] [US6] Unit test for assistant action proposal schemas in `backend/tests/test_injection_guard.py`
- [X] T047 [US6] Implement Multi-Agent Conversational Orchestrator in `backend/app/agents/orchestrator.py`
- [X] T048 [US6] Implement Assistant Chat API endpoints in `backend/app/api/assistant_routes.py`
- [X] T049 [US6] Build Conversational Assistant Drawer with confirmation cards in `frontend/src/components/AssistantDrawer.tsx`

---

## Phase 9: User Story 7 - Privacy Controls, Audit Trail & Zero-Credential Demo Mode (Priority: P3)

- [X] T050 [P] [US7] Implement Seed Script & Demo Household Provider in `backend/app/api/demo_routes.py`
- [X] T051 [US7] Implement Data Export and Data Deletion API endpoints in `backend/app/api/privacy_routes.py`
- [X] T052 [P] [US7] Build Demo Mode Banner & Switch in `frontend/src/components/DemoBanner.tsx`
- [X] T053 [US7] Build Audit Trail & Privacy Controls page in `frontend/src/app/audit/page.tsx`

---

## Phase 10: Evaluation Harness, Adversarial Suite & Submission Polish

- [X] T054 Create 50-receipt Golden Dataset in `backend/evals/golden_data/receipts.json`
- [X] T055 [P] Create 100+ case Allergen Safety Test Suite in `backend/evals/golden_data/allergen_cases.json`
- [X] T056 [P] Create 25-case Adversarial Prompt Injection Suite in `backend/evals/golden_data/injections.json`
- [X] T057 Implement Golden Receipt Extraction Evaluation Harness in `backend/evals/run_golden_eval.py`
- [X] T058 Implement Deterministic Allergen Safety Benchmark in `backend/evals/run_safety_suite.py`
- [X] T059 Implement Adversarial Injection Defense Benchmark in `backend/evals/run_injection_suite.py`
- [X] T060 Execute all evaluation suites and generate `METRICS.md` with measured F1, safety pass rate, and latency
- [X] T061 [P] Author exhaustive `DISCLOSURE.md` detailing every library, model, and dataset
- [X] T062 [P] Author Architecture & Threat Model documentation in `docs/architecture.md` and `docs/threat-model.md`
- [X] T063 [P] Author ADRs for key technical decisions in `docs/adr/`
- [X] T064 Finalize master `README.md` with setup guide, architecture diagram, security overview, and 3-minute judge script
