import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function ResultDisplay({ result }) {
  if (!result) return null;

  const chartData = [
    { name: 'PVS1', value: result.criteria.PVS1 || 0 },
    { name: 'PM2', value: result.criteria.PM2 || 0 },
    { name: 'PP3', value: result.criteria.PP3 || 0 },
    { name: 'BP4', value: result.criteria.BP4 || 0 },
  ];

  const classConfig = {
    PATHOGENIC: { color: 'from-red-600 to-red-700', bgColor: 'bg-red-500/20', icon: '🔴', textColor: 'text-red-300', borderColor: 'border-red-500/50' },
    LIKELY_PATHOGENIC: { color: 'from-orange-600 to-orange-700', bgColor: 'bg-orange-500/20', icon: '🟠', textColor: 'text-orange-300', borderColor: 'border-orange-500/50' },
    VUS: { color: 'from-yellow-600 to-yellow-700', bgColor: 'bg-yellow-500/20', icon: '🟡', textColor: 'text-yellow-300', borderColor: 'border-yellow-500/50' },
    LIKELY_BENIGN: { color: 'from-green-600 to-green-700', bgColor: 'bg-green-500/20', icon: '🟢', textColor: 'text-green-300', borderColor: 'border-green-500/50' },
    BENIGN: { color: 'from-blue-600 to-blue-700', bgColor: 'bg-blue-500/20', icon: '🔵', textColor: 'text-blue-300', borderColor: 'border-blue-500/50' },
  };

  const config = classConfig[result.pathogenicity_class] || classConfig.VUS;

  return (
    <div className="space-y-6">
      <div className={`bg-gradient-to-r ${config.color} rounded-xl border ${config.borderColor} p-6 shadow-lg`}>
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-3xl">{config.icon}</span>
              <h3 className="text-3xl font-bold text-white">{result.pathogenicity_class}</h3>
            </div>
            <p className="text-blue-100">Classificação ACMG/AMP 2015</p>
          </div>
          <div className="text-right">
            <div className="text-4xl font-bold text-white">{(result.confidence * 100).toFixed(0)}%</div>
            <p className="text-blue-100 text-sm">Confiança</p>
          </div>
        </div>
      </div>

      <div className="bg-slate-700/50 border border-slate-600/50 rounded-xl p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-slate-400 text-sm">Score Total ACMG</p>
            <p className="text-3xl font-bold text-blue-400">{result.score} pontos</p>
          </div>
          <div className="text-right">
            <p className="text-slate-400 text-sm">Interpretação</p>
            <p className="text-lg font-semibold text-slate-200">
              {result.score >= 6 ? '≥6 (Patogênico)' : 
               result.score >= 3 ? '3-5 (Provavelmente patogênico)' :
               result.score >= -2 ? '-2 a 2 (VUS)' : '≤-2 (Provavelmente benigno)'}
            </p>
          </div>
        </div>
      </div>

      <div className="bg-slate-700/50 border border-slate-600/50 rounded-xl p-6">
        <h4 className="font-semibold text-slate-200 mb-4 flex items-center gap-2">
          <span>📊</span> Critérios ACMG Aplicados
        </h4>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis dataKey="name" stroke="#cbd5e1" />
            <YAxis stroke="#cbd5e1" />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '8px' }}
              labelStyle={{ color: '#e2e8f0' }}
            />
            <Bar dataKey="value" fill="#3b82f6" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-slate-700/50 border border-slate-600/50 rounded-xl p-6">
        <h4 className="font-semibold text-slate-200 mb-3 flex items-center gap-2">
          <span>💡</span> Análise
        </h4>
        <p className="text-slate-300 leading-relaxed">{result.explanation}</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-slate-700/50 border border-slate-600/50 rounded-xl p-4">
          <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Classe</p>
          <p className="text-lg font-semibold text-slate-200">{result.pathogenicity_class}</p>
        </div>
        <div className="bg-slate-700/50 border border-slate-600/50 rounded-xl p-4">
          <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Score</p>
          <p className="text-lg font-semibold text-slate-200">{result.score} / {result.confidence.toFixed(3)}</p>
        </div>
      </div>
    </div>
  );
}
