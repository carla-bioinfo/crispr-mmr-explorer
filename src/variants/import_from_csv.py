"""
Script para importar variantes do CSV para o SQLite
Descrição: Lê clinvar_mmr_with_acmg.csv e insere no banco de dados
"""

import csv
from database import VariantDatabase

def import_variants_from_csv(csv_path: str, db_path: str = "data/processed/variants.db"):
    """
    Importa variantes de um arquivo CSV para o SQLite.
    
    Args:
        csv_path: Caminho do arquivo CSV
        db_path: Caminho do banco SQLite
    """
    
    # Inicializa o banco de dados
    db = VariantDatabase(db_path)
    
    # Cria a tabela
    db.create_variants_table()
    
    # Lê o CSV
    print(f"\n📖 Lendo dados de: {csv_path}")
    
    variants_inserted = 0
    variants_error = 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                # Converte pontos para inteiro
                row['pontos'] = int(row['pontos'])
                
                # Insere no banco
                db.insert_variant(row)
                variants_inserted += 1
                print(f"  ✓ {row['clinvar_id']} ({row['gene']}) - {row['acmg_classification']}")
                
            except Exception as e:
                variants_error += 1
                print(f"  ✗ Erro: {e}")
    
    # Validação
    print(f"\n" + "="*60)
    print(f"📊 RESUMO DA IMPORTAÇÃO")
    print(f"="*60)
    print(f"Variantes inseridas: {variants_inserted}")
    print(f"Erros: {variants_error}")
    print(f"Total no banco: {db.count_variants()}")
    print(f"="*60 + "\n")
    
    # Fecha a conexão
    db.close()

if __name__ == "__main__":
    import_variants_from_csv("data/processed/clinvar_mmr_with_acmg.csv")
