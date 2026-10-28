'use client';

import React, { useEffect, useState } from 'react';
import { Users, Shield, HeartPulse, AlertCircle, Plus } from 'lucide-react';
import { fetchHousehold } from '../../lib/api';
import { Household, HouseholdMember } from '../../lib/types';

export default function ProfilesPage() {
  const [household, setHousehold] = useState<Household | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchHousehold();
        setHousehold(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-600" /> Household Profiles & Dietary Constraints
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Up to 6 members with isolated allergen profiles, medical constraints, and sodium targets.
          </p>
        </div>

        <span className="text-xs font-mono bg-slate-100 text-slate-600 px-3 py-1.5 rounded-xl border border-slate-200">
          Role-Based Access: Owner
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {household?.members.map((member) => (
          <div key={member.id} className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-extrabold text-base text-slate-900">{member.name}</h3>
                <span className="text-[11px] uppercase tracking-wider font-bold text-slate-400">
                  Role: {member.role}
                </span>
              </div>
              <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-xs">
                {member.name.charAt(0)}
              </div>
            </div>

            {/* Allergies */}
            <div>
              <span className="text-xs font-bold text-slate-700 block mb-1">Declared Allergies:</span>
              <div className="flex flex-wrap gap-1.5">
                {member.allergies.map((a, i) => (
                  <span
                    key={i}
                    className="text-[11px] bg-red-100 text-red-800 border border-red-300 px-2 py-0.5 rounded-md font-bold"
                  >
                    {a.allergen.replace('_', ' ')} ({a.severity.replace('_', ' ')})
                  </span>
                ))}
                {member.allergies.length === 0 && (
                  <span className="text-xs text-slate-400">No known allergies</span>
                )}
              </div>
            </div>

            {/* Medical Conditions */}
            <div>
              <span className="text-xs font-bold text-slate-700 block mb-1 flex items-center gap-1">
                <HeartPulse className="w-3.5 h-3.5 text-blue-500" /> Medical Conditions:
              </span>
              <div className="flex flex-wrap gap-1.5">
                {member.medical_conditions.map((mc, i) => (
                  <span
                    key={i}
                    className="text-[11px] bg-blue-100 text-blue-800 border border-blue-300 px-2 py-0.5 rounded-md font-semibold"
                  >
                    {mc.replace('_', ' ')}
                  </span>
                ))}
                {member.medical_conditions.length === 0 && (
                  <span className="text-xs text-slate-400">None</span>
                )}
              </div>
            </div>

            {/* Targets */}
            <div className="border-t border-slate-100 pt-3 text-xs text-slate-600 space-y-1">
              <div>
                <strong>Preferences:</strong> {member.dietary_preferences.join(', ') || 'Omnivore'}
              </div>
              {member.max_daily_sodium_mg && (
                <div>
                  <strong>Max Sodium:</strong> &lt; {member.max_daily_sodium_mg} mg/day
                </div>
              )}
              {member.daily_calorie_target && (
                <div>
                  <strong>Calorie Target:</strong> {member.daily_calorie_target} kcal
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
