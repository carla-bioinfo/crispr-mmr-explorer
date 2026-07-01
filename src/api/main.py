"""
FastAPI backend para CRISPR-MMR Explorer v2.0.0
Endpoints RESTful para classificação ACMG/AMP
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar rotas
from src.api.routes.health import router as health_router
from src.api.routes.variants import router as variants_router

# Criar app
app = FastAPI(
    title="CRISPR-MMR Explorer API",
    description="API para classificação de variantes MMR usando ACMG/AMP 2015",
    version="2.0.0",
)

# CORS: permitir Streamlit fazer requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: especificar URL do Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(variants_router, prefix="/api", tags=["variants"])

# Root endpoint
@app.get("/", tags=["root"])
def read_root():
    """Endpoint raiz da API"""
    return {
        "message": "CRISPR-MMR Explorer API v2.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "health": "GET /health",
            "classify": "POST /api/classify",
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
