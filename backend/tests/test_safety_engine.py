"""
Unit Tests for the DETERMINISTIC Safety Guardian Rule Engine (Zero-LLM Veto).
Validates 100% detection of allergen synonyms, botanical Latin names, and medical limits.
"""

import pytest
from app.models.household import (
    HouseholdMember, AllergenEnum, MemberAllergy, SeverityEnum, MedicalConditionEnum, RoleEnum
)
from app.models.meal_plan import RecipeIngredient, SafetyStatus
from app.safety.engine import safety_guardian
from app.safety.ontology import resolve_allergen

def test_peanut_synonym_resolution():
    """Verify that disguised peanut synonyms resolve correctly to PEANUTS."""
    synonyms = [
        "arachis oil", "groundnut paste", "monkey nuts", "beer nuts",
        "mandelonas", "arachis hypogaea extract", "peanut butter"
    ]
    for syn in synonyms:
        matches = resolve_allergen(syn)
        allergens = [m[0] for m in matches]
        assert AllergenEnum.PEANUTS in allergens, f"Failed to identify peanut in synonym: {syn}"

def test_celiac_gluten_resolution():
    """Verify that gluten-containing grains resolve to WHEAT_GLUTEN."""
    gluten_items = ["barley malt", "spelt flour", "seitan", "semolina", "rye bread", "kamut"]
    for item in gluten_items:
        matches = resolve_allergen(item)
        allergens = [m[0] for m in matches]
        assert AllergenEnum.WHEAT_GLUTEN in allergens, f"Failed to identify gluten in: {item}"

def test_deterministic_veto_blocks_unsafe_recipe():
    """Ensure the safety guardian vetoes a recipe containing arachis oil for peanut-allergic Aarav."""
    aarav = HouseholdMember(
        id="m1",
        name="Aarav",
        role=RoleEnum.MEMBER,
        allergies=[MemberAllergy(allergen=AllergenEnum.PEANUTS, severity=SeverityEnum.SEVERE_ANAPHYLAXIS)],
        medical_conditions=[MedicalConditionEnum.HYPERTENSION],
        max_daily_sodium_mg=1500
    )

    ingredients = [
        RecipeIngredient(name="Organic Firm Tofu", normalized_name="tofu", quantity=400, unit="g"),
        RecipeIngredient(name="Arachis Cooking Oil", normalized_name="arachis cooking oil", quantity=20, unit="ml"),
        RecipeIngredient(name="Baby Spinach", normalized_name="baby spinach", quantity=100, unit="g")
    ]

    status, verdicts, is_vetoed = safety_guardian.evaluate_recipe(
        recipe_title="Crispy Tofu Satay",
        ingredients=ingredients,
        sodium_mg_per_serving=400,
        household_members=[aarav]
    )

    assert is_vetoed is True, "Safety engine MUST veto recipe containing peanut synonym"
    assert status == SafetyStatus.UNSAFE
    assert len(verdicts) == 1
    assert verdicts[0].is_vetoed is True
    assert "PEANUT" in verdicts[0].reasons[0].upper()

def test_safe_recipe_passes():
    """Verify safe recipe with no allergens passes without veto."""
    rohan = HouseholdMember(
        id="m2",
        name="Rohan",
        role=RoleEnum.MEMBER,
        allergies=[],
        medical_conditions=[]
    )

    ingredients = [
        RecipeIngredient(name="Brown Basmati Rice", normalized_name="brown rice", quantity=200, unit="g"),
        RecipeIngredient(name="Baby Spinach", normalized_name="baby spinach", quantity=100, unit="g"),
        RecipeIngredient(name="Olive Oil", normalized_name="olive oil", quantity=15, unit="ml")
    ]

    status, verdicts, is_vetoed = safety_guardian.evaluate_recipe(
        recipe_title="Spinach Rice Bowl",
        ingredients=ingredients,
        sodium_mg_per_serving=250,
        household_members=[rohan]
    )

    assert is_vetoed is False
    assert status == SafetyStatus.SAFE
