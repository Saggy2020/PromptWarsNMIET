'use client';

import React, { useEffect, useState } from 'react';
import { Shield, Download, Trash2, ShieldAlert, Cpu, Clock, DollarSign } from 'lucide-react';
import { fetchAuditLogs } from '../../lib/api';
import { AuditLogEntry } from '../../lib/types';

export default function AuditPage() {
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchAuditLogs();
        setLogs(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleExport = () => {
    window.open('http://localhost:8000/api/privacy/export?household_id=demo-household-sharma', '_blank');
  };

  const handleDelete = async () => {
    if (confirm('Are you sure you want to permanently delete all household data per Privacy by Design principles?')) {
      await fetch('http://localhost:8000/api/privacy/delete-all?household_id=demo-household-sharma', { method: 'DELETE' });
      alert('All household data permanently erased.');
      window.location.reload();
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <Shield className="w-5 h-5 text-emerald-600" /> Multi-Agent Audit Trail & Privacy Controls
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Immutable decision log with Correlation IDs, token telemetry, latency, and data sovereignty controls.
          </p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={handleExport}
            className="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition flex items-center gap-1.5 border"
          >
            <Download className="w-3.5 h-3.5" /> Export My Data (JSON)
          </button>
          <button
            onClick={handleDelete}
            className="px-3.5 py-1.5 bg-red-50 hover:bg-red-100 text-red-700 rounded-xl text-xs font-bold transition flex items-center gap-1.5 border border-red-200"
          >
            <Trash2 className="w-3.5 h-3.5" /> Delete All Data
          </button>
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-bold uppercase tracking-wider">
              <tr>
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4">Agent Name</th>
                <th className="py-3 px-4">Action</th>
                <th className="py-3 px-4">Safety Veto</th>
                <th className="py-3 px-4">Tokens / Cost</th>
                <th className="py-3 px-4">Latency</th>
                <th className="py-3 px-4">Summary</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-50/50 transition">
                  <td className="py-3 px-4 text-slate-500">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </td>
                  <td className="py-3 px-4 font-bold text-slate-800">
                    {log.agent_name}
                  </td>
                  <td className="py-3 px-4 text-slate-600">
                    {log.action}
                  </td>
                  <td className="py-3 px-4">
                    {log.safety_veto_applied ? (
                      <span className="bg-red-100 text-red-800 px-2 py-0.5 rounded font-bold uppercase text-[10px]">
                        VETOED
                      </span>
                    ) : (
                      <span className="bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-bold uppercase text-[10px]">
                        CLEARED
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-slate-600">
                    {log.tokens_used} tok (${log.cost_usd.toFixed(6)})
                  </td>
                  <td className="py-3 px-4 text-slate-600">
                    {log.latency_ms.toFixed(1)} ms
                  </td>
                  <td className="py-3 px-4 text-slate-700 max-w-xs truncate font-sans text-xs">
                    {log.output_summary}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
