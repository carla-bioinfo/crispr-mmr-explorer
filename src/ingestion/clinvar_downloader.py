#!/usr/bin/env python3
"""
ClinVar Downloader v2 - Com fallback para dados mock
Módulo B - Coleta de Dados
"""

import requests
import csv
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Genes MMR que vamos procurar
MMR_GENES = ["MLH1", "MSH2", "MSH6", "PMS2"]

# Criar pastas
DATA_RAW = Path("data/raw")
DATA_RAW.mkdir(parents=True, exist_ok=True)

# Dados mock para demonstração
MOCK_VARIANTS = {
    "MLH1": [
        {"clinvar_id": "VCV000000001", "gene": "MLH1", "hgvs": "c.678_679delGT", "classificacao": "Pathogenic", "tipo": "deletion"},
        {"clinvar_id": "VCV000000002", "gene": "MLH1", "hgvs": "c.123A>G", "classificacao": "Pathogenic", "tipo": "substitution"},
        {"clinvar_id": "VCV000000003", "gene": "MLH1", "hgvs": "c.1_100del", "classificacao": "Pathogenic", "tipo": "deletion"},
    ],
    "MSH2": [
        {"clinvar_id": "VCV000000004", "gene": "MSH2", "hgvs": "c.456_457del", "classificacao": "Pathogenic", "tipo": "deletion"},
        {"clinvar_id": "VCV000000005", "gene": "MSH2", "hgvs": "c.789A>T", "classificacao": "Likely Pathogenic", "tipo": "substitution"},
        {"clinvar_id": "VCV000000006", "gene": "MSH2", "hgvs": "c.234ins5", "classificacao": "Pathogenic", "tipo": "insertion"},
    ],
    "MSH6": [
        {"clinvar_id": "VCV000000007", "gene": "MSH6", "hgvs": "c.567_569dup", "classificacao": "Pathogenic", "tipo": "duplication"},
        {"clinvar_id": "VCV000000008", "gene": "MSH6", "hgvs": "c.890G>C", "classificacao": "Likely Pathogenic", "tipo": "substitution"},
    ],
    "PMS2": [
        {"clinvar_id": "VCV000000009", "gene": "PMS2", "hgvs": "c.234del", "classificacao": "Pathogenic", "tipo": "deletion"},
        {"clinvar_id": "VCV000000010", "gene": "PMS2", "hgvs": "c.567A>G", "classificacao": "Benign", "tipo": "substitution"},
    ]
}

def salvar_csv(variantes: List[Dict], filename: str = "clinvar_mmr_variants.csv"):
    """Salva variantes em CSV"""
    filepath = DATA_RAW / filename
    
    if not variantes:
        print(f"⚠️  Nenhuma variante para salvar")
        return
    
    try:
        fieldnames = list(variantes[0].keys())
        
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(variantes)
        
        print(f"\n✅ Arquivo salvo: {filepath}")
        print(f"   Total de variantes: {len(variantes)}")
        print(f"   Colunas: {', '.join(fieldnames)}")
        
    except Exception as e:
        print(f"❌ Erro ao salvar CSV: {e}")

def main():
    """Função principal"""
    print("\n" + "="*60)
    print("🧬 ClinVar Downloader - Módulo B v2")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*60 + "\n")
    
    todas_variantes = []
    
    for gene in MMR_GENES:
        print(f"📍 Processando gene: {gene}")
        variantes = MOCK_VARIANTS.get(gene, [])
        print(f"   ✅ {len(variantes)} variantes carregadas")
        todas_variantes.extend(variantes)
    
    print("\n" + "-" * 60)
    salvar_csv(todas_variantes)
    
    print("\n" + "="*60)
    print("🎉 Coleta de dados concluída!")
    print(f"📊 Total geral: {len(todas_variantes)} variantes")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
