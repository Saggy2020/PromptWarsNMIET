"""
Allergen Ontology Graph and Ingredient Synonym Dictionary.
Covers 14 major global allergen classes (FDA Top 9 + EU 14) with botanical Latin names,
derivatives, regional culinary terms, and cross-contamination triggers.
"""

from typing import Dict, List, Set
from app.models.household import AllergenEnum

# Synonym dictionary mapping normalized lowercase ingredient tokens to AllergenEnum
ALLERGEN_ONTOLOGY: Dict[AllergenEnum, Set[str]] = {
    AllergenEnum.PEANUTS: {
        "peanut", "peanuts", "groundnut", "groundnuts", "arachis", "arachis hypogaea",
        "arachis oil", "peanut oil", "peanut butter", "peanut flour", "beer nut", "beer nuts",
        "monkey nut", "monkey nuts", "mandelonas", "valencia peanut", "runner peanut",
        "spanish peanut", "goober", "goobers", "goober pea", "ground pea"
    },
    AllergenEnum.TREE_NUTS: {
        "tree nut", "tree nuts", "almond", "almonds", "cashew", "cashews", "walnut", "walnuts",
        "pecan", "pecans", "pistachio", "pistachios", "hazelnut", "hazelnuts", "filbert", "filberts",
        "macadamia", "macadamia nut", "brazil nut", "brazil nuts", "pine nut", "pine nuts",
        "pignoli", "piñon", "chestnut", "chestnuts", "marzipan", "praline", "frangipane",
        "gianduja", "nougat", "nutella", "pesto", "nut butter", "almond flour", "almond meal",
        "cashew milk", "almond milk", "macadamia oil", "walnut oil"
    },
    AllergenEnum.DAIRY: {
        "milk", "dairy", "cow milk", "goat milk", "sheep milk", "whole milk", "skim milk",
        "cream", "heavy cream", "sour cream", "butter", "buttermilk", "ghee", "clarified butter",
        "cheese", "cheddar", "mozzarella", "parmesan", "feta", "brie", "ricotta", "paneer",
        "curd", "curds", "cottage cheese", "yogurt", "yoghurt", "greek yogurt", "dahi",
        "casein", "caseinate", "calcium caseinate", "sodium caseinate", "whey", "whey protein",
        "whey powder", "lactalbumin", "lactoglobulin", "lactose", "milk solids", "milk powder",
        "condensed milk", "evaporated milk", "khoa", "khoya", "mawa", "custard", "gelato"
    },
    AllergenEnum.EGGS: {
        "egg", "eggs", "egg white", "egg yolk", "albumin", "albumen", "ovalbumin", "ovomucin",
        "ovomucoid", "ovovitellin", "livetin", "lysozyme", "mayonnaise", "mayo", "meringue",
        "hollandaise", "béarnaise", "eggnog", "surimi", "lecithin (egg)", "egg powder"
    },
    AllergenEnum.WHEAT_GLUTEN: {
        "wheat", "gluten", "wheat flour", "all-purpose flour", "whole wheat", "white flour",
        "bread flour", "durum", "semolina", "spelt", "kamut", "farro", "emmer", "einkorn",
        "bulgur", "couscous", "cracked wheat", "wheat bran", "wheat germ", "wheat starch",
        "barley", "barley malt", "malt", "malt extract", "malt syrup", "malt vinegar",
        "rye", "rye flour", "rye bread", "triticale", "seitan", "vital wheat gluten",
        "atta", "maida", "sooji", "suji", "rava", "wheat grass", "matzo", "fu"
    },
    AllergenEnum.SOY: {
        "soy", "soya", "soybean", "soybeans", "edamame", "tofu", "silken tofu", "firm tofu",
        "tempeh", "miso", "natto", "tamari", "soy sauce", "shoyu", "soy milk", "soy protein",
        "soy isolate", "soy lecithin", "textured vegetable protein", "tvp", "soya chunks",
        "bean curd", "yuba", "soy flour", "soya oil"
    },
    AllergenEnum.FISH: {
        "fish", "salmon", "tuna", "cod", "tilapia", "trout", "halibut", "haddock", "mackerel",
        "sardine", "sardines", "anchovy", "anchovies", "bass", "snapper", "flounder", "sole",
        "pollock", "swordfish", "catfish", "fish sauce", "worcestershire sauce", "dashi",
        "caviar", "roe", "surimi", "bonito", "bonito flakes", "isinglass"
    },
    AllergenEnum.SHELLFISH: {
        "shellfish", "crustacean", "crustaceans", "shrimp", "shrimps", "prawn", "prawns",
        "lobster", "langoustine", "scampi", "crab", "crabs", "crawfish", "crayfish",
        "krill", "shrimp paste", "belacan"
    },
    AllergenEnum.SESAME: {
        "sesame", "sesame seed", "sesame seeds", "sesame oil", "tahini", "tahina", "til",
        "gingelly", "gingelly oil", "halvah", "halva", "hummus with tahini", "benne",
        "benne seed", "gomasio", "sesamum indicum"
    },
    AllergenEnum.MUSTARD: {
        "mustard", "mustard seed", "mustard seeds", "mustard oil", "mustard greens",
        "mustard flour", "mustard powder", "dijon", "dijon mustard", "senf", "moutarde",
        "sinapis alba", "brassica nigra"
    },
    AllergenEnum.CELERY: {
        "celery", "celery stick", "celery root", "celeriac", "celery salt", "celery seed",
        "apium graveolens"
    },
    AllergenEnum.SULPHITES: {
        "sulphite", "sulphites", "sulfite", "sulfites", "sulfur dioxide", "sodium sulphite",
        "sodium bisulphite", "potassium metabisulphite", "e220", "e221", "e222", "e223", "e224"
    },
    AllergenEnum.LUPIN: {
        "lupin", "lupine", "lupin flour", "lupin seed", "lupinus"
    },
    AllergenEnum.MOLLUSCS: {
        "mollusc", "molluscs", "mollusk", "mollusks", "clam", "clams", "mussel", "mussels",
        "oyster", "oysters", "scallop", "scallops", "squid", "calamari", "octopus", "cuttlefish",
        "snail", "snails", "escargot", "whelk", "abalone"
    }
}

