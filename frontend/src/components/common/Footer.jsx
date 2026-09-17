import React from 'react';
import { Sprout, ShieldCheck, Heart, ExternalLink } from 'lucide-react';

export default function Footer({ setActivePage }) {
  return (
    <footer className="bg-slate-900 text-slate-400 border-t border-slate-800 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand & Project Mission */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-2 text-white">
              <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center">
                <Sprout className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-lg tracking-tight">Plant Disease AI</span>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed max-w-md">
              A computer vision and transfer-learning application designed for early botanical disease diagnosis, 
              lesion severity quantification, and deterministic agronomic guidance.
            </p>
            <div className="flex items-center gap-4 text-xs text-slate-400">
              <span className="inline-flex items-center gap-1">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                Zero Hallucination Protocol
              </span>
              <span>•</span>
              <span>ROSP Laboratory Project</span>
            </div>
          </div>

          {/* Supported Crops */}
          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-3">Supported Crops</h4>
            <ul className="space-y-2 text-sm">
              <li className="flex items-center gap-2 hover:text-emerald-400 transition-colors">
                <span className="w-1.5 h-1.5 rounded-full bg-rose-500" />
                <span>Strawberry (2 classes)</span>
              </li>
              <li className="flex items-center gap-2 hover:text-emerald-400 transition-colors">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                <span>Rice (4 classes)</span>
              </li>
              <li className="flex items-center gap-2 hover:text-emerald-400 transition-colors">
                <span className="w-1.5 h-1.5 rounded-full bg-red-500" />
                <span>Tomato (7 classes)</span>
              </li>
            </ul>
          </div>

          {/* Navigation Links */}
          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-3">Academic Project</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <button 
                  onClick={() => setActivePage('about')}
                  className="hover:text-emerald-400 transition-colors text-left"
                >
                  Methodology & Metrics
                </button>
              </li>
              <li>
                <button 
                  onClick={() => setActivePage('diseases')}
                  className="hover:text-emerald-400 transition-colors text-left"
                >
                  Disease Knowledge Base
                </button>
              </li>
              <li>
                <button 
                  onClick={() => setActivePage('detect')}
                  className="hover:text-emerald-400 transition-colors text-left"
                >
                  Live Detection Lab
                </button>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© {new Date().getFullYear()} Plant Disease AI. Final-Year Laboratory Capstone.</p>
          <p className="flex items-center gap-1">
            Built with TensorFlow, OpenCV, FastAPI & React
          </p>
        </div>
      </div>
    </footer>
  );
}
