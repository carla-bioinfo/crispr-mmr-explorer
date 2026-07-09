"""
Rota de classificação de variantes ACMG/AMP (v2.0.1 com ACMGClassifier real)
"""

from fastapi import APIRouter, HTTPException
from src.api.schemas import VariantInput, ClassificationResponse, ACMGClassification
from src.api.adapter import api_variant_to_acmg
from src.variants.acmg_analyzer import ACMGClassifier
from src.utils import get_logger

router = APIRouter()
logger = get_logger(__name__)

# Instanciar classifier uma vez (reutilizar em múltiplos requests)
classifier = ACMGClassifier()

@router.post("/classify")
def classify_variant(variant: VariantInput) -> ClassificationResponse:
    """
    Classifica uma variante usando ACMG/AMP 2015 (com ACMGClassifier real)
    
    Body esperado:
    {
        "chromosome": "3",
        "position": 36993722,
        "ref": "A",
        "alt": "G",
        "gene": "MLH1"
    }
    """
    
    try:
        # Validação básica
        if not variant.gene:
            raise HTTPException(status_code=400, detail="Gene é obrigatório")
        
        logger.info(f"Recebida variante: {variant.chromosome}:{variant.position} em {variant.gene}")
        
        # Converter dados da API para formato do ACMGClassifier
        acmg_variant = api_variant_to_acmg(variant)
        logger.debug(f"Adaptado para ACMGVariantInput: {acmg_variant.clinvar_id}")
        
        # Executar classificação real (com detalhes ACMG)
        pathogenicity_class, acmg_criteria, confidence_score = classifier.classify_with_details(acmg_variant.__dict__)
        logger.info(f"Classificação: {acmg_variant.clinvar_id} → {pathogenicity_class} (confiança: {confidence_score})")
        
        # Construir resposta estruturada
        classification = ACMGClassification(
            variant_id=acmg_variant.clinvar_id,
            gene=variant.gene,
            pathogenicity_class=pathogenicity_class,
            acmg_criteria=acmg_criteria,
            evidence_summary=f"Classificado por ACMGClassifier v0.5.0 usando regras ACMG/AMP 2015",
            confidence_score=confidence_score,
        )
        
        return ClassificationResponse(
            status="success",
            data=classification,
            message=f"Variante {variant.gene} classificada como {pathogenicity_class}",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao classificar variante: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
