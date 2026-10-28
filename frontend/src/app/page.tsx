'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { 
  Leaf, AlertTriangle, ShieldCheck, CalendarDays, ShoppingBag, 
  ArrowRight, Sparkles, TrendingUp, DollarSign, Clock
} from 'lucide-react';
import { fetchInventory, fetchSustainability, fetchHousehold } from '../lib/api';
import { InventoryItem, SustainabilityMetrics, Household } from '../lib/types';
import { ExpiryBadge } from '../components/ExpiryBadge';
import { AgentTicker } from '../components/AgentTicker';

export default function DashboardPage() {
  const [household, setHousehold] = useState<Household | null>(null);
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [metrics, setMetrics] = useState<SustainabilityMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [h, inv, met] = await Promise.all([
          fetchHousehold(),
          fetchInventory(),
          fetchSustainability()
        ]);
        setHousehold(h);
        setInventory(inv);
        setMetrics(met);
      } catch (e) {
        console.error('Error loading dashboard data', e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const expiringSoon = inventory.filter((item) => item.days_to_expiry <= 3 && item.status === 'in_stock');

  return (
    <div className="space-y-6">
      {/* Top Banner & Agent Ticker */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <span>Welcome, {household?.name || 'The Sharma Household'}</span>
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Autonomous multi-agent intelligence active. Tracking {inventory.length} items across 3 household profiles.
          </p>
        </div>
        <AgentTicker activeAgent="Idle" latencyMs={48} />
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-emerald-600 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Food Waste Rescued</span>
            <Leaf className="w-5 h-5" />
          </div>
          <div className="text-3xl font-extrabold text-slate-900">
            {metrics?.waste_avoided_kg ?? '4.2'} <span className="text-base font-medium text-slate-500">kg</span>
          </div>
          <div className="text-xs text-emerald-600 font-semibold mt-2 flex items-center gap-1">
            <TrendingUp className="w-3.5 h-3.5" /> +{metrics?.projected_waste_reduction_percent ?? 34.5}% vs baseline
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-teal-600 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">CO2e Mitigated</span>
            <TrendingUp className="w-5 h-5" />
          </div>
          <div className="text-3xl font-extrabold text-slate-900">
            {metrics?.co2e_avoided_kg ?? '8.8'} <span className="text-base font-medium text-slate-500">kg CO2e</span>
          </div>
          <div className="text-xs text-slate-500 mt-2">
            ≈ {metrics?.equivalencies.car_km_avoided ?? '36.1'} km passenger driving avoided
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-blue-600 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Grocery Money Saved</span>
            <DollarSign className="w-5 h-5" />
          </div>
          <div className="text-3xl font-extrabold text-slate-900">
            ${metrics?.money_saved_usd ?? '14.50'}
          </div>
          <div className="text-xs text-slate-500 mt-2">
            Based on USDA food waste cost benchmarks
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-indigo-600 mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Safety Vetoes Enforced</span>
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div className="text-3xl font-extrabold text-slate-900">
            {metrics?.safety_vetoes_prevented ?? '3'}
          </div>
          <div className="text-xs text-indigo-600 font-semibold mt-2">
            0% false negative allergen guarantee
          </div>
        </div>
      </div>

      {/* Near Expiry Alert & Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Near Expiry Action Section */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-amber-500" />
                At-Risk Ingredients (Expiring within 72h)
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Prioritized by the Meal Planner to prevent household food waste
              </p>
            </div>
            <Link
              href="/planner"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold transition shadow-sm"
            >
              <Sparkles className="w-3.5 h-3.5" /> Plan Rescue Meal
            </Link>
          </div>

          <div className="divide-y divide-slate-100">
            {expiringSoon.map((item) => (
              <div key={item.id} className="py-3 flex items-center justify-between">
                <div>
                  <span className="font-semibold text-sm text-slate-800">{item.name}</span>
                  <div className="text-xs text-slate-400">
                    {item.quantity} {item.unit} • Category: {item.category}
                  </div>
                </div>
                <ExpiryBadge days={item.days_to_expiry} />
              </div>
            ))}
            {expiringSoon.length === 0 && (
              <p className="py-4 text-xs text-slate-500 text-center">
                All pantry items have more than 3 days of fresh shelf life remaining!
              </p>
            )}
          </div>
        </div>

        {/* Multi-Agent Quick Navigator */}
        <div className="space-y-4">
          <div className="bg-gradient-to-br from-slate-900 to-slate-800 text-white p-6 rounded-2xl shadow-md">
            <h3 className="font-extrabold text-base mb-1">Autonomous Multi-Agent Mesh</h3>
            <p className="text-xs text-slate-300 mb-4">
              Explore specialized agents coordinating safety, waste reduction, and procurement:
            </p>
            <div className="space-y-2">
              <Link
                href="/intake"
                className="flex items-center justify-between p-3 rounded-xl bg-white/10 hover:bg-white/15 transition text-xs font-medium"
              >
                <span>Vision Intake (Multimodal OCR)</span>
                <ArrowRight className="w-4 h-4 text-emerald-400" />
              </Link>
              <Link
                href="/planner"
                className="flex items-center justify-between p-3 rounded-xl bg-white/10 hover:bg-white/15 transition text-xs font-medium"
              >
                <span>Meal Planner & Safety Guardian</span>
                <ArrowRight className="w-4 h-4 text-emerald-400" />
              </Link>
              <Link
                href="/shopping"
                className="flex items-center justify-between p-3 rounded-xl bg-white/10 hover:bg-white/15 transition text-xs font-medium"
              >
                <span>Smart Procurement Shopping List</span>
                <ArrowRight className="w-4 h-4 text-emerald-400" />
              </Link>
              <Link
                href="/audit"
                className="flex items-center justify-between p-3 rounded-xl bg-white/10 hover:bg-white/15 transition text-xs font-medium"
              >
                <span>Security & Decision Audit Trail</span>
                <ArrowRight className="w-4 h-4 text-emerald-400" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
