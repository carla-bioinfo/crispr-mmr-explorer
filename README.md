# 🧬 CRISPR-MMR Explorer

Uma **plataforma bioinformática completa** para análise, exploração e educação sobre variantes no sistema Mismatch Repair (MMR) e Síndrome de Lynch (HNPCC).

---

## 📋 Status do Projeto

### ✅ Fases Completadas

**Setup & Fundamentos (v0.1-v0.2)**
- ✅ Setup inicial
- ✅ Fundamentos teóricos (50+ páginas)
- ✅ Coleta de dados (10 variantes)

**Refatoração v0.4.0 (Em Progresso)**
- ✅ **Etapa 0.1**: ACMG Classifier v0.4.0 com ACMG/AMP 2015 correto
- ✅ **Etapa 0.2**: Pydantic Validation + Limpeza de código
- ⏳ **Etapa 0.3**: Logging + Exception Handling (próxima)
- ⏳ **Etapa 0.4**: Dataset expandido com allele_frequency

**Fases Legacy (v0.3.0)**
- ✅ Fase 3A: SQLite Database
- ✅ Fase 3B: Streamlit Dashboard (5 seções)

---

## 🎯 O que é este Projeto?

CRISPR-MMR Explorer demonstra:

- 🧬 **Bioinformática Translacional**: Síndrome de Lynch, genes MMR, ACMG/AMP 2015
- 💻 **Engenharia de Software**: Arquitetura modular, validação, testes
- 📊 **Ciência de Dados**: SQLite, pandas, plotly
- 🎨 **Interface Web**: Streamlit interativo
- 🔬 **Rigor Científico**: Validação Pydantic, reproduzibilidade, Git

---

## 🚀 Quick Start

### Instalação

```bash
git clone https://github.com/carla-bioinfo/crispr-mmr-explorer.git
cd crispr-mmr-explorer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Executar Análise ACMG v0.4.0

```bash
python3 src/variants/acmg_analyzer.py
```

Resultado salvo em: `data/processed/clinvar_mmr_with_acmg_v0.4.0.csv`

### Executar Dashboard

```bash
streamlit run app.py
```

Acesse: http://localhost:8501

---

## 🔬 ACMG Classifier v0.4.0

### Implementação ACMG/AMP 2015

Diferente de v0.3.0, v0.4.0 implementa a **lógica ACMG/AMP 2015 correta**:

**Critérios Implementados:**
- **PVS1** (Muito Forte): Null variant em genes MMR (frameshift, stop_gained, splice_site)
- **PS1** (Forte): Mesma mudança já reportada como Pathogenic
- **PM2** (Moderado): Frequência alélica muito baixa (< 0.001%)
- **BA1** (Muito Forte Benign): Frequência alélica alta (> 5%)

**Regras de Decisão:**
1. 1+ PVS1 → **Pathogenic (P)**
2. 1+ PS1 → **Likely Pathogenic (LP)**
3. PM2 → **Likely Pathogenic (LP)**
4. 1+ BA1 → **Benign (B)**
5. Nenhum critério → **VUS (Variant of Uncertain Significance)**

### Comparação v0.3.0 vs v0.4.0

| Aspecto | v0.3.0 | v0.4.0 |
|---------|--------|--------|
| Lógica | Pontos (simplificado) | Regras ACMG (correto) |
| Científico | ❌ Não | ✅ ACMG 2015 |
| Validação | Nenhuma | ✅ Pydantic |
| Substitution | Pathogenic | ✅ VUS (correto) |

### Resultados (10 variantes)

**v0.3.0 (Simplificado):**
Pathogenic (P/LP): 9

Benign (B): 1

VUS: 0
**v0.4.0 (ACMG 2015 Correto):**
🔴 Pathogenic (P): 5

🟠 Likely Pathogenic (LP): 2

🟡 VUS: 3 ← Identifica corretamente variantes incertas!

🟢 Benign (B): 0
---

## 📦 Pydantic Validation

Cada variante é validada com **modelos Pydantic**:

```python
from src.variants.models import VariantInput

# Valida automaticamente:
# - clinvar_id: Começa com RCV ou VCV
# - gene: Um dos 5 genes MMR (MLH1, MSH2, MSH6, PMS2, EPCAM)
# - hgvs: Notação HGVS válida
# - tipo: Um dos tipos válidos (deletion, insertion, etc)
# - allele_frequency: Entre 0 e 1 (opcional)