# Inverted mapping: token -> AllergenEnum for O(1) matching
INVERTED_ALLERGEN_MAP: Dict[str, AllergenEnum] = {}
for allergen, synonyms in ALLERGEN_ONTOLOGY.items():
    for syn in synonyms:
        INVERTED_ALLERGEN_MAP[syn.lower().strip()] = allergen

import re

def resolve_allergen(ingredient_text: str) -> List[tuple[AllergenEnum, str]]:
    """
    Scans ingredient string for any matching allergen synonyms or derivatives.
    Returns list of (AllergenEnum, matched_synonym).
    """
    text = ingredient_text.lower().strip()
    detected = []
    
    # Check if explicitly certified/labeled allergen-free (e.g. gluten-free)
    is_gluten_free = "gluten-free" in text or "gluten free" in text
    
    # Check exact match or word boundary in normalized token
    for syn, allergen in INVERTED_ALLERGEN_MAP.items():
        if allergen == AllergenEnum.WHEAT_GLUTEN and is_gluten_free and syn in ("gluten", "wheat"):
            continue

        # Prevent subword false positives for short tokens (<=4 chars) like 'fu' in 'tofu' or 'egg' in 'veggie'
        if len(syn) <= 4:
            pattern = rf'\b{re.escape(syn)}s?\b'
            if re.search(pattern, text):
                if syn == "nut" and ("coconut" in text or "butternut" in text):
                    continue
                detected.append((allergen, syn))
        else:
            if syn in text:
                if syn == "tree nut" and ("coconut" in text or "butternut" in text):
                    continue
                detected.append((allergen, syn))
            
    return detected
