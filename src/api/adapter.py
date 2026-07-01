"""
Adapter: Converte dados API → Formato ACMGClassifier
"""

from src.api.schemas import VariantInput as APIVariantInput
from src.variants.models import VariantInput as ACMGVariantInput


def api_variant_to_acmg(api_variant: APIVariantInput) -> ACMGVariantInput:
    """
    Converte VariantInput da API para VariantInput do ACMGClassifier
    Gera valores que passam na validação Pydantic do ACMGVariantInput
    """
    
    clinvar_id = f"RCV{int(api_variant.position):09d}"
    hgvs = f"c.{api_variant.position}_{api_variant.position+1}del"
    
    if len(api_variant.ref) > len(api_variant.alt):
        tipo = "deletion"
    elif len(api_variant.alt) > len(api_variant.ref):
        tipo = "insertion"
    else:
        tipo = "substitution"
    
    classificacao = "Unknown"
    allele_frequency = None
    
    return ACMGVariantInput(
        clinvar_id=clinvar_id,
        gene=api_variant.gene,
        hgvs=hgvs,
        classificacao=classificacao,
        tipo=tipo,
        allele_frequency=allele_frequency,
    )
