"""
Modelos Pydantic para validação de entrada/saída
"""

from pydantic import BaseModel
from typing import Optional, List

# ============ VARIANT CLASSIFICATION ============

class VariantInput(BaseModel):
    """Modelo para receber variante do usuário"""
    chromosome: str
    position: int
    ref: str
    alt: str
    gene: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "chromosome": "3",
                "position": 36993722,
                "ref": "A",
                "alt": "G",
                "gene": "MLH1"
            }
        }

class ACMGClassification(BaseModel):
    """Modelo para retornar classificação ACMG/AMP"""
    variant_id: str
    gene: str
    pathogenicity_class: str  # Pathogenic, Likely Pathogenic, VUS, Likely Benign, Benign
    acmg_criteria: List[str]
    evidence_summary: str
    confidence_score: float

class ClassificationResponse(BaseModel):
    """Resposta da API de classificação"""
    status: str
    data: ACMGClassification
    message: str
