"""
Mock LLM Provider for Zero-Credential Demo Mode & Offline CI Testing.
Generates realistic, schema-compliant multimodal extraction and meal plan responses
without requiring external network requests or Google Cloud API keys.
"""

import json
from typing import Dict, Any, List

class MockLLMProvider:
    @staticmethod
    def mock_vision_receipt_extraction(raw_text: str = "") -> Dict[str, Any]:
        """
        Simulates Gemini 2.5 Flash receipt entity extraction.
        """
        # If user provided raw text, parse lines, else return realistic supermarket basket
        items = []
        if raw_text and len(raw_text.strip()) > 5:
            lines = [l.strip() for l in raw_text.strip().split("\n") if l.strip()]
            for line in lines[:8]:
                items.append({
                    "name": line,
                    "category": "produce" if "spinach" in line.lower() or "apple" in line.lower() else "pantry",
                    "quantity": 1.0,
                    "unit": "pcs",
                    "confidence": 0.96
                })
        else:
            items = [
                {
                    "name": "Fresh Organic Spinach",
                    "category": "produce",
                    "quantity": 250.0,
                    "unit": "g",
                    "confidence": 0.98
                },
                {
                    "name": "Organic Firm Tofu",
                    "category": "protein",
                    "quantity": 400.0,
                    "unit": "g",
                    "confidence": 0.95
                },
                {
                    "name": "Red Bell Pepper",
                    "category": "produce",
                    "quantity": 2.0,
                    "unit": "pcs",
                    "confidence": 0.94
                },
                {
                    "name": "Greek Yogurt Tub",
                    "category": "dairy",
                    "quantity": 500.0,
                    "unit": "g",
                    "confidence": 0.97
                },
                {
                    "name": "Arachis Groundnut Cooking Oil",
                    "category": "pantry",
                    "quantity": 500.0,
                    "unit": "ml",
                    "confidence": 0.93
                }
            ]

        return {
            "merchant": "WholeFoods Market / Supermarket",
            "date": "2026-10-23",
            "currency": "USD",
            "items": items,
            "tokens_used": 340,
            "latency_ms": 780.0
        }

    @staticmethod
    def mock_meal_planning(expiring_items: List[str]) -> List[Dict[str, Any]]:
        """
        Simulates Gemini 2.5 Pro constrained meal planning.
        Intentionally includes candidate recipes designed to trigger safety engine validation.
        """
        return [
            # Candidate 1: SAFE waste-minimizing stir-fry
            {
                "title": "Golden Tofu & Spinach Wok Stir-Fry",
                "description": "Quick high-protein stir-fry utilizing soon-to-expire spinach and organic firm tofu.",
                "prep_time_minutes": 20,
                "servings": 4,
                "estimated_calories_per_serving": 380,
                "sodium_mg_per_serving": 420,
                "waste_reduction_score": 92.0,
                "expiring_items_used": ["Fresh Baby Spinach", "Organic Firm Tofu", "Red Bell Pepper"],
                "ingredients": [
                    {"name": "Organic Firm Tofu", "quantity": 400.0, "unit": "g"},
                    {"name": "Fresh Baby Spinach", "quantity": 200.0, "unit": "g"},
                    {"name": "Red Bell Pepper", "quantity": 1.0, "unit": "pcs"},
                    {"name": "Gluten-Free Tamari Soy Sauce", "quantity": 30.0, "unit": "ml"},
                    {"name": "Olive Oil", "quantity": 15.0, "unit": "ml"},
                    {"name": "Organic Brown Basmati Rice", "quantity": 200.0, "unit": "g"}
                ],
                "instructions": [
                    "Press and cube the firm tofu; sauté in olive oil until golden brown.",
                    "Slice the bell pepper and toss into the wok for 3 minutes.",
                    "Add fresh baby spinach and stir until wilted.",
                    "Season with gluten-free tamari and serve hot over steamed brown rice."
                ],
                "explainability_rationale": "Rescues 3 items expiring within 3 days. Formulated with gluten-free tamari to accommodate Maya (Celiac) and kept sodium at 420mg for Aarav (Hypertension)."
            },
            # Candidate 2: UNSAFE recipe containing peanut synonym (Arachis oil) - Test case for Deterministic Veto
            {
                "title": "Crispy Tofu Satay with Arachis Dressing",
                "description": "Rich savory dish using pantry arachis oil dressing.",
                "prep_time_minutes": 25,
                "servings": 4,
                "estimated_calories_per_serving": 490,
                "sodium_mg_per_serving": 820,
                "waste_reduction_score": 60.0,
                "expiring_items_used": ["Organic Firm Tofu"],
                "ingredients": [
                    {"name": "Organic Firm Tofu", "quantity": 400.0, "unit": "g"},
                    {"name": "Arachis Oil", "quantity": 30.0, "unit": "ml"},
                    {"name": "Regular Soy Sauce", "quantity": 40.0, "unit": "ml"}
                ],
                "instructions": [
                    "Marinate tofu in arachis oil and soy sauce, pan fry until crisp."
                ],
                "explainability_rationale": "Proposed candidate containing arachis oil; intentionally subjected to deterministic safety vetting."
            },
            # Candidate 3: SAFE Mediterranean Stew
            {
                "title": "Rustic Mushroom & Spinach Rice Bowl",
                "description": "Wholesome gluten-free, vegan bowl packed with antioxidants and fiber.",
                "prep_time_minutes": 25,
                "servings": 4,
                "estimated_calories_per_serving": 350,
                "sodium_mg_per_serving": 380,
                "waste_reduction_score": 85.0,
                "expiring_items_used": ["Button Mushrooms", "Fresh Baby Spinach"],
                "ingredients": [
                    {"name": "Button Mushrooms", "quantity": 250.0, "unit": "g"},
                    {"name": "Fresh Baby Spinach", "quantity": 100.0, "unit": "g"},
                    {"name": "Organic Brown Basmati Rice", "quantity": 200.0, "unit": "g"},
                    {"name": "Olive Oil", "quantity": 15.0, "unit": "ml"},
                    {"name": "Garlic", "quantity": 2.0, "unit": "pcs"}
                ],
                "instructions": [
                    "Sauté minced garlic and sliced button mushrooms in olive oil until caramelized.",
                    "Fold in baby spinach until tender.",
                    "Combine with cooked brown rice and season lightly with black pepper."
                ],
                "explainability_rationale": "Rescues expiring mushrooms and spinach. 100% allergen-free, low-sodium (380mg), and vegetarian-compliant."
            }
        ]

mock_provider = MockLLMProvider()
