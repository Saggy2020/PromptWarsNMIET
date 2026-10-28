import {
  Household,
  InventoryItem,
  Recipe,
  ShoppingList,
  SustainabilityMetrics,
  AuditLogEntry,
  MemberSafetyVerdict
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export async function fetchHousehold(householdId: string = 'demo-household-sharma'): Promise<Household> {
  const res = await fetch(`${API_BASE_URL}/api/household?household_id=${householdId}`);
  if (!res.ok) throw new Error('Failed to load household');
  return res.json();
}

export async function fetchInventory(householdId: string = 'demo-household-sharma'): Promise<InventoryItem[]> {
  const res = await fetch(`${API_BASE_URL}/api/inventory?household_id=${householdId}`);
  if (!res.ok) throw new Error('Failed to load inventory');
  return res.json();
}

export async function updateItemStatus(
  itemId: string,
  newStatus: 'in_stock' | 'consumed' | 'wasted',
  householdId: string = 'demo-household-sharma'
): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/inventory/${itemId}/status?household_id=${householdId}&new_status=${newStatus}`, {
    method: 'PUT'
  });
  if (!res.ok) throw new Error('Failed to update item status');
  return res.json();
}

export async function ingestReceiptText(rawText: string, householdId: string = 'demo-household-sharma'): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/intake/receipt`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ household_id: householdId, raw_text: rawText })
  });
  if (!res.ok) throw new Error('Failed to ingest receipt');
  return res.json();
}

export async function approveIntakeItems(items: any[], householdId: string = 'demo-household-sharma'): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/intake/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ household_id: householdId, items })
  });
  if (!res.ok) throw new Error('Failed to approve items');
  return res.json();
}

export async function generateMealPlan(householdId: string = 'demo-household-sharma'): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/plan/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ household_id: householdId, days: 7 })
  });
  if (!res.ok) throw new Error('Failed to generate meal plan');
  return res.json();
}

export async function checkSafetyVeto(
  recipeTitle: string,
  ingredients: string[],
  householdId: string = 'demo-household-sharma'
): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/safety/veto-check`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      household_id: householdId,
      recipe_title: recipeTitle,
      ingredients,
      sodium_mg: 500
    })
  });
  if (!res.ok) throw new Error('Failed to check safety veto');
  return res.json();
}

export async function fetchShoppingList(householdId: string = 'demo-household-sharma'): Promise<ShoppingList> {
  const res = await fetch(`${API_BASE_URL}/api/shopping?household_id=${householdId}`);
  if (!res.ok) throw new Error('Failed to load shopping list');
  return res.json();
}

export async function approveShoppingList(householdId: string = 'demo-household-sharma'): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/shopping/approve?household_id=${householdId}`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to approve shopping list');
  return res.json();
}

export async function fetchSustainability(householdId: string = 'demo-household-sharma'): Promise<SustainabilityMetrics> {
  const res = await fetch(`${API_BASE_URL}/api/sustainability/metrics?household_id=${householdId}`);
  if (!res.ok) throw new Error('Failed to load sustainability metrics');
  return res.json();
}

export async function fetchAuditLogs(householdId: string = 'demo-household-sharma'): Promise<AuditLogEntry[]> {
  const res = await fetch(`${API_BASE_URL}/api/privacy/audit-logs?household_id=${householdId}`);
  if (!res.ok) throw new Error('Failed to load audit logs');
  return res.json();
}

export async function sendChatMessage(message: string, householdId: string = 'demo-household-sharma'): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/assistant/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ household_id: householdId, message })
  });
  if (!res.ok) throw new Error('Failed to send message');
  return res.json();
}

export async function resetDemoHousehold(): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/demo/seed`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to reset demo household');
  return res.json();
}
