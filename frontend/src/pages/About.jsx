import React, { useState, useEffect } from 'react';
import { 
  GraduationCap, 
  Cpu, 
  Database, 
  CheckCircle2, 
  FileText, 
  ShieldCheck, 
  Activity,
  Layers,
  BarChart3
} from 'lucide-react';
import { getEvaluationMetrics } from '../services/api';

export default function About() {
  const [evalData, setEvalData] = useState(null);

  useEffect(() => {
    getEvaluationMetrics()
      .then((res) => {
        if (res.status === 'available') {
          setEvalData(res.metrics);
        }
      })
      .catch(() => {});
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10 space-y-12">
      {/* Title */}
      <div className="text-center space-y-3 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold uppercase tracking-wider">
          <GraduationCap className="w-4 h-4 text-emerald-700" />
          <span>Final-Year Capstone / ROSP Laboratory AI Project</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
          System Architecture & Academic Methodology
        </h1>
        <p className="text-sm sm:text-base text-slate-600 leading-relaxed">
          Comprehensive technical defense documentation detailing dataset partitioning, 
          transfer learning dynamics, deterministic vision algorithms, and real evaluation metrics.
        </p>
      </div>

      {/* 4 Pillars of Academic Rigor */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-2xs space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Academic Integrity & Isolated Test Set</h3>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            The dataset is strictly partitioned into a 70% Training, 15% Validation, and 15% Held-Out Test split. 
            The test set remains completely isolated and is never exposed to model weight updates or hyperparameter selection, 
            guaranteeing zero data leakage.
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-2xs space-y-3">
          <div className="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center">
            <Layers className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Two-Stage Transfer Learning</h3>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            Leverages a pretrained ImageNet CNN backbone (MobileNetV3-Large). 
            Stage 1 trains the customized dense head with a frozen backbone. 
            Stage 2 unfreezes upper convolution blocks with fine-grained low learning rates (5e-5) to adapt botanical feature kernels.
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-2xs space-y-3">
          <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center">
            <Activity className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Deterministic OpenCV Severity</h3>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            Rather than hallucinating severity or using random heuristics, the system utilizes OpenCV HSV color space masking 
            to isolate green leaf tissue, extract chlorotic and necrotic lesion contours, and compute mathematical surface ratios.
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-2xs space-y-3">
          <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center">
            <Database className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-slate-900">Decoupled Agronomic Knowledge Base</h3>
          <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
            Agricultural treatments, chemical active ingredients, and fertilizer advice are stored in an independent JSON registry. 
            The deep learning model predicts the pathology class, while the recommendation engine deterministically serves verified guidance.
          </p>
        </div>
      </div>

      {/* Live Held-Out Test Evaluation Dashboard */}
      <div className="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-sm space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-700">
              Verified Evaluation Metrics
            </span>
            <h2 className="text-xl font-bold text-slate-900 mt-1">
              Held-Out Test Set Performance Report
            </h2>
          </div>
          <div className="text-xs text-slate-500 font-mono">
            {evalData ? `Test Samples: ${evalData.total_test_samples}` : 'Awaiting Model Evaluation Run'}
          </div>
        </div>

        {evalData ? (
          <div className="space-y-6">
            {/* Metric Score Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
                <p className="text-xs text-slate-500 uppercase font-semibold">Test Accuracy</p>
                <p className="text-2xl font-black text-emerald-700 mt-1">
                  {(evalData.overall_accuracy * 100).toFixed(2)}%
                </p>
              </div>
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
                <p className="text-xs text-slate-500 uppercase font-semibold">Macro Precision</p>
                <p className="text-2xl font-black text-slate-800 mt-1">
                  {(evalData.macro_precision * 100).toFixed(2)}%
                </p>
              </div>
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
                <p className="text-xs text-slate-500 uppercase font-semibold">Macro Recall</p>
                <p className="text-2xl font-black text-slate-800 mt-1">
                  {(evalData.macro_recall * 100).toFixed(2)}%
                </p>
              </div>
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
                <p className="text-xs text-slate-500 uppercase font-semibold">Macro F1-Score</p>
                <p className="text-2xl font-black text-emerald-700 mt-1">
                  {(evalData.macro_f1 * 100).toFixed(2)}%
                </p>
              </div>
            </div>

            {/* Confusion Matrix Display */}
            {evalData.confusion_matrix && (
              <div className="space-y-3 pt-4 border-t border-slate-100">
                <h4 className="text-sm font-bold text-slate-800">
                  Normalized Confusion Matrix Heatmap
                </h4>
                <div className="rounded-2xl border border-slate-200 overflow-hidden bg-slate-50 p-2 text-center">
                  <img
                    src="/api/static/models/confusion_matrix.png"
                    alt="Confusion Matrix"
                    className="max-h-96 mx-auto object-contain rounded-xl"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                  <p className="text-xs text-slate-400 mt-2 font-mono">
                    Evaluation Matrix rendered on held-out test split without training contamination.
                  </p>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="p-8 rounded-2xl bg-slate-50 border border-slate-200 text-center space-y-2">
            <BarChart3 className="w-8 h-8 text-slate-400 mx-auto" />
            <p className="text-sm font-semibold text-slate-700">
              Model Training & Evaluation Scheduled
            </p>
            <p className="text-xs text-slate-500 max-w-md mx-auto">
              Evaluation metrics are calculated after running <code className="bg-slate-200 px-1 py-0.5 rounded">ml/evaluation/evaluate.py</code> on the held-out test split. No artificial metrics are simulated.
            </p>
          </div>
        )}
      </div>

      {/* Assumptions and Limitations */}
      <div className="bg-slate-50 rounded-2xl border border-slate-200 p-6 space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-800">
          Academic Assumptions & Limitations
        </h3>
        <ul className="space-y-2 text-xs sm:text-sm text-slate-600 list-disc list-inside">
          <li>Foliar images must depict adequate illumination without extreme glare or shadows.</li>
          <li>In multi-infection scenarios (e.g., both Early and Late Blight present), the model predicts the dominant visual symptom.</li>
          <li>Chemical recommendations specify standard active ingredients; local agricultural extension guidelines must be verified before field spraying.</li>
        </ul>
      </div>
    </div>
  );
}
