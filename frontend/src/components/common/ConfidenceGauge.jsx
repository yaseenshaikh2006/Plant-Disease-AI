import React from 'react';
import { CheckCircle2, AlertTriangle, AlertCircle } from 'lucide-react';

export default function ConfidenceGauge({ confidence = 0.0, size = 120 }) {
  const percentage = Math.round(confidence * 100);
  const radius = (size - 16) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  let colorScheme = {
    stroke: '#10b981', // emerald-500
    track: '#d1fae5',  // emerald-100
    text: 'text-emerald-700',
    label: 'High Confidence',
    icon: CheckCircle2,
    badgeBg: 'bg-emerald-50 text-emerald-700 border-emerald-200'
  };

  if (percentage < 65) {
    colorScheme = {
      stroke: '#f59e0b', // amber-500
      track: '#fef3c7',  // amber-100
      text: 'text-amber-700',
      label: 'Moderate / Review',
      icon: AlertTriangle,
      badgeBg: 'bg-amber-50 text-amber-700 border-amber-200'
    };
  }
  if (percentage < 45) {
    colorScheme = {
      stroke: '#ef4444', // red-500
      track: '#fee2e2',  // red-100
      text: 'text-red-700',
      label: 'Low Confidence',
      icon: AlertCircle,
      badgeBg: 'bg-red-50 text-red-700 border-red-200'
    };
  }

  const Icon = colorScheme.icon;

  return (
    <div className="flex flex-col items-center justify-center p-3">
      <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
        <svg className="transform -rotate-90" width={size} height={size}>
          {/* Background Track */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={colorScheme.track}
            strokeWidth="8"
            fill="transparent"
          />
          {/* Animated Progress Value */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={colorScheme.stroke}
            strokeWidth="8"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center Percentage Display */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-2xl font-black tracking-tight ${colorScheme.text}`}>
            {percentage}%
          </span>
          <span className="text-[10px] uppercase font-bold tracking-wider text-slate-600">
            Certainty
          </span>
        </div>
      </div>

      <div className={`mt-2.5 inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${colorScheme.badgeBg}`}>
        <Icon className="w-3.5 h-3.5" />
        <span>{colorScheme.label}</span>
      </div>
    </div>
  );
}
