"""test_main_advanced.py - Testes do bloco __main__ (pragmático)"""
import pytest
import sys
from pathlib import Path
import tempfile
import csv
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.variants.acmg_analyzer import process_csv
from src.utils import FileProcessingError


class TestMainBlockPragmatic:
    """Testes pragmáticos do bloco __main__"""
    
    def test_main_success_real_file(self):
        """Testa fluxo real de sucesso do __main__ (linhas 196-203)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "clinvar_mmr_variants.csv")
            output_file = os.path.join(tmpdir, "clinvar_mmr_with_acmg_v0.5.0.csv")
            
            # Criar arquivo de entrada válido
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
                writer.writerow({
                    'clinvar_id': 'VCV000000002',
                    'gene': 'MSH2',
                    'hgvs': 'MSH2:c.500G>A',
                    'tipo': 'missense',
                    'classificacao': 'Benign',
                    'allele_frequency': '0.3'
                })
            
            total = process_csv(input_file, output_file)
            assert total >= 2
            assert os.path.exists(output_file)
    
    def test_main_multiple_variants_processing(self):
        """Testa processamento de múltiplas variantes"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "variants.csv")
            output_file = os.path.join(tmpdir, "output.csv")
            
            with open(input_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['clinvar_id', 'gene', 'hgvs', 'tipo', 'classificacao', 'allele_frequency'])
                writer.writeheader()
                
                writer.writerow({
                    'clinvar_id': 'VCV000000001',
                    'gene': 'MLH1',
                    'hgvs': 'MLH1:c.100delA',
                    'tipo': 'frameshift',
                    'classificacao': 'Pathogenic',
                    'allele_frequency': '0.00001'
                })
                
                writer.writerow({
                    'clinvar_id': 'VCV000000002',
                    'gene': 'MSH2',
                    'hgvs': 'MSH2:c.200G>A',
                    'tipo': 'missense',
                    'classificacao': 'Benign',
                    'allele_frequency': '0.4'
                })
                
                writer.writerow({
                    'clinvar_id': 'VCV000000003',
                    'gene': 'PMS2',
                    'hgvs': 'PMS2:c.300C>T',
                    'tipo': 'stop_gained',
                    'classificacao': 'Pathogenic',
                    'allele_frequency': '0.00001'
                })
            
            total = process_csv(input_file, output_file)
            assert total == 3
            assert os.path.exists(output_file)
