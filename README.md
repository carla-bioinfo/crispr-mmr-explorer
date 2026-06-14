# 🧬 CRISPR-MMR Explorer

Uma **plataforma bioinformática completa** para análise, exploração e educação sobre variantes no sistema Mismatch Repair (MMR) e Síndrome de Lynch (HNPCC).

---

## 📋 Status do Projeto

### ✅ Fases Completadas

**Setup & Fundamentos (v0.1-v0.2)**
- ✅ Setup inicial
- ✅ Fundamentos teóricos (50+ páginas)
- ✅ Coleta de dados (10 variantes)

**Refatoração v0.5.0 (Em Andamento)**
- ✅ **Etapa 0.1**: ACMG Classifier v0.4.0 com ACMG/AMP 2015 correto
- ✅ **Etapa 0.2**: Pydantic Validation + Limpeza de código
- ✅ **Etapa 0.3**: Logging + Exception Handling (v0.5.0) ← NOVA!
- ⏳ **Etapa 0.4**: Testes + QA (próxima)

**Fases Legacy (v0.3.0)**
- ✅ Fase 3A: SQLite Database
- ✅ Fase 3B: Streamlit Dashboard (5 seções)

---

## 🎯 O que é este Projeto?

CRISPR-MMR Explorer demonstra:
- 🧬 **Bioinformática Translacional**: Síndrome de Lynch, genes MMR, ACMG/AMP 2015
- 💻 **Engenharia de Software**: Arquitetura modular, validação, testes, logging
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

### Executar Análise ACMG v0.5.0 (com Logging)

```bash
python3 src/variants/acmg_analyzer.py
```

Resultado salvo em: `data/processed/clinvar_mmr_with_acmg_v0.5.0.csv`

Logs em: `logs/crispr_mmr_YYYYMMDD.log`

### Ver Logs em Tempo Real

```bash
tail -f logs/crispr_mmr_*.log
```

### Executar Dashboard

```bash
streamlit run app.py
```

Acesse: http://localhost:8501

---

## 🔬 ACMG Classifier v0.5.0

### O que é Novo (Etapa 0.3)

**Logging Profissional:**
- Rastreamento completo de todas as operações
- Arquivo de log permanente: `logs/crispr_mmr_YYYYMMDD.log`
- Diferentes níveis: DEBUG, INFO, WARNING, ERROR
- Formato estruturado com data/hora, função, linha

**Exception Handling Robusto:**
- Custom exceptions específicas do projeto
- Tratamento estruturado com try/except/finally
- Fácil identificação e debugging de erros

**Estrutura de Pacotes:**
- Novo pacote `src/utils/` com utilidades reutilizáveis
- Importações limpas e organizadas
- Fácil manutenção e expansão

---

## 📁 Estrutura do Projeto (v0.5.0)
crispr-mmr-explorer/

├── src/

│   ├── variants/

│   │   ├── acmg_analyzer.py (v0.5.0) ← Com logging + exceptions

│   │   ├── models.py (Pydantic validation)

│   │   ├── database.py

│   │   └── init.py

│   │

│   └── utils/ ← NOVO

│       ├── logger.py (Sistema de logging)

│       ├── exceptions.py (Custom exceptions)

│       ├── init.py (Imports facilitados)

│       └── pycache/

│

├── data/

│   ├── raw/

│   │   └── clinvar_mmr_variants.csv

│   └── processed/

│       └── clinvar_mmr_with_acmg_v0.5.0.csv

│

├── logs/ ← NOVO

│   └── crispr_mmr_*.log (Arquivo de log diário)

│

├── app.py (Streamlit Dashboard)

├── requirements.txt

├── README.md

├── RESUMO_SESSAO_0.3_COMPLETO.md ← Nova documentação

└── .git/
---

## 🔬 ACMG Classifier v0.4.0 (Lógica Base)

### Implementação ACMG/AMP 2015

Diferente de v0.3.0, v0.4.0+ implementa a **lógica ACMG/AMP 2015 correta**:

**Critérios Implementados:**
- **PVS1** (Muito Forte): Null variant em genes MMR (frameshift, stop_gained, splice_site)
- **PS1** (Forte): Mesma mudança já reportada como Pathogenic
- **PM2** (Moderado): Frequência alélica muito baixa (< 0.001%)
- **BA1** (Muito Forte Benign): Frequência alélica alta (> 5%)

