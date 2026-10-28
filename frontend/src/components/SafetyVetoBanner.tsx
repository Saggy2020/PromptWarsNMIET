import React from 'react';
import { AlertTriangle, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { MemberSafetyVerdict } from '../lib/types';

interface SafetyVetoBannerProps {
  verdicts: MemberSafetyVerdict[];
  recipeTitle?: string;
}

export const SafetyVetoBanner: React.FC<SafetyVetoBannerProps> = ({ verdicts, recipeTitle }) => {
  const hasVeto = verdicts.some((v) => v.is_vetoed);
  const hasWarning = verdicts.some((v) => v.status === 'warning' && !v.is_vetoed);

  if (hasVeto) {
    return (
      <div className="bg-red-50 border-2 border-red-500 rounded-xl p-4 my-3 text-red-900 shadow-sm">
        <div className="flex items-start">
          <ShieldAlert className="w-6 h-6 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-bold text-base flex items-center gap-2">
              🛑 DETERMINISTIC SAFETY VETO
              <span className="text-xs bg-red-200 text-red-900 px-2 py-0.5 rounded font-mono uppercase">
                Zero LLM Authority
              </span>
            </h4>
            <p className="text-sm text-red-800 mt-1">
              This recipe is blocked because it violates severe allergen or medical constraints:
            </p>
            <ul className="list-disc list-inside mt-2 text-xs font-medium space-y-1">
              {verdicts
                .filter((v) => v.is_vetoed)
                .map((v) =>
                  v.reasons.map((r, i) => (
                    <li key={`${v.member_id}-${i}`} className="text-red-950 font-semibold">
                      {r}
                    </li>
                  ))
                )}
            </ul>
          </div>
        </div>
      </div>
    );
  }

  if (hasWarning) {
    return (
      <div className="bg-amber-50 border border-amber-300 rounded-xl p-3 my-2 text-amber-900 text-sm flex items-start">
        <AlertTriangle className="w-5 h-5 text-amber-600 mr-2 flex-shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Dietary Warning:</span>
          <ul className="list-disc list-inside mt-1 text-xs space-y-0.5">
            {verdicts
              .filter((v) => v.status === 'warning')
              .map((v) =>
                v.reasons.map((r, i) => (
                  <li key={`${v.member_id}-${i}`}>{r}</li>
                ))
              )}
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-emerald-50 border border-emerald-300 rounded-lg p-2.5 my-2 text-emerald-900 text-xs flex items-center">
      <CheckCircle2 className="w-4 h-4 text-emerald-600 mr-2 flex-shrink-0" />
      <span>
        <strong>100% Safe:</strong> Verified compliant with all household allergies, celiac restrictions, and sodium limits.
      </span>
    </div>
  );
};
