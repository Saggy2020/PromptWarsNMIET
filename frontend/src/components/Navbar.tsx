import React from 'react';
import Link from 'next/link';
import { Leaf, Camera, UtensilsCrossed, CalendarDays, ShoppingBag, BarChart3, Users, Shield } from 'lucide-react';

export const Navbar: React.FC = () => {
  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center space-x-8">
            <Link href="/" className="flex items-center gap-2 text-emerald-600 font-extrabold text-xl tracking-tight">
              <div className="w-9 h-9 rounded-xl bg-emerald-600 text-white flex items-center justify-center shadow-sm">
                <Leaf className="w-5 h-5" />
              </div>
              <span>Pantry<span className="text-slate-900">Pilot</span></span>
            </Link>

            <div className="hidden md:flex space-x-1">
              <Link href="/intake" className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-slate-700 hover:text-emerald-600 hover:bg-slate-50 rounded-lg">
                <Camera className="w-4 h-4" /> Intake
              </Link>
              <Link href="/inventory" className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-slate-700 hover:text-emerald-600 hover:bg-slate-50 rounded-lg">
                <UtensilsCrossed className="w-4 h-4" /> Live Pantry
              </Link>
              <Link href="/planner" className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-slate-700 hover:text-emerald-600 hover:bg-slate-50 rounded-lg">
                <CalendarDays className="w-4 h-4" /> Meal Planner
              </Link>
              <Link href="/shopping" className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-slate-700 hover:text-emerald-600 hover:bg-slate-50 rounded-lg">
                <ShoppingBag className="w-4 h-4" /> Shopping
              </Link>
              <Link href="/impact" className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-slate-700 hover:text-emerald-600 hover:bg-slate-50 rounded-lg">
                <BarChart3 className="w-4 h-4" /> Impact & CO2e
              </Link>
              <Link href="/profiles" className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-slate-700 hover:text-emerald-600 hover:bg-slate-50 rounded-lg">
                <Users className="w-4 h-4" /> Profiles
              </Link>
              <Link href="/audit" className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-slate-700 hover:text-emerald-600 hover:bg-slate-50 rounded-lg">
                <Shield className="w-4 h-4" /> Security & Audit
              </Link>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-xs bg-slate-100 text-slate-600 px-3 py-1 rounded-full font-mono font-medium border border-slate-200">
              v1.0.0
            </span>
          </div>
        </div>
      </div>
    </nav>
  );
};
