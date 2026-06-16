"""test_acmg_process_csv.py - Testes da funcao process_csv"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.variants.acmg_analyzer import process_csv
from src.utils import FileProcessingError

class TestProcessCSV:
    def test_process_csv_file_not_found(self):
        """FileNotFoundError quando arquivo nao existe"""
        with pytest.raises(FileProcessingError):
            process_csv("data/nonexistent.csv", "output.csv")
    
    def test_process_csv_creates_output(self):
        """Verifica se output file eh criado"""
        import tempfile
        import csv
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.csv")
            output_file = os.path.join(tmpdir, "output.csv")
            
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
            
            result = process_csv(input_file, output_file)
            assert result >= 0
            assert os.path.exists(output_file)

    def test_process_csv_validation_error(self):
        """Verifica ValidationError com dados invalidos"""
        import tempfile
        import csv
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.csv")
            output_file = os.path.join(tmpdir, "output.csv")
            
            with open(input_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['clinvar_id', 'gene', 'hgvs', 'tipo', 'classificacao', 'allele_frequency'])
                writer.writeheader()
                writer.writerow({
                    'clinvar_id': 'INVALID_ID',
                    'gene': 'MLH1',
                    'hgvs': 'invalid',
                    'tipo': 'deletion',
                    'classificacao': 'Pathogenic',
                    'allele_frequency': '0.000001'
                })
            
            result = process_csv(input_file, output_file)
            assert result == 0
