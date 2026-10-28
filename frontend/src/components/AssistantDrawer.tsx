import React, { useState } from 'react';
import { MessageSquare, X, Send, Bot, User, AlertCircle, CheckCircle, ShieldAlert } from 'lucide-react';
import { sendChatMessage } from '../lib/api';

export const AssistantDrawer: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Array<{ sender: 'user' | 'bot'; text: string; action?: any; isDisclaimer?: boolean }>>([
    {
      sender: 'bot',
      text: "👋 Hi! I'm your PantryPilot household assistant. Ask me to recommend meals using expiring ingredients, check allergen safety, or ask about your food waste reduction!"
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const userText = input;
    setInput('');
    setMessages((prev) => [...prev, { sender: 'user', text: userText }]);
    setLoading(true);

    try {
      const res = await sendChatMessage(userText);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: res.response,
          action: res.action_proposal,
          isDisclaimer: res.is_medical_disclaimer
        }
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: 'Error communicating with assistant. Please try again.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-50 bg-emerald-600 hover:bg-emerald-700 text-white rounded-full p-4 shadow-xl flex items-center gap-2 font-semibold transition"
        aria-label="Open Assistant"
      >
        <MessageSquare className="w-5 h-5" />
        <span className="hidden sm:inline text-sm">Ask Assistant</span>
      </button>

      {isOpen && (
        <div className="fixed inset-y-0 right-0 z-50 w-full sm:w-96 bg-white shadow-2xl flex flex-col border-l border-slate-200 animate-in slide-in-from-right duration-200">
          <div className="p-4 border-b border-slate-200 flex justify-between items-center bg-slate-50">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center">
                <Bot className="w-4 h-4" />
              </div>
              <div>
                <h3 className="font-bold text-sm text-slate-800">PantryPilot Assistant</h3>
                <span className="text-[11px] text-emerald-600 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span> Multi-Agent Guarded
                </span>
              </div>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-slate-600">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((m, i) => (
              <div key={i} className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}>
                <div
                  className={`max-w-[85%] rounded-2xl px-3.5 py-2.5 text-xs leading-relaxed shadow-sm ${
                    m.sender === 'user'
                      ? 'bg-emerald-600 text-white rounded-br-none'
                      : m.isDisclaimer
                      ? 'bg-amber-50 text-amber-900 border border-amber-200 rounded-bl-none'
                      : 'bg-slate-100 text-slate-800 rounded-bl-none'
                  }`}
                >
                  {m.text}
                </div>

                {m.action && (
                  <div className="mt-2 p-3 bg-slate-50 border border-slate-300 rounded-xl text-xs max-w-[90%] shadow-sm">
                    <div className="font-bold text-slate-900 flex items-center gap-1.5 mb-1">
                      <AlertCircle className="w-3.5 h-3.5 text-emerald-600" />
                      {m.action.title}
                    </div>
                    <p className="text-slate-600 mb-2">{m.action.details}</p>
                    <div className="flex gap-2">
                      <button
                        onClick={() => alert('Action confirmed by user.')}
                        className="px-2.5 py-1 bg-emerald-600 text-white rounded font-medium text-[11px]"
                      >
                        Approve
                      </button>
                      <button
                        onClick={() => alert('Action declined.')}
                        className="px-2.5 py-1 bg-slate-200 text-slate-700 rounded font-medium text-[11px]"
                      >
                        Dismiss
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <Bot className="w-3.5 h-3.5 animate-spin" /> Thinking...
              </div>
            )}
          </div>

          <div className="p-3 border-t border-slate-200 bg-white flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about recipes, expiry, or safety..."
              className="flex-1 border border-slate-300 rounded-xl px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
            <button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              className="bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white rounded-xl px-3 py-2 text-xs font-semibold"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </>
  );
};
