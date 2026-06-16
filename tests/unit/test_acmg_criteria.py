"""test_acmg_criteria.py - Testes dos critérios ACMG individuais"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.variants.acmg_analyzer import ACMGCriteria

class TestACMGCriteriaPVS1:
    def test_pvs1_valid_frameshift(self):
        assert ACMGCriteria.check_pvs1("frameshift", "MLH1") == True
    
    def test_pvs1_invalid_gene(self):
        assert ACMGCriteria.check_pvs1("frameshift", "TP53") == False

class TestACMGCriteriaPS1:
    def test_ps1_pathogenic(self):
        assert ACMGCriteria.check_ps1("Pathogenic") == True
    
    def test_ps1_likely_pathogenic(self):
        assert ACMGCriteria.check_ps1("Likely Pathogenic") == False

class TestACMGCriteriaPM2:
    def test_pm2_very_low(self):
        assert ACMGCriteria.check_pm2(0.000001) == True
    
    def test_pm2_borderline(self):
        assert ACMGCriteria.check_pm2(0.00001) == False
    
    def test_pm2_none(self):
        assert ACMGCriteria.check_pm2(None) == False
    
    def test_pm2_invalid_string(self):
        assert ACMGCriteria.check_pm2("invalid") == False

class TestACMGCriteriaBA1:
    def test_ba1_high(self):
        assert ACMGCriteria.check_ba1(0.10) == True
    
    def test_ba1_low(self):
        assert ACMGCriteria.check_ba1(0.01) == False
    
    def test_ba1_none(self):
        assert ACMGCriteria.check_ba1(None) == False
    
    def test_ba1_invalid_string(self):
        assert ACMGCriteria.check_ba1("not_a_number") == False
