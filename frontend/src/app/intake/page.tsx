'use client';

import React, { useState } from 'react';
import { Camera, Upload, CheckCircle2, AlertCircle, Sparkles, ArrowRight } from 'lucide-react';
import { ingestReceiptText, approveIntakeItems } from '../../lib/api';
import { ExpiryBadge } from '../../components/ExpiryBadge';
import { AgentTicker } from '../../components/AgentTicker';

export default function IntakePage() {
  const [rawText, setRawText] = useState('');
  const [loading, setLoading] = useState(false);
  const [extractedData, setExtractedData] = useState<any | null>(null);
  const [committed, setCommitted] = useState(false);

  const sampleReceipt = 
`SUPERMARKET GROCERY RECEIPT
2026-10-23
Fresh Baby Spinach 300g $2.99
Organic Firm Tofu 400g $3.49
Red Bell Pepper 2pk $2.50
Button Mushrooms 250g $2.70
Greek Yogurt 500g $4.20
Arachis Groundnut Oil 500ml $5.50
TOTAL: $21.38`;

  const handleProcess = async () => {
    setLoading(true);
    try {
      const data = await ingestReceiptText(rawText || sampleReceipt);
      setExtractedData(data);
      setCommitted(false);
    } catch (e) {
      alert('Error processing receipt');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async () => {
    if (!extractedData || !extractedData.extracted_items) return;
    try {
      await approveIntakeItems(extractedData.extracted_items);
      setCommitted(true);
    } catch (e) {
      alert('Error committing to inventory');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <Camera className="w-5 h-5 text-emerald-600" /> Multimodal Grocery Intake
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Vision Intake Agent (Gemini Flash) extracts items, quantities, and calculates shelf life from receipts.
          </p>
        </div>
        <AgentTicker activeAgent={loading ? 'vision_intake' : 'Idle'} latencyMs={extractedData?.latency_ms} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upload / Text Box */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
            Receipt Ingestion
          </h2>

          <div className="border-2 border-dashed border-slate-200 rounded-xl p-6 text-center hover:border-emerald-400 transition bg-slate-50">
            <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2" />
            <p className="text-xs font-semibold text-slate-700">Drag & Drop Supermarket Receipt Photo</p>
            <p className="text-[11px] text-slate-400 mt-1">PNG, JPG, WebP up to 10MB (EXIF stripped automatically)</p>
            <button
              onClick={() => setRawText(sampleReceipt)}
              className="mt-3 px-3 py-1 bg-white border border-slate-300 rounded-md text-xs font-semibold text-slate-700 hover:bg-slate-100"
            >
              Load Sample Supermarket Receipt
            </button>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">
              Or Paste Receipt Text / Grocery List:
            </label>
            <textarea
              rows={6}
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              placeholder="Paste line items from store app or typed receipt..."
              className="w-full border border-slate-300 rounded-xl p-3 text-xs font-mono focus:ring-2 focus:ring-emerald-500 focus:outline-none"
            />
          </div>

          <button
            onClick={handleProcess}
            disabled={loading}
            className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white rounded-xl text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition"
          >
            <Sparkles className="w-4 h-4" />
            {loading ? 'Processing via Gemini Flash...' : 'Extract & Estimate Shelf-Life'}
          </button>
        </div>

        {/* Review & Human Confirmation */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
              Human Review & Confirmation Gate
            </h2>
            {extractedData && (
              <span className="text-[11px] font-mono text-slate-500">
                PII Scrubbed: {extractedData.pii_redactions}
              </span>
            )}
          </div>

          {!extractedData && (
            <div className="h-64 flex flex-col items-center justify-center text-slate-400 text-xs text-center border border-dashed rounded-xl p-6">
              <Camera className="w-8 h-8 mb-2 opacity-50" />
              <span>Extracted receipt items will appear here for verification prior to writing to inventory.</span>
            </div>
          )}

          {extractedData && (
            <div className="space-y-3">
              <div className="max-h-72 overflow-y-auto divide-y divide-slate-100 border rounded-xl p-2 bg-slate-50">
                {extractedData.extracted_items?.map((item: any, i: number) => (
                  <div key={i} className="py-2.5 px-2 flex justify-between items-center text-xs">
                    <div>
                      <div className="font-bold text-slate-800">{item.name}</div>
                      <div className="text-[11px] text-slate-400">
                        {item.quantity} {item.unit} • Source: {item.expiry_source}
                      </div>
                    </div>
                    <ExpiryBadge days={item.days_to_expiry} />
                  </div>
                ))}
              </div>

              {!committed ? (
                <button
                  onClick={handleApprove}
                  className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  Confirm & Commit to Live Inventory
                </button>
              ) : (
                <div className="p-3 bg-emerald-50 border border-emerald-300 rounded-xl text-emerald-800 text-xs font-bold flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  Successfully committed items to live pantry!
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
