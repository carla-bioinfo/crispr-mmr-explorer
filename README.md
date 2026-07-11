# CRISPR-MMR Explorer

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.8-green)](https://fastapi.tiangolo.com/)
[![Tests Passing](https://img.shields.io/badge/tests-50%2F50%20passing-success)](./tests/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Classificação de variantes genéticas em genes *Mismatch Repair* (MMR) usando critérios ACMG/AMP 2015, com foco em **Síndrome de Lynch**.

**Status:** v2.0.2 | 🔴 **Fase 4 completa** — Backend com rastreabilidade ACMG | 🟡 Fase 5 em progresso — Documentação e Portfolio

---

## 🎯 O que é este projeto?

Este é um **projeto de aprendizagem em bioinformática clínica** realizado como estágio de formação. O objetivo é construir uma **pipeline de classificação de variantes genéticas** que:

1. **Recebe** um dado genômico (gene, posição, alelos)
2. **Calcula** evidência ACMG/AMP 2015 (critérios de patogenicidade)
3. **Retorna** classificação interpretável + score de confiança + rastreabilidade

**Contexto científico:** A Síndrome de Lynch é a predisposição hereditária ao câncer colorretal mais comum, causada por variantes germinativas nos genes MMR (MLH1, MSH2, MSH6, PMS2, EPCAM). Interpretar corretamente essas variantes é crítico para o manejo clínico.

**Scope do projeto:**
- ✅ FASE 4: Backend FastAPI com ACMG classifier funcional
- 🟡 FASE 5: README + Portfolio
- 🔵 FASE 6: Frontend React + Tailwind
- 🟣 FASE 7: Genes MSH2, MSH6, PMS2 com dados clinicamente relevantes
- 🟠 FASE 8: Integração com APIs públicas (ClinVar, gnomAD)

---

## 🏗️ Arquitetura (FASE 4)

### Componentes principais
┌──────────────────────────────────────────────────────────────────┐
│                        USER / FRONTEND                            │
│                    (Será React em FASE 6)                         │
└────────────────────────┬─────────────────────────────────────────┘
                       │
     POST /api/classify
  {gene, chromosome, position, ref, alt}
│
┌────────────────────────▼─────────────────────────────────────────┐
│                      FastAPI Router                               │
│              src/api/routes/variants.py                           │
│  • Valida input (Pydantic schema)                                │
│  • Chama adapter para normalizar dados                           │
│  • Invoca classifier                                              │
└────────────────────────┬─────────────────────────────────────────┘
         │
classify_with_details()
(retorna: classe, critérios, score)
                     │
┌────────────────────────▼─────────────────────────────────────────┐
│               ACMGClassifier                                      │
│         src/variants/acmg_analyzer.py                             │
│                                                                    │
│  1. Detecta tipo de mutação (frameshift, deletion, etc)          │
│  2. Busca frequência do alelo                                    │
│  3. Calcula scores ACMG:                                         │
│     • PVS1 (+4): frameshift/stop → muito deletério              │
│     • PM2 (+1): alelo muito raro (freq < 0.001)                 │
│     • PP3 (+1): tipo complexo + raro                            │
│     • BP4 (-1): alelo moderadamente raro (freq 0.001-0.01)     │
│  4. Soma pontos → classificação final                            │
└────────────────────────┬─────────────────────────────────────────┘
│
        allele_frequency lookup
      (gnomAD, ClinVar, etc)
              │
┌────────────────────────▼─────────────────────────────────────────┐
│              JSON Response                                         │
│                                                                    │
│  {                                                                 │
│    "pathogenicity_class": "PATHOGENIC",                          │
│    "acmg_criteria": ["PVS1", "PM2", "PP3"],                     │
│    "confidence_score": 0.95,                                     │
│    "reasoning": "frameshift + rare + ......"                    │
│  }                                                                 │
└──────────────────────────────────────────────────────────────────┘
---

## 📊 Métricas ACMG/AMP 2015 (Calibradas para Lynch)

A classificação segue o framework ACMG/AMP 2015, com critérios calibrados para genes MMR conforme **ClinGen InSiGHT Hereditary Colorectal Cancer VCEP**.

### Escala de Pontos

| Critério | Tipo | Pontos | Acionador |
|----------|------|--------|-----------|
| **PVS1** | Muito forte | +4 | Frameshift, stop-gain, deletion/inserção sem mudança de fase, indel em splice site conservado |
| **PM2** | Moderado | +1 | Alelo muito raro em população geral (AF < 0.001 em gnomAD) |
| **PP3** | Suportivo | +1 | Frequência rara (< 0.001) **E** tipo de mutação complexo (não-substitution) |
| **BP4** | Suportivo contra | -1 | Alelo em frequência moderada (0.001 ≤ AF < 0.01) — sugere variação benigna |

### Classificação Final
≥ 6 pontos         → PATHOGENIC (confiança 0.95)
3–5 pontos       → LIKELY_PATHOGENIC (0.80)
-2 a 2 pontos    → VUS / Uncertain Significance (0.50)
≤ -2 pontos      → LIKELY_BENIGN (0.20)
---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.9+
- pip ou poetry
- Git

### Instalação local

```bash
# 1. Clonar repositório
git clone https://github.com/carla-bioinfo/crispr-mmr-explorer.git
cd crispr-mmr-explorer

# 2. Criar environment virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar testes (validar setup)
pytest tests/ -v

# 5. Iniciar servidor local
python -m uvicorn src.api.main:app --reload --port 8000
```

**Output esperado:**
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
### Usar em produção (Railway)
Endpoint: https://crispr-mmr-explorer-production.up.railway.app
Status:   ✅ Live (FASE 4)
Testes:   50/50 passando
---

## 📡 API — Exemplos de Uso

### Endpoint: `POST /api/classify`

**URL:**
http://localhost:8000/api/classify          (local)
https://crispr-mmr-explorer-production.up.railway.app/api/classify  (produção)
**Headers:**
Content-Type: application/json
**Request body:**
```json
{
  "gene": "MLH1",
  "chromosome": "3",
  "position": 36993722,
  "ref": "AGT",
  "alt": "A",
  "allele_frequency": 0.0
}
```

### Exemplo 1: Deletção MLH1 (Esperado → PATHOGENIC)

```bash
curl -X POST http://localhost:8000/api/classify \
  -H "Content-Type: application/json" \
  -d '{
    "gene": "MLH1",
    "chromosome": "3",
    "position": 36993722,
    "ref": "AGT",
    "alt": "A"
  }'
```

**Resposta esperada:**
```json
{
  "pathogenicity_class": "PATHOGENIC",
  "acmg_criteria": ["PVS1", "PM2", "PP3"],
  "confidence_score": 0.95,
  "reasoning": "Frameshift deletion (PVS1: +4) in lynchpin MLH1 gene, extremely rare (PM2: +1), complex mutation type (PP3: +1). Score: 6 points = PATHOGENIC."
}
```

---

## 🧪 Testes

**Rodar todos os testes:**
```bash
pytest tests/ -v
```

**Output:**
tests/test_acmg_analyzer.py ........................ 43 passed
tests/test_api.py ............................. 7 passed
================================ 50 passed in 2.34s ===============

**Rodar com cobertura:**
```bash
pytest tests/ --cov=src --cov-report=html
```

---

## 🔧 Estrutura do Projeto
crispr-mmr-explorer/
├── src/
│   ├── api/
│   │   ├── main.py                 # FastAPI app
│   │   ├── routes/
│   │   │   └── variants.py         # POST /api/classify
│   │   ├── schemas.py              # Pydantic models
│   │   └── adapter.py              # Normaliza campos
│   ├── variants/
│   │   ├── acmg_analyzer.py        # ACMGClassifier
│   │   ├── utils.py                # get_gnomad_frequency()
│   │   ├── models.py               # Models
│   │   └── database.py             # Database setup
│   ├── data/
│   │   └── real_lynch_variants.json
│   └── utils/
│       └── logger.py               # Logging
├── tests/
│   ├── test_acmg_analyzer.py       # Unit tests (43)
│   └── test_api.py                 # API tests (7)
├── requirements.txt
├── pytest.ini
└── README.md
---

## 🐛 Gotchas & Learnings (FASE 4)

### 1. Campo "tipo" vs "type" (Bilíngue)

**Problema:** Adaptador retorna "tipo", mas código esperava "type".

**Solução:**
```python
mutation_type = (variant.get("type") or variant.get("tipo") or "substitution").lower()
```

### 2. `allele_frequency = None` quebra comparações

**Problema:** Comparação `None < 0.001` falhava.

**Solução:**
```python
allele_freq = variant.get("allele_frequency") or 0.0001
```

### 3. Versão Starlette incompatível

**Problema:** FastAPI 0.104.1 + Starlette 0.27.0 → TestClient quebrava.

**Solução:** Upgrade para FastAPI 0.128.8 + Starlette 0.49.3

---

## 📚 Referências & Leitura

### ACMG/AMP 2015 Framework
- [Richards et al. (2015), Genet Med](https://pubmed.ncbi.nlm.nih.gov/25741868/)

### Lynch Syndrome & MMR Genes
- [ClinGen InSiGHT VCEP](https://clinicalgenome.org/clingen-projects/hereditary-cancers/)
- [InSiGHT Database](https://www.insightdatabase.org/)

### Ferramentas
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/)
- [gnomAD](https://gnomad.broadinstitute.org/)

---

## 🤝 Contribuir

Reportar bugs em [Issues](https://github.com/carla-bioinfo/crispr-mmr-explorer/issues).
Sugerir melhorias em [Discussions](https://github.com/carla-bioinfo/crispr-mmr-explorer/discussions).

---

## 📖 Roadmap
FASE 1-3: ✅ Infraestrutura
FASE 4:   ✅ Backend ACMG classifier
FASE 5:   🟡 Documentação + Portfolio
FASE 6:   🔵 Frontend React
FASE 7:   🟣 Genes MSH2, MSH6, PMS2
FASE 8:   🟠 APIs reais
---

## 📝 Licença

MIT License

---

## 👤 Autor

**Carla** — Estudante de Biomedicina + Ciência de Dados
📧 carlabio.biomol@gmail.com
🔗 [GitHub](https://github.com/carla-bioinfo) | [LinkedIn](https://linkedin.com/in/carla-bioinfo/)

---

**Última atualização:** 11 de Julho de 2026 | FASE 4 ✅
