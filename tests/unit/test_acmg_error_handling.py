"""test_acmg_error_handling.py - Testes de tratamento de erros"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.variants.acmg_analyzer import ACMGClassifier
from src.variants.models import VariantInput
from pydantic import ValidationError


class TestValidationErrors:
    """Testa erros de validação Pydantic (linhas não cobertas)"""
    
    def test_invalid_gene_raises_validation_error(self):
        """Gene inválido deve lançar ValidationError"""
        with pytest.raises(ValidationError):
            VariantInput(
                clinvar_id="VCV000000001",
                gene="INVALID_GENE",  # Não é MLH1/MSH2/MSH6/PMS2/EPCAM
                hgvs="c.100delA",
                tipo="deletion",
                classificacao="Pathogenic",
                allele_frequency=0.000001
            )
    
    def test_negative_allele_frequency_raises_validation_error(self):
        """Frequência alélica negativa deve lançar ValidationError"""
        with pytest.raises(ValidationError):
            VariantInput(
                clinvar_id="VCV000000002",
                gene="MLH1",
                hgvs="MLH1:c.100delA",
                tipo="deletion",
                classificacao="Pathogenic",
                allele_frequency=-0.5  # Negativo = inválido
            )
    
    def test_empty_clinvar_id_raises_validation_error(self):
        """ClinVar ID vazio deve lançar ValidationError"""
        with pytest.raises(ValidationError):
            VariantInput(
                clinvar_id="",  # Vazio
                gene="MLH1",
                hgvs="MLH1:c.100delA",
                tipo="deletion",
                classificacao="Pathogenic",
                allele_frequency=0.000001
            )


class TestClassifyEdgeCases:
    """Testa casos extremos em ACMGClassifier.classify()"""
    
    def test_classify_variant_with_zero_frequency(self):
        """Classifica variante com frequência zero (rara)"""
        classifier = ACMGClassifier()
        variant = VariantInput(
            clinvar_id="VCV000000003",
            gene="MLH1",
            hgvs="MLH1:c.100delA",
            tipo="frameshift",
            classificacao="Pathogenic",
            allele_frequency=0.0  # Frequência zero
        )
        result = classifier.classify(variant)
        assert result in ["Pathogenic", "Likely Pathogenic", "VUS", "Likely Benign", "Benign"]
    
    def test_classify_variant_with_very_high_frequency(self):
        """Classifica variante muito frequente (benigna)"""
        classifier = ACMGClassifier()
        variant = VariantInput(
            clinvar_id="VCV000000004",
            gene="MSH2",
            hgvs="MSH2:c.200G>A",
            tipo="missense",
            classificacao="Benign",
            allele_frequency=0.45  # Muito frequente
        )
        result = classifier.classify(variant)
        assert result == "Benign"  # BA1 triggers
    
    def test_classify_stop_gained_mlh1(self):
        """Classifica variante stop_gained em MLH1 (PVS1)"""
        classifier = ACMGClassifier()
        variant = VariantInput(
            clinvar_id="VCV000000005",
            gene="MLH1",
            hgvs="MLH1:c.500C>T",
            tipo="stop_gained",
            classificacao="Pathogenic",
            allele_frequency=0.000001
        )
        result = classifier.classify(variant)
        assert result == "Pathogenic"  # PVS1 triggers
