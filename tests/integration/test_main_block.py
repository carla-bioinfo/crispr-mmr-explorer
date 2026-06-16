"""test_main_block.py - Testa bloco __main__ (linhas 192-214)"""
import pytest
import sys
from pathlib import Path
import tempfile
import csv
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.variants.acmg_analyzer import process_csv
from src.utils import FileProcessingError


class TestMainBlock:
    """Testa simulação do bloco __main__ (linhas 192-214)"""
    
    def test_main_block_success_flow(self):
        """Simula fluxo bem-sucedido do __main__"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "clinvar_mmr_variants.csv")
            output_file = os.path.join(tmpdir, "clinvar_mmr_with_acmg_v0.5.0.csv")
            
            # Criar arquivo de entrada
            with open(input_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['clinvar_id', 'gene', 'hgvs', 'tipo', 'classificacao', 'allele_frequency'])
                writer.writeheader()
                writer.writerow({
                    'clinvar_id': 'VCV000000001',
                    'gene': 'MLH1',
                    'hgvs': 'MLH1:c.100delA',
                    'tipo': 'deletion',
                    'classificacao': 'Pathogenic',
                    'allele_frequency': '0.000001'
                })
            
            # Simular: total = process_csv(input_csv, output_csv)
            total = process_csv(input_file, output_file)
            assert total >= 0
            assert os.path.exists(output_file)
    
    def test_main_block_file_error(self):
        """Simula FileProcessingError do __main__"""
        with pytest.raises(FileProcessingError):
            process_csv("nonexistent_file.csv", "output.csv")
