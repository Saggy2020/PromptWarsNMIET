"""
Integration tests for PantryPilot FastAPI routes using TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["demo_mode"] is True

def test_get_household():
    res = client.get("/api/household?household_id=demo-household-sharma")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "The Sharma Household"
    assert len(data["members"]) == 3

def test_get_inventory():
    res = client.get("/api/inventory?household_id=demo-household-sharma")
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 4
    # Check that spinach is present
    names = [i["name"].lower() for i in items]
    assert any("spinach" in n for n in names)

def test_generate_meal_plan():
    res = client.post("/api/plan/generate", json={
        "household_id": "demo-household-sharma",
        "days": 7
    })
    assert res.status_code == 200
    data = res.json()
    assert "recipes" in data
    assert len(data["recipes"]) >= 1
    # Check that all returned recipes are safe
    for r in data["recipes"]:
        assert r["overall_safety"] in ("safe", "warning")
        for verdict in r["member_verdicts"]:
            assert verdict["is_vetoed"] is False

def test_deterministic_veto_endpoint():
    # Submit unsafe recipe containing arachis oil
    res = client.post("/api/safety/veto-check", json={
        "household_id": "demo-household-sharma",
        "recipe_title": "Arachis Satay",
        "ingredients": ["tofu", "arachis oil", "salt"],
        "sodium_mg": 400
    })
    assert res.status_code == 200
    data = res.json()
    assert data["is_vetoed"] is True
    assert data["overall_status"] == "unsafe"

def test_sustainability_metrics():
    res = client.get("/api/sustainability/metrics?household_id=demo-household-sharma")
    assert res.status_code == 200
    data = res.json()
    assert data["waste_avoided_kg"] > 0
    assert data["co2e_avoided_kg"] > 0
    assert "methodology_note" in data
