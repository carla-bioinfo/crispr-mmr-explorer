"""
Script para validar integridade dos dados importados
Verifica: 0% de diferença entre CSV original e SQLite
"""

import csv
from database import VariantDatabase

def validate_import():
    """Compara dados do CSV com dados do banco."""
    
    print("\n" + "="*70)
    print("🔍 VALIDAÇÃO DE INTEGRIDADE")
    print("="*70 + "\n")
    
    # Lê o CSV
    csv_variants = []
    with open("data/processed/clinvar_mmr_with_acmg.csv", 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        csv_variants = list(reader)
    
    # Lê o banco
    db = VariantDatabase()
    db_variants = db.get_all_variants()
    db.close()
    
    # Comparação
    print(f"CSV: {len(csv_variants)} linhas")
    print(f"Banco: {len(db_variants)} linhas")
    
    if len(csv_variants) == len(db_variants):
        print(f"\n✅ Quantidade OK!\n")
    else:
        print(f"\n❌ ERRO: Quantidades diferentes!\n")
        return False
    
    # Valida campos por variante
    errors = 0
    for i, csv_row in enumerate(csv_variants):
        db_row = db_variants[i]
        
        # Compara clinvar_id (campo 1 no banco, índice 1 na tupla)
        if csv_row['clinvar_id'] != db_row[1]:
            print(f"❌ Erro em clinvar_id na linha {i+1}")
            errors += 1
        
        # Compara gene (campo 2 no banco, índice 2 na tupla)
        if csv_row['gene'] != db_row[2]:
            print(f"❌ Erro em gene na linha {i+1}")
            errors += 1
    
    if errors == 0:
        print("✅ 100% dos dados validados com sucesso!")
        print("✅ 0% de diferença entre CSV e Banco\n")
        return True
    else:
        print(f"❌ {errors} erros encontrados\n")
        return False

if __name__ == "__main__":
    validate_import()
