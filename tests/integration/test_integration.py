"""test_integration.py - Testes de Integração"""
import pytest
import sys
from pathlib import Path
import csv
import tempfile
import os
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.variants.acmg_analyzer import process_csv
from src.utils import get_logger
logger = get_logger("TEST_INTEGRATION")
class TestProcessCSV:
    def test_process_csv_creates_output_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=['clinvar_id', 'gene', 'hgvs', 'classificacao', 'tipo', 'allele_frequency'])
            writer.writeheader()
            writer.writerow({'clinvar_id': 'VCV000000001', 'gene': 'MLH1', 'hgvs': 'MLH1:c.676delA', 'classificacao': 'Pathogenic', 'tipo': 'frameshift', 'allele_frequency': '0.00001'})
            input_file = f.name
        output_file = input_file.replace('.csv', '_output.csv')
        try:
            result = process_csv(input_file, output_file)
            assert result > 0, f"process_csv retornou {result}"
            assert os.path.exists(output_file), f"Arquivo não criado"
            with open(output_file, 'r') as f:
                lines = f.readlines()
                assert len(lines) > 1, "Arquivo vazio"
        finally:
            for file in [input_file, output_file]:
                if os.path.exists(file):
                    os.remove(file)
