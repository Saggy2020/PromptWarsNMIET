export interface MemberAllergy {
  allergen: string;
  severity: string;
  notes?: string;
}

export interface HouseholdMember {
  id: string;
  name: string;
  role: string;
  allergies: MemberAllergy[];
  medical_conditions: string[];
  dietary_preferences: string[];
  daily_calorie_target?: number;
  max_daily_sodium_mg?: number;
}

export interface Household {
  id: string;
  name: string;
  currency: string;
  created_at: string;
  members: HouseholdMember[];
}

export interface InventoryItem {
  id: string;
  household_id: string;
  name: string;
  normalized_name: string;
  category: string;
  quantity: number;
  unit: string;
  purchase_date: string;
  expiry_date: string;
  days_to_expiry: number;
  expiry_source: string;
  status: 'in_stock' | 'consumed' | 'wasted';
  estimated_cost: number;
  co2e_factor_kg: number;
}

export interface MemberSafetyVerdict {
  member_id: string;
  member_name: string;
  status: 'safe' | 'warning' | 'unsafe';
  reasons: string[];
  flagged_ingredients: string[];
  synonym_matched?: string;
  is_vetoed: boolean;
}

export interface RecipeIngredient {
  name: string;
  quantity: number;
  unit: string;
}

export interface Recipe {
  id: string;
  title: string;
  description: string;
  ingredients: RecipeIngredient[];
  instructions: string[];
  prep_time_minutes: number;
  servings: number;
  estimated_calories_per_serving: number;
  sodium_mg_per_serving: number;
  waste_reduction_score: number;
  expiring_items_used: string[];
  member_verdicts: MemberSafetyVerdict[];
  overall_safety: 'safe' | 'warning' | 'unsafe';
  explainability_rationale: string;
}

export interface ShoppingItem {
  id: string;
  name: string;
  category: string;
  quantity: number;
  unit: string;
  estimated_cost: number;
  recipe_references: string[];
  is_purchased: boolean;
  safe_substitutes: string[];
}

export interface ShoppingList {
  id: string;
  household_id: string;
  items: ShoppingItem[];
  total_estimated_cost: number;
  requires_approval: boolean;
  approved_by_user: boolean;
}

export interface SustainabilityMetrics {
  household_id: string;
  waste_avoided_kg: number;
  co2e_avoided_kg: number;
  money_saved_usd: number;
  meals_planned_count: number;
  safety_vetoes_prevented: number;
  projected_waste_reduction_percent: number;
  equivalencies: {
    car_km_avoided: number;
    tree_seedling_days: number;
  };
  methodology_note: string;
  last_updated: string;
}

export interface AuditLogEntry {
  id: string;
  correlation_id: string;
  household_id: string;
  agent_name: string;
  action: string;
  input_summary: string;
  output_summary: string;
  safety_veto_applied: boolean;
  tokens_used: number;
  latency_ms: number;
  cost_usd: number;
  timestamp: string;
}
