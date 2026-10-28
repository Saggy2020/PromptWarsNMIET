# PantryPilot: Quickstart & Evaluation Guide

**Feature**: `001-autonomous-food-intelligence`  
**Date**: 2026-10-23  
**Status**: Ready for Execution

---

## 1. Quick Launch (Zero-Credential Demo Mode)

PantryPilot includes a complete, self-contained **Demo Mode** designed specifically for hackathon evaluators. You do NOT need any Google Cloud API keys or external credentials to run the full application and test suites.

### 1.1 Backend Setup (FastAPI & Deterministic Engine)
```powershell
# Navigate to backend
cd backend

# Create virtual environment with uv or python
uv venv
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Run backend in Demo Mode
$env:DEMO_MODE = "true"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be live at `http://localhost:8000`.  
Interactive API Swagger Docs: `http://localhost:8000/docs`.

### 1.2 Frontend Setup (Next.js & Tailwind)
```powershell
# Navigate to frontend in a new terminal
cd frontend

# Install dependencies
npm install

# Run frontend development server
npm run dev
```

Frontend will be live at `http://localhost:3000`.

---

## 2. 3-Minute Demo Script for Judges

1. **Open Dashboard (`http://localhost:3000`)**:
   - Notice the prominent **Demo Mode** banner.
   - Pre-seeded household "The Sharma Household" loads with 3 members:
     - **Aarav**: Severe peanut allergy & hypertension (< 1500mg sodium).
     - **Maya**: Celiac disease (strict 100% gluten-free).
     - **Rohan**: Vegetarian, high-protein target (90g/day).

2. **Multimodal Intake**:
   - Navigate to **"Grocery Intake"**.
   - Click **"Load Sample Supermarket Receipt"** (or upload an image).
   - Watch the Vision Intake Agent extract:
     - Fresh Spinach (expiring in 2 days)
     - Organic Tofu (expiring in 3 days)
     - Greek Yogurt, Bell Peppers, and Arachis Oil (flagged).
   - Review extracted items, click **"Confirm & Commit to Inventory"**.

3. **Deterministic Safety Veto in Action**:
   - Navigate to **"Meal Planner"**.
   - Click **"Generate Waste-Minimizing Meal Plan"**.
   - Observe the agent status bar: `[Vision Intake] -> [Meal Planner] -> [Safety Guardian]`.
   - **Crucial Demo**: The AI proposes a "Crispy Tofu Satay Bowl".
   - The **Deterministic Safety Guardian** intercepts:
     - 🛑 **VETO TRIGGERED**: "Arachis oil" resolves to PEANUTS $\rightarrow$ Aarav is at risk!
     - 🛑 **SODIUM WARNING**: Recipe sodium exceeds daily target.
     - Notice: The recipe is automatically disqualified from the plan, and the UI displays the exact synonym and veto explanation.
   - The system substitutes a safe "Sesame-Free Green Tofu Stir-fry" utilizing the expiring spinach and bell peppers.

4. **Procurement & Human-in-the-Loop Shopping List**:
   - View the generated shopping list. Only 2 missing staples are added (Soy Sauce - Gluten-Free Tamari for Maya, Brown Rice).
   - Click **"Approve Shopping List"**.

5. **Sustainability & Telemetry Metrics**:
   - Navigate to **"Impact Dashboard"**.
   - Inspect the real-time calculated metrics:
     - **Food Waste Avoided**: ~4.2 kg (expiring spinach, tofu, yogurt used before spoilage).
     - **CO2e Avoided**: ~8.8 kg CO2e (computed with Poore & Nemecek factors).
     - **Cost Saved**: \$14.50.
   - Click **"View Telemetry & Audit Logs"** to see exact token counts, model routing breakdown (Flash vs Pro), and response latency.

---

## 3. Running Automated Tests & Eval Suites

```powershell
cd backend

# Run Unit & Integration Tests (Safety Engine, Schemas, Endpoints)
pytest tests/ -v

# Run the Deterministic Allergen Safety Eval (Zero False Negatives Target)
python -m evals.run_safety_suite

# Run Adversarial Prompt Injection Defense Benchmark
python -m evals.run_injection_suite

# Run Golden Receipt Extraction Benchmark (F1 Score Target >= 0.90)
python -m evals.run_golden_eval
```
All evaluation results are automatically computed and written to `METRICS.md`.
