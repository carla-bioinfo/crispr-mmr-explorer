"""
Rota de health check - verifica se API está online
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    """Verifica se a API está rodando"""
    return {
        "status": "healthy",
        "service": "CRISPR-MMR Explorer API",
        "version": "2.0.0",
    }
