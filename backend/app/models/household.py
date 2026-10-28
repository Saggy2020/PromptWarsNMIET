from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class RoleEnum(str, Enum):
    OWNER = "owner"
    MEMBER = "member"
    VIEWER = "viewer"

class AllergenEnum(str, Enum):
    PEANUTS = "peanuts"
    TREE_NUTS = "tree_nuts"
    DAIRY = "dairy"
    EGGS = "eggs"
    WHEAT_GLUTEN = "wheat_gluten"
    SOY = "soy"
    FISH = "fish"
    SHELLFISH = "shellfish"
    SESAME = "sesame"
    MUSTARD = "mustard"
    CELERY = "celery"
    SULPHITES = "sulphites"
    LUPIN = "lupin"
    MOLLUSCS = "molluscs"

class SeverityEnum(str, Enum):
    MILD_INTOLERANCE = "mild_intolerance"
    MODERATE_ALLERGY = "moderate_allergy"
    SEVERE_ANAPHYLAXIS = "severe_anaphylaxis"

class MemberAllergy(BaseModel):
    allergen: AllergenEnum
    severity: SeverityEnum = SeverityEnum.SEVERE_ANAPHYLAXIS
    notes: Optional[str] = None

class MedicalConditionEnum(str, Enum):
    HYPERTENSION = "hypertension"
    TYPE_2_DIABETES = "type_2_diabetes"
    CELIAC_DISEASE = "celiac_disease"
    CHRONIC_KIDNEY_DISEASE = "chronic_kidney_disease"
    GERD = "gerd"

class HouseholdMember(BaseModel):
    id: str = Field(..., description="Unique member UUID")
    name: str = Field(..., min_length=1, max_length=50)
    role: RoleEnum = RoleEnum.MEMBER
    allergies: List[MemberAllergy] = Field(default_factory=list)
    medical_conditions: List[MedicalConditionEnum] = Field(default_factory=list)
    dietary_preferences: List[str] = Field(default_factory=list) # e.g. "vegetarian", "vegan", "halal"
    daily_calorie_target: Optional[int] = Field(None, ge=800, le=5000)
    max_daily_sodium_mg: Optional[int] = Field(None, ge=500, le=5000)

class Household(BaseModel):
    id: str = Field(..., description="Unique household UUID")
    name: str = Field(..., min_length=2, max_length=100)
    currency: str = Field("USD", max_length=3)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    members: List[HouseholdMember] = Field(default_factory=list)
