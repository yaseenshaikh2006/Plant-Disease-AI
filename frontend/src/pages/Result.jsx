import React, { useState } from 'react';
import {
  ArrowLeft,
  Printer,
  CheckCircle,
  AlertTriangle,
  ShieldAlert,
  Droplets,
  Sprout,
  ShieldCheck,
  Activity,
  Layers,
  Info,
} from 'lucide-react';

import ConfidenceGauge from '../components/common/ConfidenceGauge';
import SeverityBadge from '../components/common/SeverityBadge';

export default function Result({ result, previewImage, onReset }) {
  const [activeTab, setActiveTab] = useState('treatment');

  if (!result) {
    return (
      <div className="max-w-xl mx-auto my-16 text-center space-y-4">
        <p className="text-slate-600">No diagnosis result available.</p>

        <button
          onClick={onReset}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm font-semibold"
        >
          Return to Detection
        </button>
      </div>
    );
  }

  const {
    crop,
    disease,
    confidence,
    severity,
    description,
    treatment = [],
    fertilizer = [],
    irrigation = [],
    prevention = [],
    symptoms = [],
    causes = [],
    recovery_tips = [],
    pathogen = '',
    severity_details,
    top_predictions = [],
  } = result;

  const isHealthy = disease?.toLowerCase().includes('healthy');

  const safeArray = (value) => {
    if (Array.isArray(value)) return value;
    if (value) return [value];
    return [];
  };

  const treatmentItems = safeArray(treatment);
  const fertilizerItems = safeArray(fertilizer);
  const irrigationItems = safeArray(irrigation);
  const preventionItems = safeArray(prevention);
  const symptomItems = safeArray(symptoms);
  const causeItems = safeArray(causes);
  const recoveryItems = safeArray(recovery_tips);

  const tabs = [
    {
      id: 'treatment',
      label: 'Treatment Protocol',
      icon: ShieldAlert,
      count: treatmentItems.length,
    },
    {
      id: 'symptoms',
      label: 'Symptoms & Etiology',
      icon: Activity,
      count: symptomItems.length,
    },
    {
      id: 'fertilizer',
      label: 'Fertilizer & Nutrition',
      icon: Sprout,
      count: fertilizerItems.length,
    },
    {
      id: 'irrigation',
      label: 'Irrigation Advice',
      icon: Droplets,
      count: irrigationItems.length,
    },
    {
      id: 'prevention',
      label: 'Prevention & Sanitation',
      icon: ShieldCheck,
      count: preventionItems.length,
    },
  ];

  const handlePrint = () => {
    window.print();
  };

  const confidencePercent = Math.round((confidence || 0) * 100);

  const hasRecommendations =
    treatmentItems.length > 0 ||
    fertilizerItems.length > 0 ||
    irrigationItems.length > 0 ||
    preventionItems.length > 0;

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8 space-y-8 print:p-0">

      {/* Top Action Bar */}
      <div className="flex items-center justify-between print:hidden">
        <button
          onClick={onReset}
          className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 hover:text-emerald-700 hover:border-emerald-300 text-xs font-semibold shadow-2xs transition-all"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Upload Another Image</span>
        </button>

        <button
          onClick={handlePrint}
          className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 text-xs font-semibold shadow-2xs transition-all"
        >
          <Printer className="w-4 h-4 text-slate-500" />
          <span>Print Report</span>
        </button>
      </div>

      {/* Main Diagnostic Header */}
      <div className="bg-white rounded-3xl border border-slate-200/90 shadow-sm overflow-hidden p-6 sm:p-8">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">

          {/* Leaf Thumbnail */}
          {previewImage && (
            <div className="md:col-span-3">
              <div className="relative rounded-2xl overflow-hidden border border-slate-200 aspect-square bg-slate-900 shadow-inner">
                <img
                  src={previewImage}
                  alt="Analyzed leaf"
                  className="w-full h-full object-cover"
                />

                <span className="absolute bottom-2 left-2 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md bg-black/70 text-white backdrop-blur">
                  Analyzed Specimen
                </span>
              </div>
            </div>
          )}

          {/* Diagnosis */}
          <div
            className={`${
              previewImage ? 'md:col-span-6' : 'md:col-span-8'
            } space-y-3`}
          >
            <div className="flex flex-wrap items-center gap-2">

              <span className="text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-emerald-100 text-emerald-900 border border-emerald-200">
                {crop} Crop
              </span>

              <SeverityBadge
                severity={severity}
                lesionPercentage={severity_details?.lesion_percentage}
              />
            </div>

            <div>
              <h1 className="text-2xl sm:text-3xl font-black text-slate-950 tracking-tight">
                {disease}
              </h1>

              {pathogen && (
                <p className="text-xs font-mono text-slate-500 mt-1">
                  Etiological Pathogen: {pathogen}
                </p>
              )}
            </div>

            <p className="text-sm text-slate-600 leading-relaxed max-w-xl">
              {description}
            </p>
          </div>

          {/* Confidence */}
          <div
            className={`${
              previewImage ? 'md:col-span-3' : 'md:col-span-4'
            } flex justify-center border-t md:border-t-0 md:border-l border-slate-100 pt-4 md:pt-0`}
          >
            <div className="flex flex-col items-center gap-2">
              <ConfidenceGauge
                confidence={confidence}
                size={130}
              />

              <span className="text-[10px] uppercase tracking-wider font-bold text-slate-500">
                Model Confidence
              </span>

              <span className="text-xs font-semibold text-slate-700">
                {confidencePercent}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Important Model Interpretation Notice */}
      {!isHealthy && confidencePercent < 70 && (
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />

          <div>
            <h3 className="text-sm font-bold text-amber-900">
              Lower-confidence prediction
            </h3>

            <p className="text-xs text-amber-800 mt-1 leading-relaxed">
              The model assigned {confidencePercent}% probability to this
              prediction. Review the top candidate predictions below and
              consider expert verification before taking major field-level
              action.
            </p>
          </div>
        </div>
      )}

      {/* Healthy Notice */}
      {isHealthy && (
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 flex items-start gap-3">
          <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />

          <div>
            <h3 className="text-sm font-bold text-emerald-900">
              Healthy leaf indication
            </h3>

            <p className="text-xs text-emerald-800 mt-1">
              The model classified the submitted specimen as healthy.
              Continue regular crop monitoring and preventive care.
            </p>
          </div>
        </div>
      )}

      {/* Recommendation Area */}
      <div className="space-y-4">

        {/* Missing Knowledge Base Notice */}
        {!hasRecommendations && (
          <div className="rounded-2xl border border-blue-200 bg-blue-50 p-5 flex items-start gap-3">
            <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />

            <div>
              <h3 className="text-sm font-bold text-blue-900">
                Recommendation knowledge base unavailable
              </h3>

              <p className="text-xs text-blue-800 mt-1 leading-relaxed">
                The disease classifier detected <strong>{disease}</strong>,
                but a detailed agronomic recommendation for this disease is
                not currently available in the local knowledge base.
                No treatment or dosage has been automatically invented.
              </p>
            </div>
          </div>
        )}

        {/* Navigation Tabs */}
        <div className="flex overflow-x-auto gap-2 border-b border-slate-200 pb-2 scrollbar-none">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;

            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                  isActive
                    ? 'bg-emerald-600 text-white shadow-xs'
                    : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200/80'
                }`}
              >
                <Icon
                  className={`w-4 h-4 ${
                    isActive ? 'text-white' : 'text-slate-400'
                  }`}
                />

                <span>{tab.label}</span>

                <span
                  className={`px-1.5 py-0.2 rounded-full text-[10px] ${
                    isActive
                      ? 'bg-emerald-700 text-emerald-100'
                      : 'bg-slate-100 text-slate-600'
                  }`}
                >
                  {tab.count}
                </span>
              </button>
            );
          })}
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-6 sm:p-8">

          {/* Treatment */}
          {activeTab === 'treatment' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  Targeted Curative & Management Protocol
                </h3>

                <p className="text-xs text-slate-500 mt-1">
                  Recommendations provided by the local agronomic knowledge
                  base.
                </p>
              </div>

              {treatmentItems.length > 0 ? (
                <div className="grid grid-cols-1 gap-3">
                  {treatmentItems.map((item, idx) => (
                    <div
                      key={idx}
                      className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 flex items-start gap-3 text-sm text-slate-700 leading-relaxed"
                    >
                      <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                      <span>{item}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState message="Detailed treatment recommendations are not available for this prediction." />
              )}
            </div>
          )}

          {/* Symptoms */}
          {activeTab === 'symptoms' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-base font-bold text-slate-900 mb-3">
                  Visual Symptoms & Pathology
                </h3>

                {symptomItems.length > 0 ? (
                  <div className="space-y-2.5">
                    {symptomItems.map((item, idx) => (
                      <div
                        key={idx}
                        className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/70 text-sm text-slate-700 flex items-start gap-3"
                      >
                        <span className="w-2 h-2 rounded-full bg-amber-500 shrink-0 mt-2" />
                        <span>{item}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <EmptyState message="Detailed symptom information is not available in the current knowledge base." />
                )}
              </div>

              {causeItems.length > 0 && (
                <div className="pt-4 border-t border-slate-100">
                  <h4 className="text-sm font-bold text-slate-800 mb-2">
                    Precipitating Environmental Causes
                  </h4>

                  <ul className="list-disc list-inside space-y-1.5 text-xs sm:text-sm text-slate-600">
                    {causeItems.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Fertilizer */}
          {activeTab === 'fertilizer' && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-slate-900">
                Nutritional Regimen & Fertilizer Management
              </h3>

              {fertilizerItems.length > 0 ? (
                <div className="grid grid-cols-1 gap-3">
                  {fertilizerItems.map((item, idx) => (
                    <div
                      key={idx}
                      className="p-4 rounded-xl bg-emerald-50/50 border border-emerald-200/70 flex items-start gap-3 text-sm text-slate-700"
                    >
                      <Sprout className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                      <span>{item}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState message="Fertilizer recommendations are not available for this prediction." />
              )}
            </div>
          )}

          {/* Irrigation */}
          {activeTab === 'irrigation' && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-slate-900">
                Irrigation & Soil Moisture Guidelines
              </h3>

              {irrigationItems.length > 0 ? (
                <div className="grid grid-cols-1 gap-3">
                  {irrigationItems.map((item, idx) => (
                    <div
                      key={idx}
                      className="p-4 rounded-xl bg-sky-50/50 border border-sky-200/70 flex items-start gap-3 text-sm text-slate-700"
                    >
                      <Droplets className="w-5 h-5 text-sky-600 shrink-0 mt-0.5" />
                      <span>{item}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState message="Irrigation recommendations are not available for this prediction." />
              )}
            </div>
          )}

          {/* Prevention */}
          {activeTab === 'prevention' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-base font-bold text-slate-900 mb-3">
                  Long-Term Field Sanitation & Prevention
                </h3>

                {preventionItems.length > 0 ? (
                  <div className="grid grid-cols-1 gap-3">
                    {preventionItems.map((item, idx) => (
                      <div
                        key={idx}
                        className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex items-start gap-3 text-sm text-slate-700"
                      >
                        <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                        <span>{item}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <EmptyState message="Detailed prevention recommendations are not available for this prediction." />
                )}
              </div>

              {recoveryItems.length > 0 && (
                <div className="pt-4 border-t border-slate-100">
                  <h4 className="text-sm font-bold text-slate-800 mb-2">
                    Canopy Recovery Protocols
                  </h4>

                  <ul className="list-disc list-inside space-y-1.5 text-xs sm:text-sm text-slate-600">
                    {recoveryItems.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Top-3 Predictions */}
      {top_predictions.length > 0 && (
        <div className="bg-slate-50 rounded-2xl border border-slate-200/80 p-6 space-y-4 print:hidden">

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-emerald-700" />

              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800">
                Model Prediction Distribution
              </h3>
            </div>

            <span className="text-xs text-slate-500">
              Top-{top_predictions.length} Candidates
            </span>
          </div>

          <p className="text-xs text-slate-500">
            These values represent the model's softmax probabilities for the
            highest-ranked classes.
          </p>

          <div className="space-y-3">
            {top_predictions.map((item, idx) => {
              const itemConfidence = Number(item.confidence || 0);
              const pct = Math.round(itemConfidence * 100);

              return (
                <div key={idx} className="space-y-1">

                  <div className="flex justify-between gap-4 text-xs font-semibold text-slate-700">
                    <span className="truncate">
                      {item.crop}: {item.disease}
                    </span>

                    <span className="font-mono shrink-0">
                      {pct}% ({itemConfidence.toFixed(4)})
                    </span>
                  </div>

                  <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-2 rounded-full transition-all duration-500 ${
                        idx === 0
                          ? 'bg-emerald-600'
                          : 'bg-slate-400'
                      }`}
                      style={{
                        width: `${Math.min(100, Math.max(0, pct))}%`,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Bottom CTA */}
      <div className="text-center pt-4 print:hidden">
        <button
          onClick={onReset}
          className="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-semibold shadow-md transition-all inline-flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Diagnose Another Plant Specimen</span>
        </button>
      </div>
    </div>
  );
}

/* Small reusable empty-state component */
function EmptyState({ message }) {
  return (
    <div className="p-4 rounded-xl border border-slate-200 bg-slate-50 text-sm text-slate-500 flex items-start gap-3">
      <Info className="w-5 h-5 text-slate-400 shrink-0 mt-0.5" />
      <span>{message}</span>
    </div>
  );
}