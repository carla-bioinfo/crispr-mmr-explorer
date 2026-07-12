export default function ResultDisplay({ result }) {
  if (!result) return null;

  // Não tenta acessar nada - só renderiza se houver resultado
  return (
    <div className="bg-yellow-600 rounded-xl p-8 text-white text-center">
      <h3 className="text-4xl font-bold mb-4">🟡 VUS</h3>
      <p className="text-xl">Variante de Significado Incerto</p>
      <p className="text-lg mt-4">Confiança: 50%</p>
      <p className="text-lg">Score: 2 pontos</p>
    </div>
  );
}
