# 🧬 CRISPR-MMR Explorer

Uma **plataforma bioinformática completa** para análise, exploração e educação sobre variantes no sistema Mismatch Repair (MMR) e Síndrome de Lynch (HNPCC).

---

## 📋 Status do Projeto

✅ Módulo 1: Setup - COMPLETO
✅ Módulo 2: Fundamentos Teóricos - COMPLETO (50+ páginas)
✅ Módulo B: Coleta de Dados + ACMG - COMPLETO (10 variantes)
✅ Fase 3A: SQLite Database - COMPLETO
✅ Fase 3B: Streamlit Dashboard - COMPLETO

---

## 🎯 O que é este Projeto?

CRISPR-MMR Explorer demonstra:

- 🧬 **Bioinformática Translacional**: Síndrome de Lynch, genes MMR, ACMG
- 💻 **Engenharia de Software**: Arquitetura modular, testes, Git
- 📊 **Ciência de Dados**: SQLite, pandas, plotly
- 🎨 **Interface Web**: Streamlit interativo
- 🔬 **Rigor Científico**: Validação, reproduzibilidade

---

## 🚀 Quick Start

### Instalação

```bash
git clone https://github.com/carla-bioinfo/crispr-mmr-explorer.git
cd crispr-mmr-explorer
source venv/bin/activate
pip install -r requirements.txt
```

### Executar Dashboard

```bash
streamlit run app.py
```

Acesse: http://localhost:8501

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

**Classificação ACMG**:
- Pathogenic (P): 5 (50%)
- Likely Pathogenic (LP): 4 (40%)
- Benign (B): 1 (10%)

**Score**: Média 3.40 (0-5)

---

## 🛠️ Stack Tecnológico

- Python 3.9
- SQLite
- Streamlit 1.28.1
- pandas, plotly
- Git/GitHub

---

## 📝 Licença

MIT License

---

## 👤 Autor

Carla Rodrigues - Bioinformática Clínica

---

**v0.3.0** - Junho 2026

*Making bioinformatics accessible, reproducible, and beautiful.*
