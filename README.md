# 🧬 CRISPR-MMR Explorer
## Uma Plataforma Bioinformática para Análise de Genes Mismatch Repair e Síndrome de Lynch

![Status](https://img.shields.io/badge/Status-Development-yellow)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Maintenance](https://img.shields.io/badge/Maintenance-Active-brightgreen)

---

## 📋 Sobre o Projeto

**CRISPR-MMR Explorer** é uma plataforma bioinformática completa para análise, exploração e educação sobre genes do sistema **Mismatch Repair (MMR)** e a **Síndrome de Lynch**. 

Este projeto combina:
- ✅ **Rigor de Engenharia de Software** (testes, CI/CD, versionamento)
- ✅ **Precisão Biológica** (referências científicas, validação rigorosa)
- ✅ **Reprodutibilidade Científica** (dados públicos, metodologia clara)

### 🎯 Diferencial

- **Nicho de Alto Valor**: Foco em MMR, MSI e Síndrome de Lynch — essenciais em imunoterapia e oncogenética
- **Arquitetura de Produção**: Estrutura profissional com separação clara de responsabilidades
- **Validação Rigorosa**: 0% de diferença entre dados originais e processados
- **Testes Abrangentes**: Meta de cobertura ≥ 80%
- **Dashboard Interativo**: Visualizações em tempo real com Streamlit
- **Relatórios Científicos**: Exportação em PDF com qualidade de publicação

---

## 🏗️ Arquitetura do Projeto
│
├── data/
│   ├── raw/                    # Dados originais (ClinVar, InSiGHT)
│   ├── processed/              # Dados transformados
│   └── validation/             # Relatórios de validação
│
├── src/                        # Código principal modular
│   ├── ingestion/              # Parsers (ClinVar, InSiGHT, Ensembl)
│   ├── preprocessing/          # Normalização, validação
│   ├── variants/               # Banco de dados, classificação ACMG
│   ├── genomics/               # Sequências, análise CRISPR
│   ├── visualization/          # Plotly, gráficos interativos
│   ├── reports/                # Geração de PDFs científicos
│   ├── dashboard/              # Streamlit
│   └── utils/                  # Logging, configuração
│
├── notebooks/                  # Exploração de dados (Jupyter)
├── tests/                      # Testes automatizados (pytest)
├── docs/                       # Documentação científica e técnica
├── Dockerfile                  # Imagem para execução em container
└── requirements.txt            # Dependências Python---

## 🧬 Stack Tecnológico

### Backend & Processamento
- **pandas** — Manipulação de dados tabulares
- **numpy** — Computação numérica de alto desempenho
- **biopython** — Bioinformática (sequências, parsing)
- **sqlalchemy** — ORM para banco de dados

### Análise Genômica
- **pyvcf** — Parsing de arquivos VCF
- **requests** — Integração com APIs

### Visualização & Relatórios
- **streamlit** — Dashboard web interativo
- **plotly** — Gráficos interativos
- **matplotlib, seaborn** — Visualizações estatísticas
- **reportlab** — Geração de PDFs

### Testes & Qualidade
- **pytest** — Framework de testes
- **black** — Formatação de código
- **flake8** — Linting
- **mypy** — Type checking

---

## ⚡ Quick Start

### Pré-requisitos
- Python 3.14
- Git
- pip
- Docker

### Instalação

#### Opção 1: Execução local

```bash
# 1. Clonar o repositório
git clone https://github.com/carla-bioinfo/crispr-mmr-explorer.git
cd crispr-mmr-explorer

# 2. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar o dashboard
python -m src
```

#### Opção 2: Via Docker

```bash
# 1. Build da imagem
docker build -t crispr-mmr-explorer .

# 2. Executar o container
docker run --rm -p 8501:8501 crispr-mmr-explorer
```

Depois, acesse o Streamlit em http://localhost:8501.

---

## 📚 Documentação

- **[INSTALLATION.md](docs/INSTALLATION.md)** — Guia de instalação
- **[USAGE.md](docs/USAGE.md)** — Como usar
- **[docs/scientific/](docs/scientific/)** — Documentação científica
- **[docs/development/](docs/development/)** — Documentação técnica

---

## 🔬 Dados Utilizados

Este projeto utiliza **dados públicos desidentificados**:

| Fonte | Descrição |
|-------|-----------|
| **ClinVar** | Variantes clínicas | https://www.ncbi.nlm.nih.gov/clinvar/ |
| **InSiGHT** | Variantes MMR | http://insight.insightgroup.org/ |
| **Ensembl** | Anotações genômicas | https://www.ensembl.org/ |

---

## 🧪 Testes

```bash
# Executar testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html
```

**Meta**: Cobertura ≥ 80%

---

## 📊 10 Fases de Desenvolvimento

| Fase | Objetivo | Status |
|------|----------|--------|
| 1 | Fundamentos Biológicos | 🔵 Planejado |
| 2 | Coleta de Dados | 🔵 Planejado |
| 3 | Pré-processamento | 🔵 Planejado |
| 4 | Banco de Variantes | 🔵 Planejado |
| 5 | Módulo Analítico | 🔵 Planejado |
| 6 | Visualizações | 🔵 Planejado |
| 7 | Módulo CRISPR | 🔵 Planejado |
| 8 | Relatórios PDF | 🔵 Planejado |
| 9 | Testes Automatizados | 🔵 Planejado |
| 10 | Documentação | 🔵 Planejado |

**Tempo**: 20-26 semanas

---

## 🚀 Roadmap

### Curto Prazo (Próximas 4 semanas)
- [ ] Fase 1: Fundamentos científicos
- [ ] Fase 2: Coleta de dados
- [ ] Estruturar Git

### Médio Prazo (Próximos 3 meses)
- [ ] Fases 2-6 completas
- [ ] Dashboard com 5+ visualizações
- [ ] Deploy em Streamlit Cloud

### Longo Prazo (Próximos 6 meses)
- [ ] Todas as 10 fases
- [ ] Testes ≥ 80%
- [ ] Publicação em conferência

---

## 🤝 Contribuindo

Feedback e sugestões são bem-vindos!

---

## 📄 Referências Científicas

- Lynch, H. T., et al. (2015). "Hereditary nonpolyposis colorectal cancer". *Nature Reviews Disease Primers*, 1, 15051.
- Richards, S., et al. (2015). "Standards and guidelines for interpretation of sequence variants". *Nature Biotechnology*, 37(4), 405–413.
- InSiGHT Database: http://insight.insightgroup.org/

---

## 🔐 Segurança & Privacidade

- ✅ Nenhum dado de pacientes
- ✅ Dados públicos desidentificados
- ✅ Validação rigorosa de entrada
- ✅ Proteção contra SQL injection
- ✅ Variáveis de ambiente para dados sensíveis

---

## 📞 Contato

**Autor**: Carla Rodriguês de Moraes  
**Email**: carlabio.biomol@gmail.com  
**GitHub**: https://github.com/carla-bioinfo

---

## 📜 Licença

MIT License. Veja [LICENSE](LICENSE) para detalhes.

---

## ⭐ Se Gostou, Deixe uma Estrela!

Se este projeto foi útil, considere deixar uma ⭐ no GitHub!

---

**Status**: 🟡 Em Desenvolvimento  
**Última Atualização**: Junho 2026  
**Versão**: 0.1.0-alpha

