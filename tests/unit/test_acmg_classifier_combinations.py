"""test_acmg_classifier_combinations.py"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.variants.acmg_analyzer import ACMGClassifier
from src.variants.models import VariantInput

class TestACMGClassifierCombinations:
    def setup_method(self):
        self.classifier = ACMGClassifier()
    
    def test_ba1_triggers_benign(self):
        v = VariantInput(clinvar_id="VCV000000101", gene="MLH1", hgvs="MLH1:c.1A>G", classificacao="VUS", tipo="missense", allele_frequency=0.10)
        assert self.classifier.classify(v) == "Benign"
    
    def test_pvs1_and_ps1_pathogenic(self):
        v = VariantInput(clinvar_id="VCV000000102", gene="MSH2", hgvs="MSH2:c.1delA", classificacao="Pathogenic", tipo="deletion", allele_frequency=0.000001)
        assert self.classifier.classify(v) == "Pathogenic"
    
    def test_pvs1_alone_likely_pathogenic(self):
        v = VariantInput(clinvar_id="VCV000000103", gene="MLH1", hgvs="MLH1:c.100delA", classificacao="VUS", tipo="deletion", allele_frequency=0.000001)
        assert self.classifier.classify(v) == "Likely Pathogenic"
    
    def test_ps1_and_pm2_likely_pathogenic(self):
        v = VariantInput(clinvar_id="VCV000000104", gene="PMS2", hgvs="PMS2:c.1A>G", classificacao="Pathogenic", tipo="missense", allele_frequency=0.000001)
        assert self.classifier.classify(v) == "Likely Pathogenic"
    
    def test_pm2_vus(self):
        v = VariantInput(clinvar_id="VCV000000105", gene="MSH6", hgvs="MSH6:c.1A>G", classificacao="VUS", tipo="missense", allele_frequency=0.000001)
        assert self.classifier.classify(v) == "VUS"
    
    def test_no_criteria_vus(self):
        v = VariantInput(clinvar_id="VCV000000106", gene="EPCAM", hgvs="EPCAM:c.1A>G", classificacao="VUS", tipo="missense", allele_frequency=0.01)
        assert self.classifier.classify(v) == "VUS"
