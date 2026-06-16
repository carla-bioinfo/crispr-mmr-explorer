"""conftest.py - Configuração Compartilhada de Testes"""
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import get_logger
from src.variants.models import VariantInput
@pytest.fixture
def logger():
    return get_logger("TEST_CRISPR")
@pytest.fixture
def sample_variant_pathogenic():
    return VariantInput(
        clinvar_id="VCV000000001",
        gene="MLH1",
        hgvs="MLH1:c.676delA",
        classificacao="Pathogenic",
        tipo="frameshift",
        allele_frequency=0.00001
    )
@pytest.fixture
def sample_variant_benign():
    return VariantInput(
        clinvar_id="VCV000000002",
        gene="MSH2",
        hgvs="MSH2:c.1A>G",
        classificacao="Benign",
        tipo="substitution",
        allele_frequency=0.45
    )
@pytest.fixture
def sample_variant_vus():
    return VariantInput(
        clinvar_id="VCV000000003",
        gene="MSH6",
        hgvs="MSH6:c.100G>A",
        classificacao="VUS",
        tipo="missense",
        allele_frequency=0.01
    )

@pytest.fixture
def sample_variant_invalid_frequency():
    """Variante com allele_frequency=None"""
    return VariantInput(
        clinvar_id="VCV000000004",
        gene="MLH1",
        hgvs="MLH1:c.100A>G",
        classificacao="VUS",
        tipo="missense",
        allele_frequency=None
    )

@pytest.fixture
def sample_variant_high_frequency():
    """Variante com frequência alta (BA1)"""
    return VariantInput(
        clinvar_id="VCV000000005",
        gene="PMS2",
        hgvs="PMS2:c.200G>A",
        classificacao="VUS",
        tipo="missense",
        allele_frequency=0.10
    )

@pytest.fixture
def sample_variant_pvs1_ps1():
    """Variante com PVS1 + PS1 → Pathogenic"""
    return VariantInput(
        clinvar_id="VCV000000006",
        gene="MSH2",
        hgvs="MSH2:c.500delA",
        classificacao="Pathogenic",
        tipo="deletion",
        allele_frequency=0.000001
    )
