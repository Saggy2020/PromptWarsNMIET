<!--
Sync Impact Report:
- Version change: none -> v1.0.0 (initial ratification)
- Added sections: Core Principles (11 testable principles), Additional Technical & Hackathon Constraints, Quality Gates & Definition of Done, Governance
- Status: Fully resolved, zero deferred placeholders
-->

# PantryPilot Constitution

Autonomous Multi-Agent Household Food Intelligence & Waste Reduction System

## Core Principles

### I. Security First (Non-Negotiable)
- All untrusted input (receipt uploads, image scans, user chat prompts, barcode lookups) MUST be validated against strict schemas (Pydantic v2 / Zod) before processing.
- No secrets, API keys, or service account credentials shall ever exist in source code or git history; all secrets MUST be injected via environment variables or Google Cloud Secret Manager.
- All LLM outputs MUST be treated as untrusted and schema-validated before any system state modification or downstream consumption.
- The system MUST defend against OWASP Top 10 and OWASP Top 10 for LLMs (prompt injection, insecure output handling, excessive agency, training data poisoning). File uploads MUST enforce magic-byte verification, size limits, and EXIF sanitization.

### II. Safety Over Helpfulness (Deterministic Veto)
- Dietary constraints, allergen presence, medical contraindications (e.g., sodium limits for hypertension, glycemic index warnings, celiac disease/gluten) MUST be validated by a DETERMINISTIC rule engine using a curated allergen ontology and ingredient synonym graph.
- The LLM NEVER has the final say on allergen or medical safety. The deterministic safety engine has absolute veto authority over any generated recipe, meal plan, or ingredient substitution.
- An LLM second opinion may only add safety warnings or flag potential risks; it can NEVER remove, relax, or override a deterministic safety veto.
- Zero allergen-safety false negatives on the test suite is a hard deployment gate.

### III. Human in the Loop
- Autonomous agents can analyze, extract, optimize, and propose actions, but NO action with external, financial, or irreversible state impact (e.g., clearing inventory, executing purchases, sharing household lists, deleting profile constraints) shall execute without explicit user confirmation.
- Every agent recommendation MUST present an actionable confirmation UI with clear diffs of before and after state.

### IV. Measurable Efficiency & Intelligent Model Routing
- Every LLM invocation MUST log model identifier, prompt/completion tokens, latency (ms), and calculated cost (USD).
- Dynamic model routing MUST be enforced: lightweight fast models (e.g., Gemini 1.5/2.0 Flash) for high-throughput multimodal receipt extraction, entity parsing, and categorization; advanced reasoning models (e.g., Gemini Pro) strictly for complex multi-constraint meal planning.
- Static and semantic caching MUST be applied to recurrent ingredient parsing and shelf-life lookups to minimize duplicate token spend.
- The application MUST continuously compute and expose the primary sustainability metric: "Food Waste Avoided" (in kg and estimated CO2e / currency savings).

### V. Performance Budgets
- p95 latency for non-LLM API endpoints MUST be under 500 ms.
- p95 latency for single-agent LLM operations MUST be under 8 seconds.
- Multi-agent orchestration workflows MUST stream progress updates to the UI in real-time, showing which agent is currently active.
- Frontend Largest Contentful Paint (LCP) MUST be under 2.5 seconds on standard broadband connections.

### VI. Test-First Quality & Eval Harness
- Test-driven methodology is strictly enforced: unit tests, integration tests, E2E browser flows (Playwright), and an LLM evaluation harness.
- A golden dataset (50+ receipts, diverse dietary edge cases, and adversarial prompt injections) MUST be maintained with automated F1 scoring (target >= 0.90 for intake extraction) and 100% injection defense pass rate.
- Minimum 80% code coverage on core business logic and safety engine components.
- Automated CI pipeline MUST pass all linters, type checks, and safety tests before merge.