variant = VariantInput(
    clinvar_id='VCV000000001',
    gene='MLH1',
    hgvs='MLH1:c.678_679delGT',
    classificacao='Pathogenic',
    tipo='deletion',
    allele_frequency=0.00001
)
```

---

## 📊 Fase 3A: SQLite Database

### Dados

- 10 variantes importadas de ClinVar
- Validação: 100% (0% diferença)
- Banco: `data/processed/variants.db`

### Scripts

- `database.py`: Classe VariantDatabase
- `import_from_csv.py`: Importador de dados
- `validate_import.py`: Validação de integridade
- `query_variants.py`: Consultas SQL

---

## 🎨 Fase 3B: Streamlit Dashboard

### Seções

1. **Home**: Estatísticas + Gráfico ACMG
2. **Variantes**: Tabela com filtros (Gene, ACMG, Tipo)
3. **Análises**: Gráficos de distribuição e box plot
4. **Por Gene**: Análise individual (MLH1, MSH2, MSH6, PMS2)
5. **Sobre**: Informações do projeto

### Features

- ✅ Tabelas interativas
- ✅ Gráficos Plotly
- ✅ Filtros dinâmicos
- ✅ Download CSV

---

## 📈 Dataset

**Total**: 10 variantes

**Por Gene**:
- MLH1: 3
- MSH2: 3
- MSH6: 2
- PMS2: 2

**Classificação ACMG v0.4.0**:
- Pathogenic (P): 5 (50%)
- Likely Pathogenic (LP): 2 (20%)
- VUS: 3 (30%)
- Benign (B): 0 (0%)

---

## 📁 Estrutura do Projeto
crispr-mmr-explorer/

├── src/

│   ├── variants/

│   │   ├── acmg_analyzer.py ✅ (v0.4.0 com Pydantic)

│   │   ├── acmg_analyzer_v0.3.0_backup.py

│   │   ├── models.py ✅ (Validação Pydantic)

│   │   ├── database.py

│   │   ├── query_variants.py

│   │   ├── validate_import.py

│   │   ├── import_from_csv.py

│   │   └── init.py

│   └── utils/

│       └── (próximas etapas)

├── data/

│   ├── raw/

│   │   └── clinvar_mmr_variants.csv

│   └── processed/

│       ├── variants.db

│       └── clinvar_mmr_with_acmg_v0.4.0.csv ✅

├── tests/

│   └── (próximas etapas)

├── docs/

│   └── (referências)

├── app.py (Streamlit)

├── requirements.txt

├── .git/ (2 commits v0.4.0)

└── README.md
---

## 🛠️ Stack Tecnológico

- **Python**: 3.9.2
- **Bioinformática**: Pydantic, BioPython
- **Database**: SQLite
- **Web**: Streamlit 1.28.1
- **Data**: pandas 2.0.3, plotly 5.15.0
- **Version Control**: Git 2.30.2
- **Testing**: pytest 7.4.0

---

## 📚 Próximas Etapas (v0.4.0)

### Etapa 0.3 (Próxima)
- Implementar logging system (`src/utils/logger.py`)
- Criar custom exceptions (`src/utils/exceptions.py`)
- Integrar ao ACMG Classifier
- **Tempo**: ~1 hora

### Etapa 0.4
- Expandir dataset para 30+ variantes
- Adicionar `allele_frequency` ao CSV
- Adicionar campos `msi_status` e `cancer_type`
- **Tempo**: ~1 hora

### Fases 1-2
- Testes unitários (pytest)
- Documentação (Architecture, Installation, Dataset)
- Segurança (SQL injection review, .gitignore)
- **Tempo**: ~3-4 horas

### Fases 3+
- APIs reais (Ensembl, VEP)
- CI/CD (GitHub Actions)
- Jupyter notebooks
- Publicação científica

---

## 📖 Referências

**ACMG/AMP 2015**
- Richards et al. Genetics in Medicine 17(5):405-424
- https://www.acmg.net/

**Síndrome de Lynch**
- InSiGHT Database: https://www.insightgroup.org/
- ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/

**Notação HGVS**
- https://varnomen.hgvs.org/

**Ferramentas**
- Pydantic: https://docs.pydantic.dev/
- Streamlit: https://docs.streamlit.io/

---

## 📝 Licença

MIT License

---

## 👤 Autor

**Carla Rodrigues** - Bioinformática Clínica  
GitHub: [@carla-bioinfo](https://github.com/carla-bioinfo)

---

**v0.4.0** - Junho 2026  
*Making bioinformatics accessible, reproducible, and scientifically rigorous.*
