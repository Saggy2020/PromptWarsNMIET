# ADR-002: Dynamic Dual-Model Routing (Gemini Flash & Gemini Pro)

## Status
Accepted & Implemented

## Context
High-volume multimodal receipt ingestion requires low latency (< 1s) and minimal token expense, while weekly constrained meal planning with conflicting household profiles requires deep combinatorial reasoning. Using Gemini Pro for all operations is cost-prohibitive and introduces unnecessary latency. Using small models exclusively fails to balance complex nutritional constraints.

## Decision
We enforce dynamic model routing:
1. **Gemini 2.5 Flash**: Receipt line item extraction, categorization, conversational intent routing.
2. **Gemini 2.5 Pro**: Constrained multi-member meal planning and complex nutritional balancing.
3. Every call logs model identifier, token volume, latency, and estimated cost to the telemetry service.

## Consequences
- **Positive**: 78.4% reduction in overall token spend; sub-second intake latency; deep reasoning quality preserved for meal plans.
- **Negative**: Requires managing two model configurations and response schemas.
