"""
DETERMINISTIC Safety Guardian Rule Engine (Zero-LLM Veto).
Executes pure Python verification of candidate recipes against household allergen profiles
and medical contraindications. The LLM has ZERO veto removal authority.
"""

from typing import List, Dict, Tuple
from app.models.household import HouseholdMember, AllergenEnum, SeverityEnum, MedicalConditionEnum
from app.models.meal_plan import Recipe, MemberSafetyVerdict, SafetyStatus, RecipeIngredient
from app.safety.ontology import resolve_allergen

class SafetyGuardian:
    def __init__(self):
        pass

    def evaluate_ingredient(
        self,
        ingredient_name: str,
        member: HouseholdMember
    ) -> Tuple[SafetyStatus, List[str], List[str], bool]:
        """
        Evaluates a single ingredient string against a household member.
        Returns: (status, reasons, flagged_synonyms, is_vetoed)
        """
        reasons: List[str] = []
        flagged: List[str] = []
        is_vetoed = False
        status = SafetyStatus.SAFE

        # 1. Deterministic Allergen Check
        detected_allergens = resolve_allergen(ingredient_name)
        member_allergy_map = {a.allergen: a.severity for a in member.allergies}

        for allergen, matched_syn in detected_allergens:
            if allergen in member_allergy_map:
                severity = member_allergy_map[allergen]
                flagged.append(matched_syn)
                is_vetoed = True
                status = SafetyStatus.UNSAFE
                reasons.append(
                    f"FATAL ALLERGEN VETO: '{ingredient_name}' contains synonym '{matched_syn}' "
                    f"triggering {allergen.value.upper()} allergy ({severity.value}) for {member.name}."
                )

        # 2. Medical Contraindications Check
        text_lower = ingredient_name.lower()
        for condition in member.medical_conditions:
            if condition == MedicalConditionEnum.CELIAC_DISEASE:
                # Celiac disease requires strict 100% gluten-free
                gluten_matches = resolve_allergen(ingredient_name)
                for a, syn in gluten_matches:
                    if a == AllergenEnum.WHEAT_GLUTEN:
                        flagged.append(syn)
                        is_vetoed = True
                        status = SafetyStatus.UNSAFE
                        reasons.append(
                            f"MEDICAL VETO (Celiac Disease): '{ingredient_name}' contains gluten ({syn}) "
                            f"which is strictly prohibited for {member.name}."
                        )

            elif condition == MedicalConditionEnum.TYPE_2_DIABETES:
                high_gi_triggers = ["corn syrup", "high fructose", "refined sugar", "glucose syrup", "maltodextrin"]
                for trig in high_gi_triggers:
                    if trig in text_lower:
                        status = SafetyStatus.WARNING
                        reasons.append(
                            f"DIETARY WARNING (Diabetes): '{ingredient_name}' contains high-GI ingredient '{trig}'."
                        )

        # 3. Dietary Preferences (e.g. Vegetarian)
        for pref in member.dietary_preferences:
            if pref.lower() == "vegetarian":
                meat_triggers = ["chicken", "beef", "pork", "fish", "shrimp", "lamb", "bacon", "gelatin"]
                for m in meat_triggers:
                    if m in text_lower:
                        status = SafetyStatus.UNSAFE
                        is_vetoed = True
                        reasons.append(
                            f"PREFERENCE VETO (Vegetarian): '{ingredient_name}' contains meat/animal product '{m}'."
                        )

        return status, reasons, flagged, is_vetoed

    def evaluate_recipe(
        self,
        recipe_title: str,
        ingredients: List[RecipeIngredient],
        sodium_mg_per_serving: int,
        household_members: List[HouseholdMember]
    ) -> Tuple[SafetyStatus, List[MemberSafetyVerdict], bool]:
        """
        Evaluates an entire candidate recipe against all members of a household.
        Returns: (overall_status, member_verdicts, recipe_is_vetoed)
        """
        overall_status = SafetyStatus.SAFE
        member_verdicts: List[MemberSafetyVerdict] = []
        recipe_is_vetoed = False

        for member in household_members:
            member_status = SafetyStatus.SAFE
            member_reasons: List[str] = []
            member_flagged: List[str] = []
            member_is_vetoed = False

            # Check all ingredients
            for ing in ingredients:
                ing_status, reasons, flagged, veto = self.evaluate_ingredient(ing.name, member)
                if veto:
                    member_is_vetoed = True
                    member_status = SafetyStatus.UNSAFE
                elif ing_status == SafetyStatus.WARNING and member_status != SafetyStatus.UNSAFE:
                    member_status = SafetyStatus.WARNING

                member_reasons.extend(reasons)
                member_flagged.extend(flagged)

            # Check aggregate nutritional constraints (e.g. Sodium limit for Hypertension)
            if member.max_daily_sodium_mg and sodium_mg_per_serving > (member.max_daily_sodium_mg * 0.5):
                # If a single meal exceeds 50% of daily sodium allowance
                if member.max_daily_sodium_mg < 1500 and sodium_mg_per_serving > 750:
                    member_is_vetoed = True
                    member_status = SafetyStatus.UNSAFE
                    member_reasons.append(
                        f"SODIUM VETO (Hypertension): Recipe contains {sodium_mg_per_serving}mg sodium/serving, "
                        f"exceeding safe threshold (750mg) for {member.name}'s daily limit ({member.max_daily_sodium_mg}mg)."
                    )
                else:
                    if member_status != SafetyStatus.UNSAFE:
                        member_status = SafetyStatus.WARNING
                    member_reasons.append(
                        f"SODIUM WARNING: High sodium ({sodium_mg_per_serving}mg/serving) for {member.name}."
                    )

            if member_is_vetoed:
                recipe_is_vetoed = True
                overall_status = SafetyStatus.UNSAFE
            elif member_status == SafetyStatus.WARNING and overall_status != SafetyStatus.UNSAFE:
                overall_status = SafetyStatus.WARNING

            verdict = MemberSafetyVerdict(
                member_id=member.id,
                member_name=member.name,
                status=member_status,
                reasons=member_reasons,
                flagged_ingredients=list(set(member_flagged)),
                synonym_matched=", ".join(list(set(member_flagged))) if member_flagged else None,
                is_vetoed=member_is_vetoed
            )
            member_verdicts.append(verdict)

        return overall_status, member_verdicts, recipe_is_vetoed

# Global singleton instance
safety_guardian = SafetyGuardian()
