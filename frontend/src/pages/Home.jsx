import React from 'react';
import { 
  Sprout, 
  Activity, 
  ShieldCheck, 
  Droplets, 
  Search, 
  TrendingUp, 
  Cpu, 
  FileCheck2, 
  ChevronRight,
  Sparkles,
  ArrowRight
} from 'lucide-react';

export default function Home({ setActivePage }) {
  const supportedCrops = [
    {
      name: 'Strawberry',
      botanical: 'Fragaria × ananassa',
      classes: 'Healthy, Leaf Scorch',
      badge: 'Berry Crop',
      color: 'from-rose-500/10 to-rose-600/5 border-rose-200 text-rose-800',
      iconColor: 'bg-rose-500 text-white',
      desc: 'Sensitive crown and foliar pathogen detection with special focus on Diplocarpon scorch necrosis.'
    },
    {
      name: 'Rice',
      botanical: 'Oryza sativa',
      classes: 'Healthy, Bacterial Blight, Brown Spot, Leaf Smut',
      badge: 'Cereal Grain',
      color: 'from-amber-500/10 to-amber-600/5 border-amber-200 text-amber-800',
      iconColor: 'bg-amber-500 text-white',
      desc: 'Critical staple cereal disease diagnosis distinguishing bacterial water-soaking from fungal sesame spots.'
    },
    {
      name: 'Tomato',
      botanical: 'Solanum lycopersicum',
      classes: 'Healthy, Bacterial Spot, Early Blight, Late Blight, Septoria, TYLCV, Mosaic Virus',
      badge: 'Solanaceous Crop',
      color: 'from-emerald-500/10 to-emerald-600/5 border-emerald-200 text-emerald-800',
      iconColor: 'bg-emerald-600 text-white',
      desc: 'Comprehensive multi-class solanaceous foliar diagnostic engine across fungal, bacterial, and viral vectors.'
    }
  ];

  const features = [
    {
      icon: Cpu,
      title: 'AI Disease Detection',
      desc: 'Transfer-learning convolutional neural network extracting fine botanical textures and lesion patterns.'
    },
    {
      icon: TrendingUp,
      title: 'Real Confidence Scoring',
      desc: 'Calibrated Softmax probability distributions evaluated on an isolated held-out test split.'
    },
    {
      icon: Activity,
      title: 'Computer Vision Severity',
      desc: 'Deterministic OpenCV HSV color and contour segmentation calculating exact lesion-to-leaf surface ratios.'
    },
    {
      icon: ShieldCheck,
      title: 'Zero-Hallucination Advice',
      desc: 'Curated agronomic knowledge bases ensuring 100% verified chemical, organic, and fertilizer guidance.'
    },
    {
      icon: Droplets,
      title: 'Smart Irrigation & Plant Care',
      desc: 'Tailored soil moisture, drip irrigation timing, and N-P-K nutrient balancing for fast recovery.'
    },
    {
      icon: FileCheck2,
      title: 'Prevention & Cultural Sanitation',
      desc: 'Long-term crop rotation guidelines, nursery tool sterilization, and pathogen containment practices.'
    }
  ];

  return (
    <div className="space-y-16 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-16 md:pt-20 md:pb-24 bg-gradient-to-b from-emerald-50/60 via-white to-slate-50 border-b border-emerald-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto space-y-6">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-100/80 border border-emerald-300 text-emerald-900 text-xs font-semibold tracking-wide">
              <Sparkles className="w-3.5 h-3.5 text-emerald-700" />
              <span>ROSP Laboratory AI Research Project</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-emerald-950 tracking-tight leading-none">
              Plant Disease AI
            </h1>

            <p className="text-xl sm:text-2xl font-medium text-emerald-800">
              Detect Early. Treat Smart. Grow Better.
            </p>

            <p className="text-base sm:text-lg text-slate-600 leading-relaxed">
              An intelligent agricultural diagnostics platform combining deep learning classification, 
              deterministic OpenCV lesion severity estimation, and an evidence-based agronomic recommendation engine.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <button
                onClick={() => setActivePage('detect')}
                className="w-full sm:w-auto px-7 py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-base shadow-lg shadow-emerald-700/20 hover:shadow-xl transition-all flex items-center justify-center gap-2 group"
              >
                <Activity className="w-5 h-5 text-emerald-200 group-hover:scale-110 transition-transform" />
                <span>Diagnose Leaf Disease</span>
                <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
              </button>

              <button
                onClick={() => setActivePage('diseases')}
                className="w-full sm:w-auto px-7 py-3.5 rounded-xl bg-white hover:bg-emerald-50 text-emerald-900 font-semibold text-base border border-emerald-200 shadow-xs hover:border-emerald-300 transition-all flex items-center justify-center gap-2"
              >
                <Search className="w-5 h-5 text-emerald-600" />
                <span>Disease Encyclopedia</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Supported Crops Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Supported Botanical Crops
          </h2>
          <p className="text-sm sm:text-base text-slate-600 mt-2">
            Targeted diagnostic models optimized for high-value berries, global cereal staples, and commercial solanaceous vegetables.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {supportedCrops.map((crop, idx) => (
            <div
              key={idx}
              className={`rounded-2xl border p-6 bg-gradient-to-br ${crop.color} hover:shadow-md transition-all flex flex-col justify-between`}
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-md bg-white/80 backdrop-blur border border-current/20">
                    {crop.badge}
                  </span>
                  <span className="text-xs italic text-slate-500">{crop.botanical}</span>
                </div>
                <h3 className="text-2xl font-bold text-slate-900 mb-2">{crop.name}</h3>
                <p className="text-sm text-slate-600 mb-4 leading-relaxed">{crop.desc}</p>
              </div>

              <div className="pt-4 border-t border-slate-200/60 mt-2">
                <p className="text-xs font-semibold text-slate-700 mb-1">Supported Pathogen Classes:</p>
                <p className="text-xs text-slate-600">{crop.classes}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Core Technology & Capabilities Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            End-to-End Diagnostic Pipeline
          </h2>
          <p className="text-sm sm:text-base text-slate-600 mt-2">
            Engineered to bridge high-precision computer vision with actionable field agronomy.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div
                key={idx}
                className="bg-white rounded-xl border border-slate-200/80 p-6 shadow-xs hover:border-emerald-200 hover:shadow-md transition-all"
              >
                <div className="w-11 h-11 rounded-lg bg-emerald-100/80 text-emerald-700 flex items-center justify-center mb-4">
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-base font-bold text-slate-900 mb-2">{feat.title}</h3>
                <p className="text-sm text-slate-600 leading-relaxed">{feat.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Process Workflow Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-r from-emerald-900 to-emerald-800 rounded-3xl p-8 sm:p-12 text-white shadow-xl">
          <div className="max-w-3xl">
            <h2 className="text-2xl sm:text-3xl font-bold mb-4">
              How the Diagnostic Engine Works
            </h2>
            <p className="text-emerald-100 text-sm sm:text-base mb-8 leading-relaxed">
              Every leaf upload traverses an automated 5-stage pipeline: File Validation &rarr; Transfer-Learning CNN Classification &rarr; OpenCV Color-Space Lesion Masking &rarr; Knowledge-Base Rule Mapping &rarr; Structured Prescription Generation.
            </p>
            <button
              onClick={() => setActivePage('detect')}
              className="px-6 py-3 rounded-xl bg-white text-emerald-900 hover:bg-emerald-50 font-bold text-sm shadow-md transition-all inline-flex items-center gap-2"
            >
              <span>Test with a Sample Leaf</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
