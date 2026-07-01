"""
Testes unitários para FastAPI v2.0.0
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app


class TestHealth:
    """Testes para /health"""
    
    def test_health_check(self):
        """GET /health/ retorna 200"""
        client = TestClient(app)
        response = client.get("/health/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["service"] == "CRISPR-MMR Explorer API"


class TestRoot:
    """Testes para /"""
    
    def test_root_endpoint(self):
        """GET / retorna informações da API"""
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "CRISPR-MMR Explorer API v2.0.0"
        assert "endpoints" in data


class TestClassify:
    """Testes para POST /api/classify"""
    
    def test_classify_valid_variant(self):
        """POST /api/classify com dados válidos"""
        client = TestClient(app)
        payload = {
            "chromosome": "3",
            "position": 36993722,
            "ref": "A",
            "alt": "G",
            "gene": "MLH1"
        }
        response = client.post("/api/classify", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["gene"] == "MLH1"
        assert data["data"]["pathogenicity_class"] == "Likely Pathogenic"
    
    def test_classify_missing_gene(self):
        """POST /api/classify SEM gene (deve falhar)"""
        client = TestClient(app)
        payload = {
            "chromosome": "3",
            "position": 36993722,
            "ref": "A",
            "alt": "G",
            "gene": None
        }
        response = client.post("/api/classify", json=payload)
        assert response.status_code == 400
    
    def test_classify_invalid_position(self):
        """POST /api/classify com position string (Pydantic rejeita)"""
        client = TestClient(app)
        payload = {
            "chromosome": "3",
            "position": "INVALIDO",
            "ref": "A",
            "alt": "G",
            "gene": "MLH1"
        }
        response = client.post("/api/classify", json=payload)
        assert response.status_code == 422
