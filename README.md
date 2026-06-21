# 🧬 CRISPR-MMR Explorer
Uma **plataforma bioinformática completa** para análise, exploração e educação sobre variantes no sistema Mismatch Repair (MMR) e Síndrome de Lynch (HNPCC).

---

## 📋 Status do Projeto

### ✅ Fases Completadas

**Refatoração v0.5.0 - VERSÃO ATUAL**
- ✅ **Etapa 0.1**: ACMG Classifier v0.4.0 com ACMG/AMP 2015 correto
- ✅ **Etapa 0.2**: Pydantic Validation + Limpeza de código
- ✅ **Etapa 0.3**: Logging + Exception Handling (v0.5.0)
- ✅ **Etapa 0.4**: Testes + Code Coverage iniciais (v0.5.0)
- ✅ **Etapa 0.5**: Aumentar Coverage para 78% (v0.5.0)
- ✅ **Etapa 0.6**: Aumentar Coverage para 86% + Error Handling
- ✅ **Etapa 0.7**: Migração Pydantic V1 → V2 (Zero warnings) ← NOVO!
- ✅ **Etapa 0.8**: Refatorar __main__ para função testável (94% coverage) ← NOVO!

**Próximas Etapas**
- 🔄 **Etapa 0.9**: GitHub Actions CI/CD (testes automáticos)
- 📋 **Etapa 1.0**: Release v1.0.0 (tag oficial)
- 📋 **BONUS**: Dashboard Streamlit + APIs FastAPI

---

## 📊 Métricas Atuais (Etapas 0.7-0.8)

| Métrica | Valor | Status |
|---------|-------|--------|
| **Coverage acmg_analyzer.py** | 94% | ✅ EXCELENTE |
| **Testes Unitários + Integração** | 43 | ✅ ROBUSTO |
| **Testes Passando** | 43/43 (100%) | ✅ PERFEITO |
| **Linhas Cobertas** | 115/122 | ✅ |
| **Genes MMR Testados** | 5 | ✅ MLH1, MSH2, MSH6, PMS2, EPCAM |
| **Critérios ACMG** | 4 | ✅ PVS1, PS1, PM2, BA1 (100% cobertura) |
| **Warnings Pydantic** | 0 | ✅ ZERO WARNINGS |

---

## 🧪 Testes - Etapas 0.7-0.8 NOVA!

### Progressão de Testes e Coverage

| Etapa | Testes | Coverage | Status |
|-------|--------|----------|--------|
| **0.4** | 6 | 62% | ✅ |
| **0.5** | 27 | 78% | ✅ |
| **0.6** | 40 | 86% | ✅ |
| **0.7** | 40 | 86% | ✅ Pydantic V2 OK |
| **0.8** | 43 | 94% | ✅ ATUAL |
| **0.9** | 43 | 94% | 🔄 Próxima |
| **1.0** | 43 | 94% | 📋 Release |

### Estrutura Completa de Testes
```
tests/
├── conftest.py                              # 6 fixtures reutilizáveis
├── unit/
│   ├── test_acmg_analyzer.py                # 5 testes
│   ├── test_acmg_criteria.py                # 12 testes
│   ├── test_acmg_classifier_combinations.py # 6 testes
│   ├── test_acmg_process_csv.py             # 3 testes
│   ├── test_acmg_error_handling.py          # 6 testes
│   ├── test_acmg_exception_forcing.py       # 3 testes
│   └── test_main_function.py                # 3 testes ⭐ NOVO (Etapa 0.8)
└── integration/
    ├── test_integration.py                  # 1 teste
    ├── test_main_block.py                   # 2 testes
    └── test_main_advanced.py                # 2 testes
```

### Rodar Testes

```bash
# Ativar virtual environment
source ~/crispr-mmr-explorer/venv/bin/activate

# Todos os testes
pytest tests/ -v

# Apenas testes unitários
pytest tests/unit/ -v

# Apenas testes de integração
pytest tests/integration/ -v

# Code coverage detalhado
pytest tests/ --cov=src.variants.acmg_analyzer --cov-report=term-missing

# Teste específico
pytest tests/unit/test_main_function.py -v
```

---

## 🧬 Cobertura Bioinformática

### Genes Mismatch Repair (MMR) - 100% Testados
- ✅ **MLH1** (Ligase de DNA)
- ✅ **MSH2** (Sensor de mismatch)
- ✅ **MSH6** (Sensor de mismatch)
- ✅ **PMS2** (Exonuclease 1)
- ✅ **EPCAM** (Regulador)

### Critérios ACMG/AMP 2015 - 100% Testados
- ✅ **PVS1**: Null variant em gene com LoF
- ✅ **PS1**: Já reportado como Pathogenic
- ✅ **PM2**: Frequência muito baixa
- ✅ **BA1**: Frequência alta (benigno)
- ✅ **Combinações**: Lógica de múltiplos critérios

### Tipos de Variantes Testadas
- ✅ Frameshift (insertion/deletion)
- ✅ Stop-gained (nonsense)
- ✅ Missense (substitution)
- ✅ Splice site (splicing)
- ✅ Duplication (copy number)

---

## 🚀 Instalação e Setup

### Requisitos
- Python 3.9+
- pip ou conda

### Instalação

```bash
# Clonar repositório
git clone https://github.com/carla-bioinfo/crispr-mmr-explorer.git
cd crispr-mmr-explorer

# Criar virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar testes
pytest tests/ -v
```

