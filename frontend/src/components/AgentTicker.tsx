import React from 'react';
import { Bot, Cpu, ShieldCheck, ShoppingCart, Sparkles } from 'lucide-react';

interface AgentTickerProps {
  activeAgent?: string;
  latencyMs?: number;
}

export const AgentTicker: React.FC<AgentTickerProps> = ({ activeAgent = 'Idle', latencyMs }) => {
  const getBadge = () => {
    switch (activeAgent.toLowerCase()) {
      case 'vision_intake':
      case 'vision':
        return { name: 'Vision Intake Agent (Gemini Flash)', color: 'bg-purple-100 text-purple-800 border-purple-300', icon: Sparkles };
      case 'meal_planner':
      case 'planner':
        return { name: 'Constrained Meal Planner (Gemini Pro)', color: 'bg-blue-100 text-blue-800 border-blue-300', icon: Cpu };
      case 'safety_guardian':
      case 'safety':
        return { name: 'Deterministic Safety Guardian (Rule Engine)', color: 'bg-red-100 text-red-800 border-red-300', icon: ShieldCheck };
      case 'procurement':
        return { name: 'Procurement & Substitution Agent', color: 'bg-emerald-100 text-emerald-800 border-emerald-300', icon: ShoppingCart };
      default:
        return { name: 'Multi-Agent Mesh Ready', color: 'bg-slate-100 text-slate-700 border-slate-300', icon: Bot };
    }
  };

  const badge = getBadge();
  const IconComponent = badge.icon;

  return (
    <div className="flex items-center gap-3 px-3 py-1.5 rounded-full border bg-white/80 backdrop-blur-sm shadow-sm text-xs">
      <span className="flex h-2 w-2 relative">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
        <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
      </span>
      <span className="text-slate-500 font-medium">Orchestration State:</span>
      <div className={`flex items-center gap-1.5 px-2.5 py-0.5 rounded-md font-semibold border ${badge.color}`}>
        <IconComponent className="w-3.5 h-3.5" />
        {badge.name}
      </div>
      {latencyMs !== undefined && latencyMs > 0 && (
        <span className="text-slate-400 font-mono text-[11px]">
          {latencyMs}ms
        </span>
      )}
    </div>
  );
};
