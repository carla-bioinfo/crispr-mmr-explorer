import { useState } from 'react';
import VariantForm from './VariantForm';
import ResultDisplay from './ResultDisplay';
import './App.css';

export default function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <header className="sticky top-0 z-50 backdrop-blur-md bg-slate-900/80 border-b border-blue-500/20">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="text-3xl">🧬</div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                CRISPR-MMR Explorer
              </h1>
              <p className="text-sm text-blue-300/70">Classificação ACMG de variantes Mismatch Repair</p>
            </div>
          </div>
          <div className="hidden md:flex gap-2">
            <span className="px-3 py-1 bg-blue-500/20 text-blue-300 rounded-full text-xs font-semibold">
              v2.0.2
            </span>
            <span className="px-3 py-1 bg-green-500/20 text-green-300 rounded-full text-xs font-semibold">
              Backend: ✓
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <div className="sticky top-24">
              <div className="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl border border-blue-500/20 shadow-2xl overflow-hidden">
                <div className="bg-gradient-to-r from-blue-600 to-cyan-600 p-4">
                  <h2 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>📋</span> Dados da Variante
                  </h2>
                </div>
                <div className="p-6">
                  <VariantForm onResultReceived={setResult} />
                </div>
              </div>
            </div>
          </div>

          <div className="lg:col-span-2">
            {result ? (
              <div className="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl border border-blue-500/20 shadow-2xl overflow-hidden">
                <div className="bg-gradient-to-r from-blue-600 to-cyan-600 p-4">
                  <h2 className="text-lg font-bold text-white flex items-center gap-2">
                    <span>📊</span> Resultado da Classificação
                  </h2>
                </div>
                <div className="p-8">
                  <ResultDisplay result={result} />
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-96 bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl border border-blue-500/20 border-dashed">
                <div className="text-6xl mb-4">🔬</div>
                <p className="text-xl text-slate-300 font-semibold">Aguardando análise</p>
                <p className="text-sm text-slate-400 mt-2">Preencha os dados e clique em "Classificar"</p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="border-t border-blue-500/20 mt-16 py-8 bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-6 text-center text-slate-400 text-sm">
          <p>CRISPR-MMR Explorer v2.0.2 • Classificação baseada em ACMG/AMP 2015 • ClinGen InSiGHT VCEP</p>
        </div>
      </footer>
    </div>
  );
}
