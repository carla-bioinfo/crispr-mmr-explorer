"""
Rota de classificação de variantes ACMG/AMP
"""

from fastapi import APIRouter, HTTPException
from src.api.schemas import VariantInput, ClassificationResponse, ACMGClassification

router = APIRouter()

@router.post("/classify")
def classify_variant(variant: VariantInput) -> ClassificationResponse:
    """
    Classifica uma variante usando ACMG/AMP 2015
    
    Body esperado:
    {
        "chromosome": "3",
        "position": 36993722,
        "ref": "A",
        "alt": "G",
        "gene": "MLH1"
    }
    """
    
    # Validação básica
    if not variant.gene:
        raise HTTPException(status_code=400, detail="Gene é obrigatório")
    
    # Simular classificação (mock data)
    # Em produção, isso chamaria ACMGClassifier
    classification = ACMGClassification(
        variant_id=f"{variant.chromosome}:{variant.position}:{variant.ref}:{variant.alt}",
        gene=variant.gene,
        pathogenicity_class="Likely Pathogenic",
        acmg_criteria=["PM2", "PP3", "PP5"],
        evidence_summary="Raro em população, predições in silico patogênicas, publicado em Lynch",
        confidence_score=0.85,
    )
    
    return ClassificationResponse(
        status="success",
        data=classification,
        message=f"Variante {variant.gene} classificada com sucesso",
    )
