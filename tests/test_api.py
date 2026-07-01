"""
Testes unitários para FastAPI v2.0.1 com ACMGClassifier Real
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


class TestRoot:
    """Testes para /"""
    
    def test_root_endpoint(self):
        """GET / retorna informações da API"""
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "CRISPR-MMR Explorer API v2.0.0"


class TestClassify:
    """Testes para POST /api/classify com ACMGClassifier REAL"""
    
    def test_classify_substitution_returns_vus(self):
        """Substitution simples → VUS"""
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
        assert data["data"]["pathogenicity_class"] == "VUS"
    
    def test_classify_deletion_returns_likely_pathogenic(self):
        """Deletion em MLH1 → Likely Pathogenic"""
        client = TestClient(app)
        payload = {
            "chromosome": "3",
            "position": 36993722,
            "ref": "AGT",
            "alt": "A",
            "gene": "MLH1"
        }
        response = client.post("/api/classify", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["pathogenicity_class"] == "Likely Pathogenic"
    
    def test_classify_missing_gene(self):
        """POST com gene None → HTTP 422 (validation error)"""
        client = TestClient(app)
        payload = {
            "chromosome": "3",
            "position": 36993722,
            "ref": "A",
            "alt": "G",
            "gene": None
        }
        response = client.post("/api/classify", json=payload)
        assert response.status_code == 422
    
    def test_classify_invalid_position(self):
        """Position string → HTTP 422"""
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
    
    def test_classify_invalid_gene(self):
        """Gene não MMR (BRCA1) → HTTP 422"""
        client = TestClient(app)
        payload = {
            "chromosome": "3",
            "position": 36993722,
            "ref": "A",
            "alt": "G",
            "gene": "BRCA1"
        }
        response = client.post("/api/classify", json=payload)
        assert response.status_code == 422
