import React, { useState, useEffect } from 'react';
import { Search, Filter, BookOpen, AlertCircle, ShieldCheck, ChevronRight, X } from 'lucide-react';
import { getDiseaseCatalog } from '../services/api';

export default function DiseaseDirectory() {
  const [diseases, setDiseases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCrop, setSelectedCrop] = useState('all');
  const [activeModalDisease, setActiveModalDisease] = useState(null);

  useEffect(() => {
    getDiseaseCatalog()
      .then((res) => {
        setDiseases(res.diseases || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load disease directory:', err);
        setLoading(false);
      });
  }, []);

  const filteredDiseases = diseases.filter((d) => {
    const matchesCrop = selectedCrop === 'all' || d.crop.toLowerCase() === selectedCrop.toLowerCase();
    const query = searchQuery.toLowerCase();
    const matchesSearch = 
      d.disease.toLowerCase().includes(query) ||
      d.crop.toLowerCase().includes(query) ||
      d.pathogen.toLowerCase().includes(query) ||
      d.description.toLowerCase().includes(query);
    return matchesCrop && matchesSearch;
  });

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10 space-y-8">
      {/* Header */}
      <div className="text-center space-y-2 max-w-2xl mx-auto">
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">
          Disease Knowledge Encyclopedia
        </h1>
        <p className="text-sm sm:text-base text-slate-600">
          Curated botanical repository with etiology, clinical symptoms, and verified organic & chemical treatments.
        </p>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-2xs p-4 sm:p-5 flex flex-col sm:flex-row gap-3 items-center justify-between">
        {/* Search input */}
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search disease, pathogen, or symptoms..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs sm:text-sm text-slate-900 placeholder:text-slate-400 focus:outline-emerald-600 focus:bg-white transition-all"
          />
        </div>

        {/* Crop Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
          {[
            { id: 'all', label: 'All Crops' },
            { id: 'strawberry', label: 'Strawberry' },
            { id: 'rice', label: 'Rice' },
            { id: 'tomato', label: 'Tomato' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setSelectedCrop(tab.id)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                selectedCrop === tab.id
                  ? 'bg-emerald-600 text-white shadow-2xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Disease Cards Grid */}
      {loading ? (
        <div className="py-16 text-center text-slate-500 text-sm">
          Loading catalog records from agronomic knowledge base...
        </div>
      ) : filteredDiseases.length === 0 ? (
        <div className="py-16 text-center text-slate-500 text-sm">
          No catalog records found matching "{searchQuery}".
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredDiseases.map((item, idx) => {
            const isHealthy = item.disease.toLowerCase().includes('healthy');
            return (
              <div
                key={idx}
                onClick={() => setActiveModalDisease(item)}
                className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-2xs hover:border-emerald-300 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between group"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200">
                      {item.crop}
                    </span>
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                      isHealthy ? 'bg-green-100 text-green-800' : 'bg-rose-100 text-rose-800'
                    }`}>
                      {isHealthy ? 'Healthy Class' : 'Pathogenic'}
                    </span>
                  </div>

                  <div>
                    <h3 className="text-base font-bold text-slate-900 group-hover:text-emerald-700 transition-colors">
                      {item.disease}
                    </h3>
                    <p className="text-[11px] font-mono text-slate-400 truncate mt-0.5">
                      {item.pathogen}
                    </p>
                  </div>

                  <p className="text-xs text-slate-600 line-clamp-3 leading-relaxed">
                    {item.description}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-emerald-700 font-semibold group-hover:translate-x-0.5 transition-transform">
                  <span>View Management Protocol</span>
                  <ChevronRight className="w-4 h-4" />
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Disease Detail Modal */}
      {activeModalDisease && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs">
          <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-slate-200 shadow-2xl p-6 sm:p-8 space-y-6">
            <div className="flex items-start justify-between border-b border-slate-100 pb-4">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-700">
                  {activeModalDisease.crop} Pathogen Profile
                </span>
                <h2 className="text-2xl font-black text-slate-900 mt-1">
                  {activeModalDisease.disease}
                </h2>
                <p className="text-xs font-mono text-slate-500 mt-0.5">
                  {activeModalDisease.pathogen}
                </p>
              </div>
              <button
                onClick={() => setActiveModalDisease(null)}
                className="p-1.5 rounded-full hover:bg-slate-100 text-slate-500"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4 text-xs sm:text-sm">
              <div>
                <h4 className="font-bold text-slate-900 mb-1">Clinical Overview</h4>
                <p className="text-slate-600 leading-relaxed">{activeModalDisease.description}</p>
              </div>

              {activeModalDisease.symptoms?.length > 0 && (
                <div>
                  <h4 className="font-bold text-slate-900 mb-2">Key Diagnostic Symptoms</h4>
                  <ul className="list-disc list-inside space-y-1 text-slate-600">
                    {activeModalDisease.symptoms.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
              )}

              {activeModalDisease.treatment?.organic && (
                <div>
                  <h4 className="font-bold text-emerald-800 mb-1.5">Organic & Biological Controls</h4>
                  <ul className="space-y-1 text-slate-600">
                    {activeModalDisease.treatment.organic.map((t, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-emerald-600 font-bold">•</span>
                        <span>{t}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {activeModalDisease.treatment?.chemical && (
                <div>
                  <h4 className="font-bold text-amber-800 mb-1.5">Chemical Treatments & Fungicides</h4>
                  <ul className="space-y-1 text-slate-600">
                    {activeModalDisease.treatment.chemical.map((t, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-amber-600 font-bold">•</span>
                        <span>{t}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="pt-4 border-t border-slate-100 text-right">
              <button
                onClick={() => setActiveModalDisease(null)}
                className="px-5 py-2 rounded-xl bg-slate-900 text-white font-semibold text-xs hover:bg-slate-800"
              >
                Close Profile
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
