'use client';

import React, { useEffect, useState } from 'react';
import { UtensilsCrossed, CheckCircle2, Trash2, AlertTriangle, Filter } from 'lucide-react';
import { fetchInventory, updateItemStatus } from '../../lib/api';
import { InventoryItem } from '../../lib/types';
import { ExpiryBadge } from '../../components/ExpiryBadge';

export default function InventoryPage() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'urgent' | 'pantry'>('all');
  const [notification, setNotification] = useState('');

  const loadData = async () => {
    try {
      const data = await fetchInventory();
      setItems(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleStatusChange = async (itemId: string, newStatus: 'consumed' | 'wasted') => {
    try {
      const res = await updateItemStatus(itemId, newStatus);
      if (newStatus === 'consumed') {
        setNotification('Item marked as consumed! Food waste avoided logged to Sustainability.');
      } else {
        setNotification('Item marked as wasted. Re-Planning Agent notified.');
      }
      setTimeout(() => setNotification(''), 3000);
      loadData();
    } catch (e) {
      alert('Error updating item');
    }
  };

  const filteredItems = items.filter((item) => {
    if (filter === 'urgent') return item.days_to_expiry <= 3 && item.status === 'in_stock';
    if (filter === 'pantry') return item.category === 'pantry';
    return item.status === 'in_stock';
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <UtensilsCrossed className="w-5 h-5 text-emerald-600" /> Live Household Inventory
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Tracking active shelf life and expiration countdowns. Consuming items updates waste metrics.
          </p>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl text-xs font-semibold">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1.5 rounded-lg transition ${filter === 'all' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600'}`}
          >
            All Items ({items.filter((i) => i.status === 'in_stock').length})
          </button>
          <button
            onClick={() => setFilter('urgent')}
            className={`px-3 py-1.5 rounded-lg transition ${filter === 'urgent' ? 'bg-white text-red-600 shadow-sm' : 'text-slate-600'}`}
          >
            Expiring &le; 3d ({items.filter((i) => i.days_to_expiry <= 3 && i.status === 'in_stock').length})
          </button>
          <button
            onClick={() => setFilter('pantry')}
            className={`px-3 py-1.5 rounded-lg transition ${filter === 'pantry' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600'}`}
          >
            Pantry Staples
          </button>
        </div>
      </div>

      {notification && (
        <div className="p-3 bg-emerald-50 border border-emerald-300 rounded-xl text-emerald-800 text-xs font-semibold flex items-center gap-2 animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          {notification}
        </div>
      )}

      {/* Inventory Grid */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-bold uppercase tracking-wider">
              <tr>
                <th className="py-3 px-4">Item Name</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Quantity</th>
                <th className="py-3 px-4">Expiry Countdown</th>
                <th className="py-3 px-4">Est. Cost</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {filteredItems.map((item) => (
                <tr key={item.id} className="hover:bg-slate-50/50 transition">
                  <td className="py-3.5 px-4 font-semibold text-slate-900">
                    {item.name}
                  </td>
                  <td className="py-3.5 px-4 capitalize text-slate-500">
                    {item.category}
                  </td>
                  <td className="py-3.5 px-4 text-slate-700">
                    {item.quantity} {item.unit}
                  </td>
                  <td className="py-3.5 px-4">
                    <ExpiryBadge days={item.days_to_expiry} />
                  </td>
                  <td className="py-3.5 px-4 text-slate-600">
                    ${item.estimated_cost.toFixed(2)}
                  </td>
                  <td className="py-3.5 px-4 text-right space-x-2">
                    <button
                      onClick={() => handleStatusChange(item.id, 'consumed')}
                      title="Mark as Consumed"
                      className="px-2.5 py-1 bg-emerald-100 hover:bg-emerald-200 text-emerald-800 rounded font-semibold text-[11px]"
                    >
                      Used
                    </button>
                    <button
                      onClick={() => handleStatusChange(item.id, 'wasted')}
                      title="Mark as Spoiled"
                      className="px-2.5 py-1 bg-slate-100 hover:bg-red-100 hover:text-red-700 text-slate-600 rounded font-semibold text-[11px]"
                    >
                      Spoiled
                    </button>
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
