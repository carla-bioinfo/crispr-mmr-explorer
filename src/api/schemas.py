"""
Modelos Pydantic para validação de entrada/saída
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal

# ============ VARIANT CLASSIFICATION ============

class VariantInput(BaseModel):
    """Modelo para receber variante do usuário"""
    chromosome: str = Field(..., description="Cromossomo (1-22, X, Y, MT)")
    position: int = Field(..., description="Posição genômica")
    ref: str = Field(..., description="Alelo referência")
    alt: str = Field(..., description="Alelo alternativo")
    gene: Literal['MLH1', 'MSH2', 'MSH6', 'PMS2', 'EPCAM'] = Field(
        ..., 
        description="Gene MMR (um dos 5 principais)"
    )
    
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
    pathogenicity_class: str
    acmg_criteria: List[str]
    evidence_summary: str
    confidence_score: float

class ClassificationResponse(BaseModel):
    """Resposta da API de classificação"""
    status: str
    data: ACMGClassification
    message: str
