'use client';

import React, { useEffect, useState } from 'react';
import { CalendarDays, Sparkles, ShieldCheck, ShieldAlert, AlertTriangle, ChevronDown, ChevronUp, Info, Utensils } from 'lucide-react';
import { generateMealPlan, checkSafetyVeto } from '../../lib/api';
import { Recipe } from '../../lib/types';
import { SafetyVetoBanner } from '../../components/SafetyVetoBanner';
import { AgentTicker } from '../../components/AgentTicker';

export default function PlannerPage() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(false);
  const [vetoedCount, setVetoedCount] = useState(0);
  const [vetoDetails, setVetoDetails] = useState<string[]>([]);
  const [activeRecipeId, setActiveRecipeId] = useState<string | null>(null);

  // Custom interactive veto tester state
  const [testTitle, setTestTitle] = useState('Thai Peanut Tofu Satay');
  const [testIngredients, setTestIngredients] = useState('firm tofu, arachis oil, soy sauce, garlic');
  const [testResult, setTestResult] = useState<any | null>(null);
  const [testingVeto, setTestingVeto] = useState(false);

  const handleGeneratePlan = async () => {
    setLoading(true);
    try {
      const data = await generateMealPlan();
      setRecipes(data.recipes || []);
      setVetoedCount(data.vetoed_candidates_count || 0);
      setVetoDetails(data.veto_details || []);
      if (data.recipes && data.recipes.length > 0) {
        setActiveRecipeId(data.recipes[0].id);
      }
    } catch (e) {
      alert('Error generating meal plan');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleGeneratePlan();
  }, []);

  const handleRunCustomVeto = async () => {
    setTestingVeto(true);
    try {
      const ingList = testIngredients.split(',').map((s) => s.trim()).filter(Boolean);
      const res = await checkSafetyVeto(testTitle, ingList);
      setTestResult(res);
    } catch (e) {
      alert('Error running safety check');
    } finally {
      setTestingVeto(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <CalendarDays className="w-5 h-5 text-emerald-600" /> Constrained Meal Planner & Safety Guardian
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Prioritizes near-expiry ingredients while enforcing 100% deterministic allergen & medical safety vetoes.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <AgentTicker activeAgent={loading ? 'safety_guardian' : 'Idle'} />
          <button
            onClick={handleGeneratePlan}
            disabled={loading}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white rounded-xl text-xs font-bold flex items-center gap-2 shadow-sm transition"
          >
            <Sparkles className="w-4 h-4" />
            {loading ? 'Solving Constraints...' : 'Generate New Plan'}
          </button>
        </div>
      </div>

      {/* Safety Veto Interception Summary */}
      {vetoedCount > 0 && (
        <div className="bg-red-50 border-2 border-red-500 rounded-2xl p-5 shadow-sm">
          <div className="flex items-start gap-3">
            <ShieldAlert className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold text-sm text-red-900 flex items-center gap-2">
                🛑 DETERMINISTIC SAFETY INTERCEPTION APPLIED ({vetoedCount} candidate recipe vetoed)
                <span className="text-[10px] bg-red-200 text-red-900 px-2 py-0.5 rounded font-mono uppercase font-bold">
                  Zero LLM Override
                </span>
              </h3>
              <p className="text-xs text-red-800 mt-1">
                The generative planner formulated candidate recipes that contained disguised allergen synonyms. The deterministic safety engine exercised absolute veto power and permanently excluded them from the approved plan:
              </p>
              <ul className="list-disc list-inside mt-2 text-xs text-red-950 font-semibold space-y-1">
                {vetoDetails.map((detail, idx) => (
                  <li key={idx}>{detail}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Approved Meal Plan Recipes */}
      <div className="space-y-4">
        <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
          <Utensils className="w-4 h-4 text-emerald-600" />
          Verified Safe, Waste-Minimizing Recipes
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {recipes.map((recipe) => (
            <div key={recipe.id} className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4 flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start gap-2">
                  <div>
                    <h3 className="font-extrabold text-base text-slate-900">{recipe.title}</h3>
                    <p className="text-xs text-slate-500 mt-1">{recipe.description}</p>
                  </div>
                  <span className="bg-emerald-100 text-emerald-800 text-xs px-2.5 py-1 rounded-full font-bold flex-shrink-0">
                    {recipe.waste_reduction_score}% Waste Rescued
                  </span>
                </div>

                {/* Rescued near-expiry items */}
                <div className="mt-3 flex flex-wrap gap-1.5 items-center">
                  <span className="text-[11px] font-bold text-slate-500 mr-1">Rescues:</span>
                  {recipe.expiring_items_used.map((it, i) => (
                    <span key={i} className="text-[11px] bg-amber-50 text-amber-800 border border-amber-300 px-2 py-0.5 rounded-md font-semibold">
                      {it}
                    </span>
                  ))}
                </div>

                {/* Deterministic Safety Badges */}
                <SafetyVetoBanner verdicts={recipe.member_verdicts} recipeTitle={recipe.title} />

                {/* Explainability Rationale */}
                <div className="bg-slate-50 rounded-xl p-3 border border-slate-200 text-xs">
                  <div className="font-bold text-slate-700 flex items-center gap-1.5 mb-1">
                    <Info className="w-3.5 h-3.5 text-blue-500" />
                    Why this recipe? (Agent Explainability)
                  </div>
                  <p className="text-slate-600 leading-relaxed">{recipe.explainability_rationale}</p>
                </div>
              </div>

              {/* Ingredients & Prep */}
              <div className="border-t border-slate-100 pt-3 text-xs text-slate-600 flex justify-between">
                <span>⏱️ {recipe.prep_time_minutes} mins</span>
                <span>🍽️ {recipe.servings} servings</span>
                <span>🔥 {recipe.estimated_calories_per_serving} kcal</span>
                <span>🧂 {recipe.sodium_mg_per_serving}mg sodium</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Interactive Safety Veto Sandbox for Judges */}
      <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-lg space-y-4">
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-red-400" />
          <h2 className="text-base font-bold">Judges' Deterministic Safety Veto Sandbox</h2>
        </div>
        <p className="text-xs text-slate-300 leading-relaxed">
          Test any ingredient or disguised allergen synonym (e.g. <em>arachis oil</em> for peanuts, <em>spelt/seitan</em> for celiac disease) to observe the deterministic rule engine vetoing the proposal in real-time.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Recipe Name:</label>
            <input
              type="text"
              value={testTitle}
              onChange={(e) => setTestTitle(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Comma-Separated Ingredients:</label>
            <input
              type="text"
              value={testIngredients}
              onChange={(e) => setTestIngredients(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
            />
          </div>
        </div>

        <button
          onClick={handleRunCustomVeto}
          disabled={testingVeto}
          className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-bold transition flex items-center gap-2"
        >
          {testingVeto ? 'Evaluating...' : 'Run Deterministic Veto Check'}
        </button>

        {testResult && (
          <div className="mt-4 p-4 rounded-xl bg-slate-800 border border-slate-700 text-xs space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold">Verdict:</span>
              <span className={`px-2 py-0.5 rounded text-[11px] font-bold uppercase ${testResult.is_vetoed ? 'bg-red-900 text-red-200' : 'bg-emerald-900 text-emerald-200'}`}>
                {testResult.is_vetoed ? '🛑 VETOED (UNSAFE)' : '✅ 100% SAFE'}
              </span>
            </div>
            <div className="space-y-1">
              {testResult.member_verdicts?.map((v: any, i: number) => (
                <div key={i} className="text-slate-300">
                  <strong>{v.member_name}:</strong> {v.is_vetoed ? <span className="text-red-400 font-semibold">{v.reasons.join('; ')}</span> : <span className="text-emerald-400">Safe</span>}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
