import React, { useState, useEffect } from 'react';
import { Sprout, Activity, BookOpen, Info, ShieldCheck, AlertCircle } from 'lucide-react';
import { getHealthStatus } from '../../services/api';

export default function Navbar({ activePage, setActivePage }) {
  const [systemHealth, setSystemHealth] = useState({ online: false, modelLoaded: false });

  useEffect(() => {
    getHealthStatus()
      .then((data) => {
        setSystemHealth({
          online: data.status === 'healthy',
          modelLoaded: data.model_loaded,
        });
      })
      .catch(() => {
        setSystemHealth({ online: false, modelLoaded: false });
      });
  }, []);

  const navItems = [
    { id: 'home', label: 'Home', icon: Sprout },
    { id: 'detect', label: 'Disease Detection', icon: Activity },
    { id: 'diseases', label: 'Disease Information', icon: BookOpen },
    { id: 'about', label: 'About Project', icon: Info },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-emerald-100 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <div 
            onClick={() => setActivePage('home')}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-600 to-emerald-800 flex items-center justify-center text-white shadow-md shadow-emerald-700/20 group-hover:scale-105 transition-transform">
              <Sprout className="w-6 h-6 text-emerald-100" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-lg text-emerald-950 tracking-tight">Plant Disease AI</span>
                <span className="text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                  Academic
                </span>
              </div>
              <p className="text-[11px] text-slate-500 hidden sm:block">Prediction & Smart Recommendation System</p>
            </div>
          </div>

          {/* Desktop Nav Items */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activePage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActivePage(item.id)}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-emerald-50 text-emerald-700 border border-emerald-200/80 shadow-xs'
                      : 'text-slate-600 hover:text-emerald-700 hover:bg-slate-50'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-600' : 'text-slate-400'}`} />
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* System Status Pill */}
          <div className="flex items-center gap-3">
            <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-50 border border-slate-200 text-xs">
              <span className="relative flex h-2 w-2">
                <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                  systemHealth.online ? 'bg-emerald-400' : 'bg-amber-400'
                }`} />
                <span className={`relative inline-flex rounded-full h-2 w-2 ${
                  systemHealth.online ? 'bg-emerald-500' : 'bg-amber-500'
                }`} />
              </span>
              <span className="font-medium text-slate-600">
                {systemHealth.online ? 'AI Engine Ready' : 'Backend Initializing'}
              </span>
            </div>

            <button
              onClick={() => setActivePage('detect')}
              className="bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium px-4 py-2 rounded-lg shadow-sm hover:shadow transition-all flex items-center gap-1.5"
            >
              <Activity className="w-4 h-4" />
              <span>Diagnose Leaf</span>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Bar */}
      <div className="md:hidden flex items-center justify-around border-t border-slate-100 bg-white px-2 py-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activePage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              className={`flex flex-col items-center gap-1 p-2 rounded-lg text-[11px] font-medium transition-colors ${
                isActive ? 'text-emerald-700 font-semibold' : 'text-slate-500'
              }`}
            >
              <Icon className={`w-5 h-5 ${isActive ? 'text-emerald-600' : 'text-slate-400'}`} />
              {item.label}
            </button>
          );
        })}
      </div>
    </header>
  );
}
