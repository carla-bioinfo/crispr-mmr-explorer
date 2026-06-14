# 🧬 CRISPR-MMR Explorer
Uma **plataforma bioinformática completa** para análise, exploração e educação sobre variantes no sistema Mismatch Repair (MMR) e Síndrome de Lynch (HNPCC).

---

## 📋 Status do Projeto

### ✅ Fases Completadas

**Refatoração v0.5.0 (Em Andamento)**
- ✅ **Etapa 0.1**: ACMG Classifier v0.4.0 com ACMG/AMP 2015 correto
- ✅ **Etapa 0.2**: Pydantic Validation + Limpeza de código
- ✅ **Etapa 0.3**: Logging + Exception Handling (v0.5.0)
- ✅ **Etapa 0.4**: Testes + Code Coverage (v0.5.0) ← NOVO!
- ⏳ **Etapa 0.5**: Aumentar Coverage para 80%+ (próxima)

**Fases Legacy (v0.3.0)**
- ✅ Fase 3A: SQLite Database
- ✅ Fase 3B: Streamlit Dashboard (5 seções)

---

## 🧪 Testes (Etapa 0.4) - NOVO!

### Estrutura de Testes
tests/

├── conftest.py                      # Fixtures reutilizáveis

├── unit/

│   └── test_acmg_analyzer.py       # 5 testes unitários

└── integration/

└── test_integration.py         # 1 teste de integração
### Rodar Testes

```bash
# Todos os testes
pytest tests/ -v

# Apenas unitários
pytest tests/unit/ -v

# Code coverage
pytest tests/ --cov=src.variants --cov-report=term-missing
```

### Resultados
✅ 6 testes total

✅ 100% de sucesso

✅ 62% code coverage em acmg_analyzer.py

✅ 92% code coverage em models.py
---

## 🎯 O que é este Projeto?

CRISPR-MMR Explorer demonstra:
- 🧬 **Bioinformática Translacional**: ACMG/AMP 2015
- 💻 **Engenharia de Software**: Testes, Logging, Validação
- 📊 **Ciência de Dados**: SQLite, pandas, plotly
- 🔬 **Qualidade**: Code Coverage, TDD, Git

---

## 🚀 Quick Start

```bash
# Instalação
git clone https://github.com/carla-bioinfo/crispr-mmr-explorer.git
cd crispr-mmr-explorer
source venv/bin/activate

# Executar análise
python3 src/variants/acmg_analyzer.py

# Executar testes
pytest tests/ -v
```

---

**Última atualização:** 14 de Junho de 2026
**Versão:** v0.5.0
**Status:** Etapa 0.4 Completa ✅
