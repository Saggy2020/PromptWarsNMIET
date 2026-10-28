"""
Curated Food Shelf-Life Table and Carbon Emission Factors.
Emission benchmarks sourced from Poore & Nemecek, Science (2018).
"""

from typing import Dict, Tuple, Optional
from datetime import date, timedelta
from app.models.inventory import ItemCategory, ExpirySource

# Shelf-life in days (standard refrigerated or cool-pantry storage)
# Format: normalized_key -> (shelf_life_days, category, co2e_factor_kg, estimated_unit_cost_usd)
SHELF_LIFE_DATABASE: Dict[str, Tuple[int, ItemCategory, float, float]] = {
    # Fresh Produce (short shelf-life)
    "spinach": (4, ItemCategory.PRODUCE, 0.5, 2.50),
    "baby spinach": (4, ItemCategory.PRODUCE, 0.5, 2.99),
    "lettuce": (5, ItemCategory.PRODUCE, 0.4, 1.80),
    "cilantro": (5, ItemCategory.PRODUCE, 0.4, 0.99),
    "coriander": (5, ItemCategory.PRODUCE, 0.4, 0.99),
    "berries": (4, ItemCategory.PRODUCE, 1.1, 3.99),
    "strawberries": (4, ItemCategory.PRODUCE, 1.1, 3.99),
    "mushrooms": (5, ItemCategory.PRODUCE, 1.3, 2.70),
    "button mushrooms": (5, ItemCategory.PRODUCE, 1.3, 2.70),
    "tomatoes": (6, ItemCategory.PRODUCE, 1.4, 2.20),
    "bell pepper": (7, ItemCategory.PRODUCE, 0.8, 1.50),
    "capsicum": (7, ItemCategory.PRODUCE, 0.8, 1.50),
    "cucumber": (7, ItemCategory.PRODUCE, 0.6, 1.20),
    "broccoli": (6, ItemCategory.PRODUCE, 0.6, 2.10),
    "cauliflower": (7, ItemCategory.PRODUCE, 0.6, 2.30),
    "avocado": (5, ItemCategory.PRODUCE, 1.3, 1.99),
    "banana": (5, ItemCategory.PRODUCE, 0.8, 0.89),
    "apples": (21, ItemCategory.PRODUCE, 0.4, 3.50),
    "oranges": (14, ItemCategory.PRODUCE, 0.5, 3.20),
    "carrots": (21, ItemCategory.PRODUCE, 0.4, 1.60),
    "potatoes": (30, ItemCategory.PRODUCE, 0.5, 3.00),
    "onions": (30, ItemCategory.PRODUCE, 0.5, 2.20),
    "garlic": (60, ItemCategory.PRODUCE, 0.4, 1.50),
    
    # Dairy & Plant Milks
    "fresh milk": (7, ItemCategory.DAIRY, 3.2, 3.49),
    "whole milk": (7, ItemCategory.DAIRY, 3.2, 3.49),
    "milk": (7, ItemCategory.DAIRY, 3.2, 3.49),
    "skim milk": (7, ItemCategory.DAIRY, 3.0, 3.49),
    "oat milk": (10, ItemCategory.DAIRY, 0.9, 3.99),
    "almond milk": (10, ItemCategory.DAIRY, 0.7, 3.79),
    "soy milk": (10, ItemCategory.DAIRY, 1.0, 3.50),
    "greek yogurt": (12, ItemCategory.DAIRY, 3.8, 4.20),
    "yogurt": (10, ItemCategory.DAIRY, 3.5, 3.50),
    "cheddar cheese": (28, ItemCategory.DAIRY, 21.2, 5.50),
    "mozzarella": (14, ItemCategory.DAIRY, 18.0, 4.50),
    "paneer": (7, ItemCategory.DAIRY, 12.0, 4.00),
    "butter": (60, ItemCategory.DAIRY, 12.0, 4.50),
    
    # Proteins & Meat / Alternatives
    "fresh chicken breast": (3, ItemCategory.PROTEIN, 6.1, 7.99),
    "chicken": (3, ItemCategory.PROTEIN, 6.1, 7.50),
    "ground beef": (2, ItemCategory.PROTEIN, 60.0, 8.99),
    "beef": (3, ItemCategory.PROTEIN, 60.0, 11.50),
    "salmon": (2, ItemCategory.PROTEIN, 5.4, 9.99),
    "fish fillet": (2, ItemCategory.PROTEIN, 5.0, 8.50),
    "prawns": (2, ItemCategory.PROTEIN, 12.0, 10.50),
    "shrimp": (2, ItemCategory.PROTEIN, 12.0, 10.50),
    "organic tofu": (7, ItemCategory.PROTEIN, 2.0, 2.99),
    "tofu": (7, ItemCategory.PROTEIN, 2.0, 2.99),
    "eggs": (28, ItemCategory.PROTEIN, 4.5, 3.80),
    "paneer fresh": (7, ItemCategory.PROTEIN, 12.0, 4.00),
    "tempeh": (10, ItemCategory.PROTEIN, 2.1, 3.50),

    # Bakery
    "white bread": (5, ItemCategory.BAKERY, 1.3, 2.49),
    "sourdough bread": (5, ItemCategory.BAKERY, 1.3, 4.50),
    "whole wheat bread": (6, ItemCategory.BAKERY, 1.4, 3.00),
    "tortillas": (14, ItemCategory.BAKERY, 1.2, 2.80),
    
    # Pantry Staples (Long Shelf-Life)
    "brown rice": (180, ItemCategory.PANTRY, 2.7, 3.00),
    "white rice": (365, ItemCategory.PANTRY, 2.7, 2.50),
    "basmati rice": (365, ItemCategory.PANTRY, 2.7, 4.00),
    "pasta": (365, ItemCategory.PANTRY, 1.5, 1.80),
    "rolled oats": (180, ItemCategory.PANTRY, 1.6, 3.20),
    "lentils": (365, ItemCategory.PANTRY, 0.9, 2.20),
    "chickpeas": (365, ItemCategory.PANTRY, 0.9, 1.50),
    "canned beans": (730, ItemCategory.PANTRY, 1.1, 1.25),
    "olive oil": (365, ItemCategory.PANTRY, 6.0, 9.50),
    "peanut butter": (180, ItemCategory.PANTRY, 2.5, 3.50),
    "arachis oil": (365, ItemCategory.PANTRY, 4.0, 6.00)
}

def lookup_shelf_life(item_name: str, purchase_date: Optional[date] = None) -> Tuple[date, int, ItemCategory, float, float, ExpirySource]:
    """
    Returns (expiry_date, days_to_expiry, category, co2e_factor, cost, source)
    """
    if purchase_date is None:
        purchase_date = date.today()
        
    cleaned = item_name.strip().lower()
    
    # Direct match or substring match
    matched_entry = None
    for key, data in SHELF_LIFE_DATABASE.items():
        if key == cleaned or key in cleaned or cleaned in key:
            matched_entry = data
            break
            
    if matched_entry:
        days, category, co2e, cost = matched_entry
        expiry_date = purchase_date + timedelta(days=days)
        days_remaining = (expiry_date - date.today()).days
        return expiry_date, days_remaining, category, co2e, cost, ExpirySource.CURATED_TABLE
    else:
        # Heuristic fallback for uncataloged items
        days = 7
        category = ItemCategory.PANTRY
        co2e = 1.5
        cost = 3.00
        expiry_date = purchase_date + timedelta(days=days)
        days_remaining = (expiry_date - date.today()).days
        return expiry_date, days_remaining, category, co2e, cost, ExpirySource.AI_ESTIMATE
