import React, { useState } from 'react';
import Navbar from './components/common/Navbar';
import Footer from './components/common/Footer';
import Home from './pages/Home';
import Detect from './pages/Detect';
import Result from './pages/Result';
import DiseaseDirectory from './pages/DiseaseDirectory';
import About from './pages/About';

export default function App() {
  const [activePage, setActivePage] = useState('home');
  const [currentDiagnosis, setCurrentDiagnosis] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);

  const handleDiagnosisComplete = (diagnosisResult, imageUrl) => {
    setCurrentDiagnosis(diagnosisResult);
    setPreviewImage(imageUrl);
    setActivePage('result');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleResetDiagnosis = () => {
    setCurrentDiagnosis(null);
    setPreviewImage(null);
    setActivePage('detect');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 selection:bg-emerald-200">
      <Navbar activePage={activePage} setActivePage={setActivePage} />

      <main className="flex-1">
        {activePage === 'home' && <Home setActivePage={setActivePage} />}
        {activePage === 'detect' && (
          <Detect onDiagnosisComplete={handleDiagnosisComplete} />
        )}
        {activePage === 'result' && (
          <Result
            result={currentDiagnosis}
            previewImage={previewImage}
            onReset={handleResetDiagnosis}
          />
        )}
        {activePage === 'diseases' && <DiseaseDirectory />}
        {activePage === 'about' && <About />}
      </main>

      <Footer setActivePage={setActivePage} />
    </div>
  );
}
