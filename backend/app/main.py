from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.config import settings
from app.api.intake_routes import router as intake_router
from app.api.inventory_routes import router as inventory_router
from app.api.household_routes import router as household_router
from app.api.safety_routes import router as safety_router
from app.api.plan_routes import router as plan_router
from app.api.shopping_routes import router as shopping_router
from app.api.sustainability_routes import router as sustainability_router
from app.api.assistant_routes import router as assistant_router
from app.api.privacy_routes import router as privacy_router
from app.api.demo_routes import router as demo_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Autonomous Multi-Agent Household Food Intelligence & Waste Reduction Platform"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers & Latency Middleware
@app.middleware("http")
async def add_security_headers_and_latency(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000.0
    
    # Constitution performance tracking header
    response.headers["X-Response-Time-Ms"] = f"{round(duration, 2)}"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Demo-Mode"] = "true" if settings.demo_mode else "false"
    
    return response

# Register Routers
app.include_router(intake_router)
app.include_router(inventory_router)
app.include_router(household_router)
app.include_router(safety_router)
app.include_router(plan_router)
app.include_router(shopping_router)
app.include_router(sustainability_router)
app.include_router(assistant_router)
app.include_router(privacy_router)
app.include_router(demo_router)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "demo_mode": settings.demo_mode,
        "models": {
            "flash": settings.gemini_flash_model,
            "pro": settings.gemini_pro_model
        }
    }

@app.get("/")
async def root():
    return {
        "message": "Welcome to PantryPilot Autonomous Food Intelligence API",
        "docs": "/docs",
        "health": "/api/health",
        "demo_mode": settings.demo_mode
    }
