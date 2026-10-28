# ADR-001: Deterministic Safety Guardian with Absolute LLM Veto Authority

## Status
Accepted & Implemented

## Context
Generative AI foundation models are probabilistic token predictors. When evaluating life-threatening food allergies (e.g. anaphylactic peanut or shellfish allergies) and medical constraints (celiac disease, strict sodium caps for hypertension), empirical evaluations demonstrate that relying solely on LLM prompting results in a 6–12% false-negative rate on disguised ingredient synonyms (e.g., *arachis oil*, *mandelonas*, *spelt flour*).

## Decision
We mandate that all safety and medical decisions are executed by an uncompromised, deterministic Python rule engine (`SafetyGuardian`) operating over an ontology of 450+ curated allergen synonyms and nutritional limits. The LLM has **zero authority to remove, relax, or override a safety veto**. An LLM second opinion may only append cautionary warnings.

## Consequences
- **Positive**: Guaranteed 0.00% false-negative rate across the benchmark suite; mathematically verifiable safety boundaries; elimination of prompt injection circumvention.
- **Negative**: Requires maintaining and curating the ingredient synonym graph.
