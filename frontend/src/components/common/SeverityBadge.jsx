import React from 'react';
import { ShieldCheck, AlertCircle, AlertTriangle, Flame } from 'lucide-react';

export default function SeverityBadge({ severity = 'Mild', lesionPercentage = null }) {
  const norm = (severity || 'Mild').toLowerCase();

  let config = {
    label: 'Mild Severity',
    bg: 'bg-emerald-50 text-emerald-800 border-emerald-200',
    dot: 'bg-emerald-500',
    icon: AlertCircle,
    desc: 'Localized leaf spotting (< 10% lesion area)'
  };

  if (norm === 'healthy') {
    config = {
      label: 'Healthy Foliage',
      bg: 'bg-green-50 text-green-800 border-green-200',
      dot: 'bg-green-500',
      icon: ShieldCheck,
      desc: 'No active necrotic or chlorotic lesions detected'
    };
  } else if (norm === 'moderate') {
    config = {
      label: 'Moderate Severity',
      bg: 'bg-amber-50 text-amber-800 border-amber-200',
      dot: 'bg-amber-500',
      icon: AlertTriangle,
      desc: 'Expanding lesions (10% - 30% leaf surface affected)'
    };
  } else if (norm === 'severe') {
    config = {
      label: 'Severe Infestation',
      bg: 'bg-rose-50 text-rose-800 border-rose-200',
      dot: 'bg-rose-500',
      icon: Flame,
      desc: 'Systemic blighting (> 30% lesion coverage); immediate intervention'
    };
  }

  const Icon = config.icon;

  return (
    <div className="inline-flex flex-col">
      <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold border shadow-2xs ${config.bg}`}>
        <span className={`w-2 h-2 rounded-full ${config.dot}`} />
        <Icon className="w-4 h-4" />
        <span>{config.label}</span>
        {lesionPercentage !== null && (
          <span className="opacity-75 font-mono text-[11px] border-l border-current pl-1.5 ml-0.5">
            {lesionPercentage}% area
          </span>
        )}
      </div>
    </div>
  );
}
