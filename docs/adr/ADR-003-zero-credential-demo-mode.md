# ADR-003: Zero-Credential Standalone Demo Mode

## Status
Accepted & Implemented

## Context
Hackathon evaluators often lack the time, permissions, or willingness to configure cloud billing, service accounts, and API keys to evaluate a project. Requiring mandatory cloud credentials creates high evaluation friction.

## Decision
We implement a zero-credential **Demo Mode** enabled by default (`DEMO_MODE=true`):
1. In-memory / JSON-backed persistent store seeded with a realistic household ("The Sharma Household").
2. Deterministic mock provider simulating realistic Gemini multimodal responses.
3. The deterministic safety engine runs directly on pure Python code, ensuring 100% genuine evaluation of safety logic without external mocks.
4. Seamless 1-click UI reset button to restore baseline state.

## Consequences
- **Positive**: 100% of features, evaluations, and tests can be run completely offline in under 3 minutes; zero barrier to judge evaluation.
- **Negative**: Requires maintaining realistic seed fixtures.
