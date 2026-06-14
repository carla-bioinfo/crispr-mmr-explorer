#!/usr/bin/env python3
"""
ACMG Classifier - Analisa variantes com critérios ACMG
Aplica aprendizado da Parte C
"""

import csv
from pathlib import Path
from typing import Dict, List

class ACMGClassifier:
    """Classifica variantes usando critérios ACMG"""
    
    # Mapeamento de classificações
    PATHOGENIC_KEYWORDS = ["Pathogenic", "pathogenic", "likely pathogenic"]
    BENIGN_KEYWORDS = ["Benign", "benign", "likely benign"]
    VUS_KEYWORDS = ["uncertain", "uncertain significance", "unknown"]
    
    @staticmethod
    def classificar(variante: Dict) -> Dict:
        """
        Classifica variante usando critérios ACMG
        Retorna variante com novo campo 'acmg_classification'
        """
        
        classificacao_original = variante.get('classificacao', '')
        tipo = variante.get('tipo', '')
        gene = variante.get('gene', '')
        
        # Critério 1: Tipo de variante
        pontos_patogenico = 0
        
        # Deleções/Frameshift = PVS1 (Muito Forte)
        if tipo in ['deletion', 'insertion']:
            pontos_patogenico += 3
            variante['criterio_pvs1'] = 'Sim (frameshift)'
        else:
            variante['criterio_pvs1'] = 'Não'
        
        # Critério 2: Classificação original (PS1 - já relatada)
        if 'Pathogenic' in classificacao_original:
            pontos_patogenico += 2
            variante['criterio_ps1'] = 'Sim (relatada como patogênica)'
        else:
            variante['criterio_ps1'] = 'Não'
        
        # Critério 3: Duplicação = possível problema
        if tipo == 'duplication':
            pontos_patogenico += 1
            variante['criterio_pm'] = 'Sim (duplicação)'
        else:
            variante['criterio_pm'] = 'Não'
        
        # Classificação final ACMG
        if pontos_patogenico >= 4:
            acmg = 'Pathogenic (P)'
        elif pontos_patogenico >= 3:
            acmg = 'Likely Pathogenic (LP)'
        elif pontos_patogenico == 2:
            acmg = 'Likely Pathogenic (LP)'
        elif pontos_patogenico == 1:
            acmg = 'Variant of Uncertain Significance (VUS)'
        else:
            acmg = 'Benign (B)'
        
        # Se original é Benign, respeita
        if 'Benign' in classificacao_original:
            acmg = 'Benign (B)'
            variante['criterio_ba1'] = 'Sim (frequente em população)'
        else:
            variante['criterio_ba1'] = 'Não'
        
        variante['acmg_classification'] = acmg
        variante['pontos'] = pontos_patogenico
        
        return variante


def processar_arquivo(input_file: str, output_file: str):
    """
    Lê CSV, analisa com ACMG, salva novo CSV
    """
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    print(f"\n📖 Lendo: {input_path}")
    
    # Ler CSV original
    variantes = []
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            variantes.append(row)
    
    print(f"✅ {len(variantes)} variantes lidas")
    
    # Aplicar ACMG
    print(f"\n🔍 Aplicando critérios ACMG...")
    classifier = ACMGClassifier()
    variantes_analisadas = []
    
    for var in variantes:
        var_analisada = classifier.classificar(var)
        variantes_analisadas.append(var_analisada)
        print(f"  ✓ {var['gene']}: {var['hgvs']} → {var_analisada['acmg_classification']}")
    
    # Salvar novo CSV
    print(f"\n💾 Salvando: {output_path}")
    if variantes_analisadas:
        fieldnames = list(variantes_analisadas[0].keys())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(variantes_analisadas)
        
        print(f"✅ Arquivo salvo com {len(variantes_analisadas)} variantes analisadas!")
        print(f"📊 Colunas: {len(fieldnames)}")
    
    return variantes_analisadas


def main():
    """Função principal"""
    print("\n" + "="*70)
    print("🧬 ACMG Classifier - Análise de Variantes Lynch")
    print("="*70)
    
    input_file = "data/raw/clinvar_mmr_variants.csv"
    output_file = "data/processed/clinvar_mmr_with_acmg.csv"
    
    # Criar pasta processed
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    
    # Processar
    variantes = processar_arquivo(input_file, output_file)
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO DA ANÁLISE")
    print("="*70)
    
    pathogenic = sum(1 for v in variantes if 'Pathogenic' in v['acmg_classification'])
    vus = sum(1 for v in variantes if 'VUS' in v['acmg_classification'])
    benign = sum(1 for v in variantes if 'Benign' in v['acmg_classification'])
    
    print(f"\n🔴 Patogênicas (P/LP): {pathogenic}")
    print(f"🟡 Incertas (VUS): {vus}")
    print(f"🟢 Benignas (B/LB): {benign}")
    print(f"\n📍 Total processado: {len(variantes)} variantes")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