### VII. Privacy by Design & Data Isolation
- Strict per-household data isolation: users can never access or query inventory, profiles, or plans of another household.
- Personal Identifiable Information (PII) MUST be redacted or masked prior to sending user-generated text/images to third-party or foundational LLM endpoints.
- Full compliance with data sovereignty: Provide clear "Export My Data" (JSON) and "Delete My Data" (hard delete across storage/database) workflows.

### VIII. Reliability, Graceful Degradation & Resilience
- Every agent call and external API request MUST feature timeouts, bounded retries with exponential backoff, and circuit breaker patterns.
- If cloud AI services are unreachable or rate-limited, the system MUST gracefully degrade to deterministic offline rules (e.g., rule-based pantry recipe lookup and curated shelf-life heuristics) without application crash.
- State-mutating operations MUST be idempotent using idempotency keys.

### IX. Observability & Explainability
- Every request and agent execution trace MUST carry a unique Correlation ID.
- Agent decisions MUST produce an audit trail containing: triggering event, data retrieved, candidate options, deterministic safety checks applied, and final user-facing rationale ("Why this recipe?").
- Structured JSON logging across all backend and agent components.

### X. Accessibility, UX & Standalone Demo Mode
- The user interface MUST comply with WCAG 2.2 Level AA accessibility standards, responsive across desktop and mobile, with full light and dark mode themes.
- The project MUST include a zero-credential DEMO MODE pre-seeded with a realistic household (allergies, diabetic constraints, near-expiry inventory) that runs completely offline using local mocks or emulators for immediate hackathon judge evaluation.

### XI. Documentation & Originality
- All code MUST be original work built specifically for PantryPilot.
- Every open-source library, external pretrained model, framework, and dataset MUST be exhaustively cataloged in `DISCLOSURE.md` detailing purpose and license.
- Architecture diagrams, STRIDE threat models, and Architecture Decision Records (ADRs) MUST be versioned directly in repository documentation.

## Hackathon Evaluation Alignment

PantryPilot directly targets all five judging criteria:
1. **Security**: Deterministic allergen veto, PII redaction, prompt injection defense harness, schema boundaries, signed URLs, Secret Manager, App Check.
2. **Efficiency**: Gemini Flash / Pro model routing, token and financial telemetry, context caching, measurable food waste reduction analytics.
3. **Technology Implemented**: Multi-agent orchestration (Vision Intake, Inventory, Safety Guardian, Meal Planner, Procurement, Sustainability), deterministic constraint solver alongside generative AI, automated golden evaluation harness.
4. **Performance**: Latency budgets (p95 < 500ms API, < 8s LLM), streaming UI, async parallel execution, graceful offline fallback.
5. **Google Technology**: Gemini on Vertex AI, Agent Development Kit (ADK) concepts, Firebase Auth/Firestore/Storage, Google Cloud Run, BigQuery analytics, Secret Manager.

## Governance & Definition of Done

### Amendment Procedure
1. Any modification to this Constitution requires a formal documented proposal specifying the rationale, affected principles, and migration impact.
2. Versioning follows Semantic Versioning:
   - **MAJOR (X.0.0)**: Removal or fundamental redefinition of core safety/security principles.
   - **MINOR (1.X.0)**: Addition of new principles, architectural standards, or evaluation criteria.
   - **PATCH (1.0.X)**: Wording clarifications, typo fixes, and non-semantic documentation enhancements.

### Definition of Done (DoD)
A feature or pull request is considered complete ONLY when:
1. All deterministic safety and constraint rules pass with 100% compliance (zero safety regressions).
2. Code coverage on business logic meets or exceeds 80%.
3. Golden eval harness runs and verifies extraction F1 >= 0.90 and 0 prompt injection escapes.
4. Latency and token metrics are recorded and within budget.
5. DISCLOSURE.md is updated for any new dependencies.
6. The feature functions seamlessly in both Live Cloud Mode and Zero-Credential Demo Mode.

**Version**: 1.0.0 | **Ratified**: 2026-10-23 | **Last Amended**: 2026-10-23
