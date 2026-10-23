# Open-Source & Model Attribution Disclosure (DISCLOSURE.md)

This document provides a comprehensive and transparent disclosure of all third-party open-source libraries, frameworks, pretrained models, datasets, and APIs utilized in **PantryPilot** in accordance with hackathon originality guidelines.

All orchestration logic, multi-agent pipelines, deterministic allergen ontology engine, prompt injection filters, and web applications are original work developed specifically for this project.

---

## 1. Pretrained Models & AI APIs

| Model / Service | Provider | Purpose in Project | License / Terms |
|:---|:---|:---|:---|
| **Gemini 2.5 Flash** (`gemini-2.5-flash`) | Google / Vertex AI | High-throughput multimodal receipt line extraction and food item categorization | Google Cloud Terms of Service |
| **Gemini 2.5 Pro** (`gemini-2.5-pro`) | Google / Vertex AI | Constrained weekly household meal planning with multi-member optimization | Google Cloud Terms of Service |
| **Google GenAI SDK** (`google-genai`) | Google Cloud | Native Python SDK for Vertex AI and Gemini multimodal invocations | Apache 2.0 |

---

## 2. Backend Libraries (Python 3.11+)

| Package | Version | Purpose | License |
|:---|:---|:---|:---|
| **FastAPI** | 0.115+ | High-performance async web framework for REST API endpoints | MIT License |
| **Pydantic / Pydantic Settings** | 2.8+ | Schema validation at untrusted boundaries, data models, settings | MIT License |
| **Uvicorn** | 0.30+ | ASGI production server for FastAPI | BSD-3-Clause |
| **HTTPX** | 0.27+ | Async HTTP client for internal services and testing | BSD-3-Clause |
| **python-multipart** | 0.0.9+ | Streaming multipart form parsing for receipt uploads | Apache 2.0 |
| **pytest / pytest-asyncio** | 8.3+ | Automated test framework, unit tests, and eval harnesses | MIT License |
| **Pillow (PIL)** | 10.4+ | Image processing and EXIF metadata stripping before upload | Historical Permission Notice |

---

## 3. Frontend Frameworks & Libraries (Node.js 20+)

| Package | Version | Purpose | License |
|:---|:---|:---|:---|
| **Next.js** | 14.2+ | React server framework with App Router, SSR, and API routing | MIT License |
| **React / React-DOM** | 18.3+ | User interface component rendering library | MIT License |
| **Tailwind CSS** | 3.4+ | Utility-first CSS framework for responsive WCAG AA styling | MIT License |
| **Lucide React** | 0.453+ | Clean, accessible iconography | ISC License |
| **TypeScript** | 5.6+ | Static type safety and contract enforcement | Apache 2.0 |

---

## 4. Benchmark Datasets & Emission Citations

| Dataset / Source | Author / Citation | Usage in Project |
|:---|:---|:---|
| **Global Food Environmental Impact Dataset** | Poore, J., & Nemecek, T. (2018). *Reducing food's environmental impacts through producers and consumers*. Science, 360(6392), 987–992. | Static CO2e emission factors per kilogram of food category (Beef, Dairy, Poultry, Produce, Grains) |
| **USDA / BLS Food Waste Cost Benchmarks** | United States Department of Agriculture (USDA) Economic Research Service | Financial benchmark for calculating consumer money saved per kg of edible food rescued ($3.20/kg) |
| **FDA Major Food Allergens (FALCPA / FASTER Act) & EU 14 Allergens** | FDA & European Food Safety Authority (EFSA) | Structural foundation for the 14 global allergen classes and 450+ synonym ontology |
