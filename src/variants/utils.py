
def get_gnomad_frequency(gene: str, hgvs: str) -> dict:
    """
    Busca frequência alélica no gnomAD v4 (fallback: dados mock).
    Exemplo: get_gnomad_frequency("MLH1", "MLH1:c.1528_1529delAA")
    Retorna: {"frequency": 0.00001, "source": "gnomad_v4"}
    """
    # Mock data — em produção seria API real gnomAD
    mock_freqs = {
        "MLH1:c.1528_1529delAA": {"frequency": 0.00001, "source": "gnomad_v4"},
        "MSH2:c.942+1G>A": {"frequency": 0.00002, "source": "gnomad_v4"},
        "MSH6:c.3226_3227insA": {"frequency": 0.000008, "source": "gnomad_v4"}
    }
    
    return mock_freqs.get(hgvs, {"frequency": 0.0001, "source": "unknown"})

