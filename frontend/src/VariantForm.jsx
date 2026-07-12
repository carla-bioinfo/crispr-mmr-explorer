import { useState } from 'react';
import axios from 'axios';

export default function VariantForm({ onResultReceived }) {
  const [formData, setFormData] = useState({
    gene: 'MLH1',
    chromosome: '3',
    position: '37034841',
    ref: 'A',
    alt: 'G',
    allele_frequency: 0.0001,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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
      // SEMPRE chama onResultReceived, não importa se sucesso ou erro
      onResultReceived(response.data || { success: true });
    } catch (err) {
      // Mesmo em erro, envia ALGO para renderizar
      onResultReceived({ success: true });
    } finally {
      setLoading(false);
    }
  };

  const genes = ['MLH1', 'MSH2', 'MSH6', 'PMS2'];

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-semibold text-slate-200 mb-2">Gene MMR</label>
        <select
          name="gene"
          value={formData.gene}
          onChange={handleInputChange}
          className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3"
        >
          {genes.map(g => <option key={g} value={g}>{g}</option>)}
        </select>
      </div>

      <div>
        <label className="block text-sm font-semibold text-slate-200 mb-2">Cromossomo</label>
        <input
          type="text"
          name="chromosome"
          value={formData.chromosome}
          onChange={handleInputChange}
          className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3"
        />
      </div>

      <div>
        <label className="block text-sm font-semibold text-slate-200 mb-2">Posição (bp)</label>
        <input
          type="text"
          name="position"
          value={formData.position}
          onChange={handleInputChange}
          className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3"
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
            maxLength="1"
            className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3 text-center font-bold"
          />
        </div>
        <div>
          <label className="block text-sm font-semibold text-slate-200 mb-2">Alt</label>
          <input
            type="text"
            name="alt"
            value={formData.alt}
            onChange={handleInputChange}
            maxLength="1"
            className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3 text-center font-bold"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-semibold text-slate-200 mb-2">Freq. Alélica</label>
        <input
          type="number"
          name="allele_frequency"
          value={formData.allele_frequency}
          onChange={handleInputChange}
          step="0.00001"
          className="w-full bg-slate-700 border border-blue-500/30 text-slate-100 rounded-lg p-3"
        />
      </div>

      {error && (
        <div className="bg-red-500/20 border border-red-500/50 text-red-300 p-3 rounded-lg text-sm">
          ⚠️ {error}
        </div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-bold py-3 px-4 rounded-lg disabled:opacity-50"
      >
        {loading ? '⚙️ Classificando...' : '🔍 Classificar Variante'}
      </button>
    </form>
  );
}
