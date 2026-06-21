"""
Modelos Pydantic para validação de variantes
Define esquema de dados e validações
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Literal
from datetime import datetime


class VariantInput(BaseModel):
    """
    Modelo para validar entrada de variante
    Garante que dados estão corretos ANTES de processar
    """
    
    # Campo: clinvar_id
    clinvar_id: str = Field(
        ..., 
        min_length=1,
        description="ID único de ClinVar (ex: RCV000000001 ou VCV000000001)"
    )
    
    # Campo: gene
    gene: Literal['MLH1', 'MSH2', 'MSH6', 'PMS2', 'EPCAM'] = Field(
        ...,
        description="Gene MMR (um dos 5 principais)"
    )
    
    # Campo: hgvs
    hgvs: str = Field(
        ...,
        min_length=3,
        description="Notação HGVS (ex: c.678_679delGT)"
    )
    
    # Campo: classificacao
    classificacao: str = Field(
        ...,
        min_length=1,
        description="Classificação original (Pathogenic, Benign, etc)"
    )
    
    # Campo: tipo
    tipo: Literal[
        'deletion', 
        'insertion', 
        'duplication',
        'substitution',
        'frameshift',
        'stop_gained',
        'splice_site',
        'missense',
        'inframe_deletion'
    ] = Field(
        ...,
        description="Tipo de variante"
    )
    
    # Campo opcional: allele_frequency
    allele_frequency: Optional[float] = Field(
        None,
        ge=0,
        le=1.0,
        description="Frequência alélica (0-1)"
    )
    
    # Validadores customizados
    @field_validator('clinvar_id')
    def validate_clinvar_id(cls, v):
        """Valida formato de ClinVar ID"""
        if not (v.startswith('RCV') or v.startswith('VCV')):
            raise ValueError(f"ClinVar ID deve começar com RCV ou VCV, recebeu: {v}")
        return v
    
    @field_validator('hgvs')
    def validate_hgvs(cls, v):
        """Valida formato HGVS básico"""
        if ':' not in v and '.' not in v:
            raise ValueError(f"HGVS inválido: {v}. Exemplo: MLH1:c.678_679delGT")
        return v
    
    @field_validator('allele_frequency')
    def validate_allele_frequency(cls, v):
        """Valida frequência alélica"""
        if v is not None and (v < 0 or v > 1):
            raise ValueError(f"Frequência deve estar entre 0 e 1, recebeu: {v}")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "clinvar_id": "VCV000000001",
                "gene": "MLH1",
                "hgvs": "MLH1:c.678_679delGT",
                "classificacao": "Pathogenic",
                "tipo": "deletion",
                "allele_frequency": 0.00001
            }
        }
    )


class VariantInDB(VariantInput):
    """Variante com campos de banco de dados"""
    
    id: Optional[int] = None
    acmg_classification: Optional[str] = None
    acmg_criteria: Optional[str] = None
    acmg_explanation: Optional[str] = None
    created_at: Optional[datetime] = None


class VariantResponse(BaseModel):
    """Response model para API"""
    
    clinvar_id: str
    gene: str
    hgvs: str
    acmg_classification: str
    acmg_criteria: Optional[str]
    acmg_explanation: Optional[str]
