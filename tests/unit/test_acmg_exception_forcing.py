"""test_acmg_exception_forcing.py - Força exceções para cobrir linhas não testáveis"""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.variants.acmg_analyzer import ACMGClassifier, process_csv
from src.variants.models import VariantInput
from src.utils import ACMGClassificationError, FileProcessingError


class TestACMGClassifierExceptions:
    """Força exceções em ACMGClassifier.classify() (linhas 113-115)"""
    
    @patch('src.variants.acmg_analyzer.ACMGCriteria.check_pvs1')
    def test_classify_forces_exception_in_classify(self, mock_check_pvs1):
        """Força exceção em classify() para cobrir linhas 113-115"""
        # Mock lança exceção ao ser chamado
        mock_check_pvs1.side_effect = Exception("Erro simulado na classificação")
        
        classifier = ACMGClassifier()
        variant = VariantInput(
            clinvar_id="VCV000000001",
            gene="MLH1",
            hgvs="MLH1:c.100delA",
            tipo="frameshift",
            classificacao="Pathogenic",
            allele_frequency=0.000001
        )
        
        # Deve lançar ACMGClassificationError
        with pytest.raises(ACMGClassificationError):
            classifier.classify(variant)


class TestProcessCSVExceptions:
    """Força exceções em process_csv() (linhas 186-188)"""
    
    @patch('builtins.open', side_effect=Exception("Erro ao ler arquivo"))
    def test_process_csv_forces_generic_exception(self, mock_open):
        """Força exceção genérica em process_csv() para cobrir linhas 186-188"""
        with pytest.raises(FileProcessingError):
            process_csv("data/test.csv", "output.csv")

    @patch('src.variants.acmg_analyzer.ACMGClassifier.classify')
    def test_process_csv_forces_acmg_classification_error(self, mock_classify):
        """Força ACMGClassificationError em process_csv (linhas 171-173)"""
        import tempfile
        import csv
        import os
        
        mock_classify.side_effect = ACMGClassificationError("Erro de classificação simulado")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.csv")
            output_file = os.path.join(tmpdir, "output.csv")
            
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
            
            # process_csv deve continuar e retornar contagem (não falhar)
            result = process_csv(input_file, output_file)
            assert result >= 0
