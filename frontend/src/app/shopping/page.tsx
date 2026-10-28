'use client';

import React, { useEffect, useState } from 'react';
import { ShoppingBag, CheckCircle2, ShieldCheck, Tag, ArrowRight } from 'lucide-react';
import { fetchShoppingList, approveShoppingList } from '../../lib/api';
import { ShoppingList, ShoppingItem } from '../../lib/types';

export default function ShoppingPage() {
  const [shoppingList, setShoppingList] = useState<ShoppingList | null>(null);
  const [loading, setLoading] = useState(true);
  const [approved, setApproved] = useState(false);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchShoppingList();
        setShoppingList(data);
        setApproved(data.approved_by_user);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleApprove = async () => {
    try {
      await approveShoppingList();
      setApproved(true);
    } catch (e) {
      alert('Error approving shopping list');
    }
  };

  // Group by category/aisle
  const groupedItems: { [cat: string]: ShoppingItem[] } = {};
  shoppingList?.items?.forEach((item) => {
    const cat = item.category || 'Pantry';
    if (!groupedItems[cat]) groupedItems[cat] = [];
    groupedItems[cat].push(item);
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <ShoppingBag className="w-5 h-5 text-emerald-600" /> Smart Procurement & Aisle Shopping List
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Diffs approved meal plans against live pantry so you only buy what is missing, with safe substitutions.
          </p>
        </div>

        <div className="text-right">
          <span className="text-xs text-slate-400 block">Est. Grocery Spend</span>
          <span className="text-2xl font-black text-slate-900">
            ${shoppingList?.total_estimated_cost.toFixed(2) || '0.00'}
          </span>
        </div>
      </div>

      {/* Human in the loop confirmation banner */}
      <div className="bg-emerald-50 border border-emerald-300 rounded-2xl p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div className="flex items-center gap-2 text-emerald-900 text-xs">
          <ShieldCheck className="w-5 h-5 text-emerald-600 flex-shrink-0" />
          <span>
            <strong>Human-in-the-Loop Gate:</strong> Autonomous agents proposed this replenishment list. Explicit user confirmation is required before final checkout.
          </span>
        </div>
        {!approved ? (
          <button
            onClick={handleApprove}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-1.5 shadow-sm"
          >
            <CheckCircle2 className="w-4 h-4" /> Approve Shopping List
          </button>
        ) : (
          <span className="px-3 py-1.5 bg-emerald-200 text-emerald-900 rounded-lg text-xs font-bold flex items-center gap-1">
            <CheckCircle2 className="w-4 h-4 text-emerald-700" /> Approved by User
          </span>
        )}
      </div>

      {/* Aisle Grouped List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {Object.entries(groupedItems).map(([category, items]) => (
          <div key={category} className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
            <h3 className="font-extrabold text-xs uppercase tracking-wider text-slate-500 border-b pb-2 flex items-center justify-between">
              <span>{category} Department</span>
              <span className="text-[11px] font-mono text-slate-400">{items.length} items</span>
            </h3>

            <div className="divide-y divide-slate-100">
              {items.map((item) => (
                <div key={item.id} className="py-2.5 flex flex-col gap-1">
                  <div className="flex justify-between items-center text-xs">
                    <span className="font-semibold text-slate-800">{item.name}</span>
                    <span className="font-bold text-slate-900">${item.estimated_cost.toFixed(2)}</span>
                  </div>
                  <div className="text-[11px] text-slate-400">
                    Needed: {item.quantity} {item.unit} for {item.recipe_references.join(', ')}
                  </div>
                  {item.safe_substitutes.length > 0 && (
                    <div className="text-[11px] text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200 inline-block w-fit mt-1">
                      Safe Allergen Alternative: {item.safe_substitutes.join(', ')}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}

        {Object.keys(groupedItems).length === 0 && (
          <div className="col-span-2 text-center py-12 text-slate-400 text-xs bg-white rounded-2xl border">
            No missing ingredients! Your current live pantry fulfills all approved recipes.
          </div>
        )}
      </div>
    </div>
  );
}
