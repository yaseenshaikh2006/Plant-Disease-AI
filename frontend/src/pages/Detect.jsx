import React, { useState, useRef } from 'react';
import { 
  UploadCloud, 
  Image as ImageIcon, 
  Activity, 
  AlertCircle, 
  CheckCircle, 
  X, 
  RefreshCw,
  Sparkles,
  Camera
} from 'lucide-react';
import { predictDisease } from '../services/api';

export default function Detect({ onDiagnosisComplete }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [selectedCrop, setSelectedCrop] = useState('auto');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);

  // Sample leaves for rapid demonstration during academic presentation
  const demoSamples = [
    { label: 'Strawberry Scorch', crop: 'strawberry', url: '/sample_images/strawberry_scorch.jpg' },
    { label: 'Rice Blight', crop: 'rice', url: '/sample_images/rice_blight.jpg' },
    { label: 'Tomato Early Blight', crop: 'tomato', url: '/sample_images/tomato_early_blight.jpg' },
    { label: 'Healthy Tomato', crop: 'tomato', url: '/sample_images/tomato_healthy.jpg' }
  ];

  const handleFileChange = (file) => {
    setErrorMessage(null);
    if (!file) return;

    // Client-side quick validation
    const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/bmp'];
    if (!validTypes.includes(file.type)) {
      setErrorMessage('Unsupported file format. Please select a JPEG, PNG, or WEBP photograph.');
      return;
    }

    if (file.size > 15 * 1024 * 1024) {
      setErrorMessage('Image exceeds the 15MB file size limit. Please upload a smaller image.');
      return;
    }

    setSelectedFile(file);
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const clearSelection = () => {
    setSelectedFile(null);
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setErrorMessage(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleDemoSelect = async (sample) => {
    try {
      setIsLoading(true);
      setErrorMessage(null);
      const res = await fetch(sample.url);
      if (!res.ok) throw new Error('Sample image unavailable.');
      const blob = await res.blob();
      const file = new File([blob], `${sample.label.toLowerCase().replace(/\s+/g, '_')}.jpg`, { type: 'image/jpeg' });
      setSelectedCrop(sample.crop);
      handleFileChange(file);
    } catch (err) {
      setErrorMessage(`Failed to load sample image: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitDiagnosis = async () => {
    if (!selectedFile) {
      setErrorMessage('Please upload or select a leaf photograph first.');
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      const result = await predictDisease(selectedFile, selectedCrop);
      onDiagnosisComplete(result, previewUrl);
    } catch (err) {
      setErrorMessage(err.message || 'An error occurred during disease analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-10 space-y-8">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">
          Plant Disease Diagnosis Lab
        </h1>
        <p className="text-sm sm:text-base text-slate-600">
          Upload a clear photograph of a plant leaf showing suspicious symptoms or lesions.
        </p>
      </div>

      {/* Validation / Error Notification Banner */}
      {errorMessage && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-3 shadow-xs">
          <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="font-semibold">Validation Notice</p>
            <p className="text-rose-700 mt-0.5">{errorMessage}</p>
          </div>
          <button onClick={() => setErrorMessage(null)} className="text-rose-500 hover:text-rose-800">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Main Upload Card */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden p-6 sm:p-8 space-y-6">
        {/* Crop Selection Option */}
        <div className="space-y-2">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700">
            Select Crop Species (Optional)
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
            {[
              { id: 'auto', name: 'Auto Detect Crop' },
              { id: 'strawberry', name: 'Strawberry' },
              { id: 'rice', name: 'Rice' },
              { id: 'tomato', name: 'Tomato' },
            ].map((c) => (
              <button
                key={c.id}
                type="button"
                onClick={() => setSelectedCrop(c.id)}
                className={`px-3 py-2.5 rounded-xl text-xs font-semibold border transition-all text-center ${
                  selectedCrop === c.id
                    ? 'bg-emerald-600 text-white border-emerald-600 shadow-xs'
                    : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                }`}
              >
                {c.name}
              </button>
            ))}
          </div>
        </div>

        {/* Dropzone / Preview Area */}
        {!previewUrl ? (
          <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center cursor-pointer transition-all ${
              isDragOver
                ? 'border-emerald-500 bg-emerald-50/50 scale-[0.99]'
                : 'border-slate-300 hover:border-emerald-400 bg-slate-50/50 hover:bg-emerald-50/20'
            }`}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={(e) => e.target.files && handleFileChange(e.target.files[0])}
              accept="image/jpeg,image/png,image/webp,image/bmp"
              className="hidden"
            />
            <div className="w-16 h-16 rounded-2xl bg-emerald-100 text-emerald-700 mx-auto flex items-center justify-center mb-4 shadow-xs">
              <UploadCloud className="w-8 h-8" />
            </div>
            <h3 className="text-base font-bold text-slate-800 mb-1">
              Drag and drop your leaf photograph here
            </h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto mb-4">
              Supports JPEG, PNG, WEBP, and BMP up to 15MB. Ensure high illumination and focus on the lesion area.
            </p>
            <div className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-white border border-slate-200 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50">
              <Camera className="w-4 h-4 text-emerald-600" />
              <span>Browse Local Files</span>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="relative rounded-2xl border border-slate-200 bg-slate-900 overflow-hidden flex items-center justify-center max-h-[380px]">
              <img
                src={previewUrl}
                alt="Selected Leaf Preview"
                className="max-h-[380px] w-auto object-contain"
              />
              <button
                onClick={clearSelection}
                className="absolute top-3 right-3 p-2 rounded-full bg-black/60 hover:bg-black/80 text-white backdrop-blur transition-all"
                title="Remove image"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="flex items-center justify-between text-xs text-slate-500 px-1">
              <span className="truncate max-w-xs font-mono">{selectedFile?.name}</span>
              <span>{(selectedFile?.size ? (selectedFile.size / (1024 * 1024)).toFixed(2) : 0)} MB</span>
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="pt-2">
          <button
            onClick={handleSubmitDiagnosis}
            disabled={!selectedFile || isLoading}
            className={`w-full py-3.5 rounded-xl font-bold text-sm shadow-md transition-all flex items-center justify-center gap-2 ${
              !selectedFile || isLoading
                ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                : 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-emerald-700/20 hover:shadow-lg'
            }`}
          >
            {isLoading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin text-emerald-200" />
                <span>Running Deep Learning & Vision Pipeline...</span>
              </>
            ) : (
              <>
                <Activity className="w-4 h-4" />
                <span>Diagnose Plant Disease</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Quick Test Demo Samples (Helpful for academic demo) */}
      <div className="bg-slate-50 rounded-2xl border border-slate-200/80 p-5 space-y-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-emerald-600" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">
            Quick Demonstration Benchmark Samples
          </h3>
        </div>
        <p className="text-xs text-slate-500">
          Click any reference sample below to instantly load an academic benchmark image into the diagnosis pipeline:
        </p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          {demoSamples.map((sample, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleDemoSelect(sample)}
              disabled={isLoading}
              className="p-2 rounded-xl bg-white border border-slate-200 hover:border-emerald-300 hover:bg-emerald-50/50 text-left text-xs font-medium text-slate-700 transition-all flex items-center gap-2 shadow-2xs"
            >
              <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0" />
              <span className="truncate">{sample.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
