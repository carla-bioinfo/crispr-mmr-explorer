"""
Módulo de banco de dados SQLite para variantes MMR/Lynch
Autor: CRISPR-MMR Explorer
Descrição: Gerencia conexão, criação de tabelas e operações CRUD
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path

class VariantDatabase:
    """
    Classe para gerenciar o banco de dados SQLite de variantes.
    
    Atributos:
        db_path (str): Caminho do arquivo do banco de dados
        conn (sqlite3.Connection): Conexão com o banco
    """
    
    def __init__(self, db_path: str = "data/processed/variants.db"):
        """
        Inicializa a conexão com o banco de dados.
        
        Args:
            db_path: Caminho onde o arquivo .db será criado
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._ensure_db_directory()
        self._connect()
    
    def _ensure_db_directory(self):
        """Cria o diretório se não existir."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def _connect(self):
        """Conecta ao banco de dados."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"✅ Conectado ao banco: {self.db_path}")
    
    def create_variants_table(self):
        """Cria a tabela 'variants' com validações."""
        sql = """
        CREATE TABLE IF NOT EXISTS variants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clinvar_id TEXT UNIQUE NOT NULL,
            gene TEXT NOT NULL,
            hgvs TEXT NOT NULL,
            classificacao TEXT NOT NULL,
            tipo TEXT NOT NULL,
            criterio_pvs1 TEXT,
            criterio_ps1 TEXT,
            criterio_pm TEXT,
            criterio_ba1 TEXT,
            acmg_classification TEXT NOT NULL,
            pontos INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cursor.execute(sql)
        self.conn.commit()
        print("✅ Tabela 'variants' criada com sucesso!")
    
    def insert_variant(self, variant_dict: dict):
        """
        Insere uma variante no banco.
        
        Args:
            variant_dict: Dicionário com dados da variante
        """
        sql = """
        INSERT INTO variants 
        (clinvar_id, gene, hgvs, classificacao, tipo, 
         criterio_pvs1, criterio_ps1, criterio_pm, criterio_ba1, 
         acmg_classification, pontos)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            self.cursor.execute(sql, (
                variant_dict['clinvar_id'],
                variant_dict['gene'],
                variant_dict['hgvs'],
                variant_dict['classificacao'],
                variant_dict['tipo'],
                variant_dict['criterio_pvs1'],
                variant_dict['criterio_ps1'],
                variant_dict['criterio_pm'],
                variant_dict['criterio_ba1'],
                variant_dict['acmg_classification'],
                variant_dict['pontos']
            ))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"⚠️ Erro ao inserir variante {variant_dict['clinvar_id']}: {e}")
    
    def get_all_variants(self):
        """Retorna todas as variantes do banco."""
        sql = "SELECT * FROM variants"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def count_variants(self):
        """Retorna o número de variantes no banco."""
        sql = "SELECT COUNT(*) FROM variants"
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]
    
    def close(self):
        """Fecha a conexão com o banco."""
        if self.conn:
            self.conn.close()
            print("✅ Conexão fechada")

if __name__ == "__main__":
    # Teste básico
    db = VariantDatabase()
    db.create_variants_table()
    print(f"Total de variantes: {db.count_variants()}")
    db.close()
