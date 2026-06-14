#!/usr/bin/env python3
"""
ACMG Classifier v0.4.0 - ACMG/AMP 2015 (Adaptado para dados reais)
"""

import csv
from pathlib import Path
from typing import Dict, List


class ACMGCriteria:
    """Critérios ACMG/AMP 2015 para genes MMR"""
    
    # Genes MMR onde Loss of Function é patogênico
    PVS1_GENES = {
        'MLH1': ['deletion', 'insertion', 'stop_gained', 'splice_site', 'frameshift'],
        'MSH2': ['deletion', 'insertion', 'stop_gained', 'splice_site', 'frameshift'],
        'MSH6': ['deletion', 'insertion', 'stop_gained', 'splice_site', 'frameshift'],
        'PMS2': ['deletion', 'insertion', 'stop_gained', 'splice_site', 'frameshift'],
        'EPCAM': ['deletion', 'insertion', 'stop_gained', 'splice_site', 'frameshift']
    }
    
    @staticmethod
    def check_pvs1(tipo: str, gene: str) -> bool:
        """PVS1: Null variant em gene MMR (frameshift, stop, splice)"""
        if gene not in ACMGCriteria.PVS1_GENES:
            return False
        return tipo in ACMGCriteria.PVS1_GENES[gene]
    
    @staticmethod
    def check_ps1(classificacao_original: str) -> bool:
        """PS1: Mesma mudança já reportada como Pathogenic"""
        return 'Pathogenic' in classificacao_original and 'Likely' not in classificacao_original
    
    @staticmethod
    def check_pm2(allele_frequency) -> bool:
        """PM2: Frequência alélica muito baixa"""
        if not allele_frequency:
            return False
        try:
            freq = float(allele_frequency)
            return freq < 0.00001
        except:
            return False
    
    @staticmethod
    def check_ba1(allele_frequency) -> bool:
        """BA1: Frequência alélica alta (>5%)"""
        if not allele_frequency:
            return False
        try:
            freq = float(allele_frequency)
            return freq > 0.05
        except:
            return False


class ACMGClassifier:
    """Classifica variantes com ACMG/AMP 2015"""
    
    @staticmethod
    def classificar(variante: Dict) -> Dict:
        """Classifica uma variante"""
        
        gene = variante.get('gene', '')
        tipo = variante.get('tipo', '')
        classificacao_original = variante.get('classificacao', '')
        allele_frequency = variante.get('allele_frequency', 0)
        
        pathogenic_criteria = []
        benign_criteria = []
        
        # Verificar critérios
        if ACMGCriteria.check_pvs1(tipo, gene):
            pathogenic_criteria.append('PVS1')
        
        if ACMGCriteria.check_ps1(classificacao_original):
            pathogenic_criteria.append('PS1')
        
        if ACMGCriteria.check_pm2(allele_frequency):
            pathogenic_criteria.append('PM2')
        
        if ACMGCriteria.check_ba1(allele_frequency):
            benign_criteria.append('BA1')
        
        # Aplicar regras ACMG
        if 'PVS1' in pathogenic_criteria:
            classification = 'Pathogenic (P)'
            strength = 'Very Strong (PVS1)'
        elif 'PS1' in pathogenic_criteria:
            classification = 'Likely Pathogenic (LP)'
            strength = 'Strong (PS1)'
        elif 'PM2' in pathogenic_criteria:
            classification = 'Likely Pathogenic (LP)'
            strength = 'Moderate (PM2)'
        elif 'BA1' in benign_criteria:
            classification = 'Benign (B)'
            strength = 'Very Strong (BA1)'
        else:
            classification = 'Variant of Uncertain Significance (VUS)'
            strength = 'Insufficient Evidence'
        
        all_criteria = pathogenic_criteria + benign_criteria
        criteria_str = ','.join(all_criteria) if all_criteria else 'None'
        
        variante['acmg_classification'] = classification
        variante['acmg_criteria'] = criteria_str
        variante['acmg_explanation'] = f"{classification} - {strength}"
        
        return variante


def processar_arquivo(input_file: str, output_file: str) -> List[Dict]:
    """Processa arquivo"""
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    print(f"\n📖 Lendo: {input_path}")
    
    variantes = []
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            variantes.append(row)
    
    print(f"✅ {len(variantes)} variantes lidas")
    print(f"\n🔍 Aplicando ACMG/AMP 2015 v0.4.0...")
    
    classifier = ACMGClassifier()
    variantes_analisadas = []
    
    for var in variantes:
        var_analisada = classifier.classificar(var)
        variantes_analisadas.append(var_analisada)
        print(f"  ✓ {var['gene']}: {var['hgvs']} [{var['tipo']}] → {var_analisada['acmg_classification']}")
    
    print(f"\n💾 Salvando: {output_path}")
    if variantes_analisadas:
        fieldnames = list(variantes_analisadas[0].keys())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(variantes_analisadas)
        
        print(f"✅ Arquivo salvo!")
    
    return variantes_analisadas


def main():
    print("\n" + "="*70)
    print("🧬 ACMG Classifier v0.4.0 - ACMG/AMP 2015 (Adaptado)")
    print("="*70)
    
    input_file = "data/raw/clinvar_mmr_variants.csv"
    output_file = "data/processed/clinvar_mmr_with_acmg_v0.4.0.csv"
    
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    
    variantes = processar_arquivo(input_file, output_file)
    
    print("\n" + "="*70)
    print("📊 RESUMO v0.4.0")
    print("="*70)
    
    pathogenic = sum(1 for v in variantes if v['acmg_classification'] == 'Pathogenic (P)')
    likely_pathogenic = sum(1 for v in variantes if v['acmg_classification'] == 'Likely Pathogenic (LP)')
    vus = sum(1 for v in variantes if 'VUS' in v['acmg_classification'])
    benign = sum(1 for v in variantes if v['acmg_classification'] == 'Benign (B)')
    
    print(f"\n🔴 Pathogenic (P): {pathogenic}")
    print(f"🟠 Likely Pathogenic (LP): {likely_pathogenic}")
    print(f"🟡 VUS: {vus}")
    print(f"🟢 Benign (B): {benign}")
    print(f"📍 Total: {len(variantes)} variantes")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
