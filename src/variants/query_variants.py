"""
Script para fazer consultas (queries) no banco SQLite
Demonstra como extrair informações úteis do banco
"""

from database import VariantDatabase

def print_separator(title=""):
    """Printa uma linha decorada."""
    print("\n" + "="*70)
    if title:
        print(f"  {title}")
    print("="*70 + "\n")

def query_all_variants():
    """Mostra todas as variantes."""
    db = VariantDatabase()
    
    print_separator("📋 TODAS AS VARIANTES")
    
    sql = "SELECT clinvar_id, gene, hgvs, acmg_classification, pontos FROM variants"
    db.cursor.execute(sql)
    results = db.cursor.fetchall()
    
    for row in results:
        print(f"  {row[0]} | {row[1]:6} | {row[2]:20} | {row[3]:20} | Pts: {row[4]}")
    
    db.close()

def query_by_gene(gene_name: str):
    """Mostra variantes de um gene específico."""
    db = VariantDatabase()
    
    print_separator(f"🧬 VARIANTES DO GENE: {gene_name}")
    
    sql = "SELECT clinvar_id, hgvs, acmg_classification FROM variants WHERE gene = ?"
    db.cursor.execute(sql, (gene_name,))
    results = db.cursor.fetchall()
    
    if results:
        print(f"  Total: {len(results)} variante(s)\n")
        for row in results:
            print(f"    • {row[0]}: {row[1]} → {row[2]}")
    else:
        print(f"  Nenhuma variante encontrada para {gene_name}")
    
    db.close()

def query_pathogenic():
    """Mostra apenas variantes patogênicas."""
    db = VariantDatabase()
    
    print_separator("⚠️ VARIANTES PATOGÊNICAS")
    
    sql = "SELECT COUNT(*) FROM variants WHERE acmg_classification LIKE '%Pathogenic%'"
    db.cursor.execute(sql)
    count = db.cursor.fetchone()[0]
    
    print(f"  Total de variantes patogênicas: {count}\n")
    
    sql = "SELECT clinvar_id, gene, hgvs FROM variants WHERE acmg_classification LIKE '%Pathogenic%'"
    db.cursor.execute(sql)
    results = db.cursor.fetchall()
    
    for row in results:
        print(f"    • {row[0]} ({row[1]}): {row[2]}")
    
    db.close()

def query_statistics():
    """Mostra estatísticas dos dados."""
    db = VariantDatabase()
    
    print_separator("📊 ESTATÍSTICAS GERAIS")
    
    # Total
    sql = "SELECT COUNT(*) FROM variants"
    db.cursor.execute(sql)
    total = db.cursor.fetchone()[0]
    print(f"  Total de variantes: {total}")
    
    # Por gene
    print(f"\n  Distribuição por Gene:")
    sql = "SELECT gene, COUNT(*) as count FROM variants GROUP BY gene ORDER BY count DESC"
    db.cursor.execute(sql)
    results = db.cursor.fetchall()
    for row in results:
        print(f"    • {row[0]}: {row[1]} variante(s)")
    
    # Por classificação ACMG
    print(f"\n  Distribuição por Classificação ACMG:")
    sql = "SELECT acmg_classification, COUNT(*) as count FROM variants GROUP BY acmg_classification"
    db.cursor.execute(sql)
    results = db.cursor.fetchall()
    for row in results:
        print(f"    • {row[0]}: {row[1]} variante(s)")
    
    # Pontos médios
    print(f"\n  Análise de Pontos:")
    sql = "SELECT AVG(pontos), MIN(pontos), MAX(pontos) FROM variants"
    db.cursor.execute(sql)
    avg, min_pts, max_pts = db.cursor.fetchone()
    print(f"    • Média: {avg:.2f}")
    print(f"    • Mínimo: {min_pts}")
    print(f"    • Máximo: {max_pts}")
    
    db.close()

if __name__ == "__main__":
    # Executa todas as queries
    query_all_variants()
    query_by_gene("MLH1")
    query_by_gene("MSH2")
    query_by_gene("MSH6")
    query_by_gene("PMS2")
    query_pathogenic()
    query_statistics()
    
    print_separator("✅ Consultas Finalizadas")