**Regras de Decisão:**
1. 1+ PVS1 + 1+ PS1 → **Pathogenic (P)**
2. 1+ PVS1 ou (PS1 + PM2) → **Likely Pathogenic (LP)**
3. PM2 → **VUS (Variant of Uncertain Significance)**
4. 1+ BA1 → **Benign (B)**
5. Nenhum critério → **VUS**

### Comparação v0.3.0 vs v0.4.0+

| Aspecto | v0.3.0 | v0.4.0+ |
|---------|--------|---------|
| Lógica | Pontos (simplificado) | Regras ACMG (correto) |
| Científico | ❌ Não | ✅ ACMG 2015 |
| Validação | Nenhuma | ✅ Pydantic |
| Logging | ❌ Não | ✅ v0.5.0 |
| Exceptions | Nenhuma | ✅ v0.5.0 |
| Substitution | Pathogenic | ✅ VUS (correto) |

### Resultados (10 variantes teste)

**v0.4.0 (ACMG correto):**
Pathogenic: 5

Likely Pathogenic: 0

VUS: 5

Benign: 0
**v0.5.0 (Com logging + rastreamento):**
Pathogenic: 5

Likely Pathogenic: 0

VUS: 5

Benign: 0
Logs registrados: logs/crispr_mmr_20260614.log (2.5K)

Rastreamento completo: ✅ Sim
---

## 💾 Componentes Principais

### src/utils/logger.py (v0.5.0)

Sistema centralizado de logging:

```python
from src.utils import get_logger

logger = get_logger(__name__)
logger.info("Operação iniciada")
logger.error("Algo falhou")
```

Saída:
2026-06-14 18:06:44 | INFO     | CRISPR_MMR | <module>:10 | Operação iniciada

2026-06-14 18:06:44 | ERROR    | CRISPR_MMR | <module>:11 | Algo falhou
### src/utils/exceptions.py (v0.5.0)

Custom exceptions do projeto:

```python
from src.utils import VariantValidationError, ACMGClassificationError

try:
    # validação
except VariantValidationError as e:
    logger.error(f"Validação falhou: {e}")
except ACMGClassificationError as e:
    logger.error(f"Classificação falhou: {e}")
```

---

## 🧪 Genes MMR Suportados

- ✅ MLH1 (Mutl Homolog 1)
- ✅ MSH2 (MutS Homolog 2)
- ✅ MSH6 (MutS Homolog 6)
- ✅ PMS2 (PMS1 Homolog 2)
- ✅ EPCAM (Epithelial Cell Adhesion Molecule)

---

## 📚 Referências

### ACMG/AMP 2015
- Richards et al. Genetics in Medicine. 2015
- https://www.ncbi.nlm.nih.gov/pubmed/25741868

### Síndrome de Lynch & Genes MMR
- InSiGHT Database: https://www.insight-group.org/
- ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/

### Documentação Técnica
- Pydantic: https://docs.pydantic.dev/
- Python Logging: https://docs.python.org/3/library/logging.html

---

## 👤 Autor

**Carla Rodrigues** | Bioinformática Clínica Translacional

- 🔗 GitHub: https://github.com/carla-bioinfo
- 💼 LinkedIn: https://www.linkedin.com/in/carla-bioinfo/
- 📧 Email: carlabio.biomol@gmail.com

---

## 📄 Licença

MIT License - Veja LICENSE para detalhes

---

## 🚀 Próximas Etapas

**Etapa 0.4 (Próxima):**
- Unit Tests com pytest
- Integration Tests
- Edge Cases
- Code Coverage (80%+)

**Etapa 0.5+:**
- Dataset expandido (50+ variantes)
- Adicionar allele_frequency
- Integração com bases de dados online
- API REST

---

## 📞 Contato & Suporte

Dúvidas? Sugestões? Issues?

👉 Abra uma issue no GitHub: https://github.com/carla-bioinfo/crispr-mmr-explorer/issues

---

**Última atualização:** 14 de Junho de 2026 (Etapa 0.3)  
**Versão atual:** v0.5.0  
**Status:** Em desenvolvimento ✅