---

## 📚 Uso da Biblioteca

### Classificar Uma Variante (ACMG/AMP 2015)

```python
from src.variants.acmg_analyzer import ACMGClassifier
from src.variants.models import VariantInput

# Criar classifier
classifier = ACMGClassifier()

# Criar variante
variant = VariantInput(
    clinvar_id="VCV000000001",
    gene="MLH1",
    hgvs="MLH1:c.100delA",
    tipo="frameshift",
    classificacao="Pathogenic",
    allele_frequency=0.000001
)

# Classificar
resultado = classifier.classify(variant)
print(f"Classificação: {resultado}")
# Output: Classificação: Pathogenic
```

### Processar Arquivo CSV

```python
from src.variants.acmg_analyzer import process_csv

# Processar arquivo
total = process_csv(
    "data/raw/clinvar_mmr_variants.csv",
    "data/processed/output_with_acmg.csv"
)

print(f"✅ {total} variantes processadas")
```

---

## 📁 Estrutura do Projeto

```
crispr-mmr-explorer/
│
├── src/
│   ├── variants/
│   │   ├── acmg_analyzer.py          (122 linhas, 94% coverage)
│   │   ├── models.py                 (Pydantic V2, zero warnings)
│   │   ├── database.py
│   │   ├── query_variants.py
│   │   └── ...
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── exceptions.py
│   │   └── ...
│   │
│   └── [outras pastas]
│
├── tests/
│   ├── conftest.py
│   ├── unit/            (40 testes)
│   └── integration/      (3 testes)
│
├── data/
│   ├── raw/             (dados de entrada)
│   └── processed/       (resultados)
│
├── README.md            ← ESTE ARQUIVO
├── CHANGELOG.md
├── requirements.txt
└── venv/                (virtual environment)
```

---

## 🔬 Metodologia Científica

### Padrões Internacionais Utilizados

1. **ACMG/AMP 2015** - Richards et al. (PMID: 25741868)
   - Classificação de variantes: Pathogenic/Likely Pathogenic/VUS/Likely Benign/Benign
   - Critérios evidência-baseados
   - Aplicado a genes MMR da Síndrome de Lynch

2. **Frequência Alélica** - gnomAD
   - Populações globais
   - Impacto na classificação (BA1, PM2)

3. **Síndrome de Lynch (HNPCC)**
   - Penetrância variável
   - Validação funcional necessária
   - Segregação familiar crítica

---

## 📊 Roadmap Futuro

### Etapa 0.9 (Próxima - GitHub Actions CI/CD)
- [ ] Criar `.github/workflows/tests.yml`
- [ ] Testes automáticos em cada push
- [ ] Coverage reports no GitHub
- [ ] Badge no README

### Etapa 1.0 (Release Official)
- [ ] Tag release v1.0.0
- [ ] Atualizar CHANGELOG.md
- [ ] GitHub Release com notas
- [ ] Anúncio no LinkedIn

### BONUS (Dashboard + APIs)
- [ ] Dashboard Streamlit (5 páginas)
- [ ] APIs FastAPI (2 endpoints)
- [ ] Deploy no Streamlit Cloud

---

## 📞 Contato e Contribuições

**Desenvolvido por:** Especialista em Bioinformática Clínica Translacional  
**GitHub:** [carla-bioinfo/crispr-mmr-explorer](https://github.com/carla-bioinfo/crispr-mmr-explorer)  
**Versão:** v0.5.0 (Etapas 0.7-0.8 Completas)  
**Data Última Atualização:** 17 de Junho de 2026

---

## 🎓 Referências

### ACMG/AMP 2015
- **Autores:** Richards, S., Aziz, N., Bast, S., et al.
- **PMID:** 25741868
- **DOI:** 10.1038/gim.2015.30
- **Título:** Standards and Guidelines for the Interpretation of Sequence Variants

### Síndrome de Lynch
- **Genes:** MLH1, MSH2, MSH6, PMS2, EPCAM
- **Sistema:** Mismatch Repair (MMR)
- **Base:** InSiGHT database

### Ferramentas
- **Python 3.9.2** | **Pytest 7.4.2** | **Pydantic 2.3.0**
- **pandas 2.0.3** | **Coverage 7.10.7**

---

## 📈 Histórico de Versões

### v0.5.0 (Etapas 0.7-0.8) - 17 JUN 2026
- ✅ Migração Pydantic V1 → V2 (Etapa 0.7)
- ✅ Refatoração __main__ → main() (Etapa 0.8)
- ✅ Coverage: 86% → 94%
- ✅ Testes: 40 → 43
- ✅ Zero Pydantic warnings

### v0.5.0 (Etapa 0.6) - 16 JUN 2026
- ✅ Aumentar coverage para 86%
- ✅ 13 novos testes
- ✅ Error handling robusto
- ✅ 40 testes totais passando

### v0.5.0 (Etapas 0.1-0.5)
- ✅ ACMG Classifier profissional
- ✅ Pydantic validation
- ✅ Logging + Exception handling
- ✅ 27 testes com 78% coverage

---

**✅ Projeto em desenvolvimento ativo!**

**Próximas ações:**
1. Etapa 0.9: GitHub Actions CI/CD
2. Etapa 1.0: Release v1.0.0
3. BONUS: Dashboard Streamlit
4. BONUS: APIs FastAPI
5. 
