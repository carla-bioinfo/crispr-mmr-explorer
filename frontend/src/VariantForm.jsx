import { useState } from 'react';
import axios from 'axios';

export default function VariantForm({ onResultReceived }) {
  const [formData, setFormData] = useState({
    gene: 'MLH1',
    chromosome: '3',
    position: '',
    ref: '',
    alt: '',
    allele_frequency: 0.0001,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const genes = [
    { value: 'MLH1', label: 'MLH1', color: 'bg-blue-500' },
    { value: 'MSH2', label: 'MSH2', color: 'bg-orange-500' },
    { value: 'MSH6', label: 'MSH6', color: 'bg-green-500' },
    { value: 'PMS2', label: 'PMS2', color: 'bg-purple-500' },
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/api/classify', formData);
      onResultReceived(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao classificar variante');
    } finally {
      setLoading(false);
    }
  };

  const selectedGene = genes.find(g => g.value === formData.gene);

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-semibold text-slate-200 mb-2">Gene MMR</label>
        <select
          name="gene"
          value={formData.gene}
          onChange={handleInputChange}
          className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3 hover:border-blue-500/60 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
        >
          {genes.map(g => <option key={g.value} value={g.value}>{g.label}</option>)}
        </select>
        {selectedGene && (
          <div className="mt-2 flex gap-2">
            <span className={`${selectedGene.color} text-white text-xs font-bold px-3 py-1 rounded-full`}>
              {selectedGene.label}
            </span>
          </div>
        )}
      </div>

      <div>
        <label className="block text-sm font-semibold text-slate-200 mb-2">Cromossomo</label>
        <input
          type="text"
          name="chromosome"
          value={formData.chromosome}
          onChange={handleInputChange}
          placeholder="3, 2, X, Y"
          className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3 hover:border-blue-500/60 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
        />
      </div>

      <div>
        <label className="block text-sm font-semibold text-slate-200 mb-2">Posição (bp)</label>
        <input
          type="number"
          name="position"
          value={formData.position}
          onChange={handleInputChange}
          placeholder="37034841"
          className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3 hover:border-blue-500/60 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
        />
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-semibold text-slate-200 mb-2">Ref</label>
          <input
            type="text"
            name="ref"
            value={formData.ref}
            onChange={handleInputChange}
            placeholder="A"
            maxLength="1"
            className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3 hover:border-blue-500/60 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all text-center font-bold"
          />
        </div>
        <div>
          <label className="block text-sm font-semibold text-slate-200 mb-2">Alt</label>
          <input
            type="text"
            name="alt"
            value={formData.alt}
            onChange={handleInputChange}
            placeholder="G"
            maxLength="1"
            className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3 hover:border-blue-500/60 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all text-center font-bold"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-semibold text-slate-200 mb-2">Freq. Alélica (gnomAD)</label>
        <input
          type="number"
          name="allele_frequency"
          value={formData.allele_frequency}
          onChange={handleInputChange}
          step="0.00001"
          placeholder="0.0001"
          className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3 hover:border-blue-500/60 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
        />
      </div>

      {error && (
        <div className="bg-red-500/20 border border-red-500/50 text-red-300 p-3 rounded-lg text-sm flex items-start gap-2">
          <span className="text-lg">⚠️</span>
          <div>{error}</div>
        </div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-bold py-3 px-4 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl hover:scale-105 active:scale-95"
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <span className="animate-spin">⚙️</span>
            Classificando...
          </span>
        ) : (
          <span className="flex items-center justify-center gap-2">
            <span>🔍</span>
            Classificar Variante
          </span>
        )}
      </button>
    </form>
  );
}
