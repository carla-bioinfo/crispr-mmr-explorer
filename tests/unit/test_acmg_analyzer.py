"""test_acmg_analyzer.py - Testes da lógica ACMG"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.variants.acmg_analyzer import ACMGClassifier
from src.utils import get_logger
logger = get_logger("TEST_ACMG")
class TestACMGClassifier:
    def setup_method(self):
        self.classifier = ACMGClassifier()
    def test_pathogenic_variant(self, sample_variant_pathogenic):
        logger.info(f"Testando variante patogênica: {sample_variant_pathogenic.hgvs}")
        result = self.classifier.classify(sample_variant_pathogenic)
        assert result == "Pathogenic", f"Esperado Pathogenic, recebeu {result}"
        logger.info(f"✅ Teste passou! Classificação: {result}")
    def test_benign_variant(self, sample_variant_benign):
        logger.info(f"Testando variante benigna: {sample_variant_benign.hgvs}")
        result = self.classifier.classify(sample_variant_benign)
        assert result == "Benign", f"Esperado Benign, recebeu {result}"
        logger.info(f"✅ Teste passou! Classificação: {result}")
    def test_vus_variant(self, sample_variant_vus):
        logger.info(f"Testando variante VUS: {sample_variant_vus.hgvs}")
        result = self.classifier.classify(sample_variant_vus)
        assert result == "VUS", f"Esperado VUS, recebeu {result}"
        logger.info(f"✅ Teste passou! Classificação: {result}")
class TestACMGValidation:
    def test_gene_validation(self, sample_variant_pathogenic):
        logger.info(f"Validando gene: {sample_variant_pathogenic.gene}")
        valid_genes = ["MLH1", "MSH2", "MSH6", "PMS2", "EPCAM"]
        assert sample_variant_pathogenic.gene in valid_genes, f"Gene inválido"
        logger.info(f"✅ Gene válido: {sample_variant_pathogenic.gene}")
class TestACMGClassifierInstantiation:
    def test_classifier_can_be_instantiated(self):
        classifier = ACMGClassifier()
        assert classifier is not None
        logger.info("✅ ACMGClassifier instanciado!")
