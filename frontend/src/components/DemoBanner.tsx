import React, { useState } from 'react';
import { Sparkles, RefreshCw, CheckCircle2 } from 'lucide-react';
import { resetDemoHousehold } from '../lib/api';

export const DemoBanner: React.FC = () => {
  const [resetting, setResetting] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');

  const handleReset = async () => {
    setResetting(true);
    try {
      await resetDemoHousehold();
      setStatusMsg('Household re-seeded with near-expiry items & profiles!');
      setTimeout(() => {
        setStatusMsg('');
        window.location.reload();
      }, 1200);
    } catch (e) {
      setStatusMsg('Error resetting demo');
    } finally {
      setResetting(false);
    }
  };

  return (
    <div className="bg-gradient-to-r from-emerald-600 via-teal-600 to-indigo-700 text-white px-4 py-2.5 text-xs font-medium shadow-md">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <span className="bg-white/20 text-white uppercase text-[10px] tracking-wider px-2 py-0.5 rounded-full font-bold border border-white/30">
            Hackathon Demo Mode
          </span>
          <span>
            Evaluating <strong>The Sharma Household</strong> (Aarav: Peanut Veto & Hypertension; Maya: Celiac; Rohan: Vegetarian). Running offline with zero cloud credentials required.
          </span>
        </div>
        <div className="flex items-center gap-2">
          {statusMsg && (
            <span className="flex items-center gap-1 text-emerald-200">
              <CheckCircle2 className="w-3.5 h-3.5" /> {statusMsg}
            </span>
          )}
          <button
            onClick={handleReset}
            disabled={resetting}
            className="flex items-center gap-1.5 px-3 py-1 bg-white/20 hover:bg-white/30 rounded-md transition font-semibold text-white border border-white/30"
          >
            <RefreshCw className={`w-3 h-3 ${resetting ? 'animate-spin' : ''}`} />
            Reset Seed Data
          </button>
        </div>
      </div>
    </div>
  );
};
