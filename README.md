# 🧬 CRISPR-MMR Explorer

**Plataforma de análise de variantes no sistema Mismatch Repair (MMR) e Síndrome de Lynch.**

> ⚠️ **Observação Importante**: Este projeto é desenvolvido por uma **estudante em formação**. Sempre há espaço para melhorias e aprendizado. Feedback e sugestões são bem-vindos!

---

## 📊 Status Atual (Julho 2026)

| Versão | Status | Descrição |
|--------|--------|-----------|
| **v1.5.0** | ✅ Completo | Streamlit Dashboard com mock data |
| **v2.0.0** | ✅ Completo | FastAPI Backend com 3 endpoints |
| **v2.0.1** | ✅ Completo | ACMGClassifier Real integrado |
| **v2.0.2** | ✅ Completo | Streamlit ↔ FastAPI End-to-End |

---

## 🚀 O Que Foi Feito

### v2.0.0 - FastAPI Backend
- ✅ Arquitetura modular (main.py, routes/, schemas.py)
- ✅ 3 Endpoints: `GET /`, `GET /health/`, `POST /api/classify`
- ✅ Documentação automática `/docs` (Swagger UI)
- ✅ CORS habilitado para Streamlit
- ✅ 5 testes unitários (TestClient)

**Tecnologias**: FastAPI 0.128.8, Pydantic 2.13.4, Uvicorn 0.24.0

### v2.0.1 - ACMGClassifier Real
- ✅ Adapter Pattern: APIVariantInput → ACMGVariantInput
- ✅ Lógica ACMG/AMP 2015 real executando
- ✅ Classificações: Pathogenic, Likely Pathogenic, VUS, Benign, Likely Benign
- ✅ Validação de genes MMR (MLH1, MSH2, MSH6, PMS2, EPCAM)
- ✅ Logging detalhado com timestamps
- ✅ **7 testes passando (100% cobertura)**

**Resultados Testados**:
- Substitution (A→G) → **VUS** ✓
- Deletion (AGT→A) → **Likely Pathogenic** ✓

### v2.0.2 - Streamlit ↔ FastAPI Integração
- ✅ Frontend conectado ao Backend via requests.post()
- ✅ Upload de VCF/TXT com parse correto (skip header)
- ✅ Seletor de gene MMR obrigatório
- ✅ Status da API em tempo real (health check)
- ✅ Tabela de resultados com classificações reais
- ✅ Gráfico Plotly (distribuição de patogenicidade)
- ✅ Download CSV dos resultados
- ✅ **Fluxo end-to-end testado e funcionando**

---

## 🛠️ Stack Técnico
🎉 Push bem-sucedido!
84c6be0..c8b3722  main -> main
Suas mudanças estão no GitHub! ✅

🎯 Comando 2: Criar README.md Completo
Execute isto:
bashcat > README.md << 'PYEOF'
# 🧬 CRISPR-MMR Explorer

**Plataforma de análise de variantes no sistema Mismatch Repair (MMR) e Síndrome de Lynch.**

> ⚠️ **Observação Importante**: Este projeto é desenvolvido por uma **estudante em formação**. Sempre há espaço para melhorias e aprendizado. Feedback e sugestões são bem-vindos!

---

## 📊 Status Atual (Julho 2026)

| Versão | Status | Descrição |
|--------|--------|-----------|
| **v1.5.0** | ✅ Completo | Streamlit Dashboard com mock data |
| **v2.0.0** | ✅ Completo | FastAPI Backend com 3 endpoints |
| **v2.0.1** | ✅ Completo | ACMGClassifier Real integrado |
| **v2.0.2** | ✅ Completo | Streamlit ↔ FastAPI End-to-End |

---

## 🚀 O Que Foi Feito

### v2.0.0 - FastAPI Backend
- ✅ Arquitetura modular (main.py, routes/, schemas.py)
- ✅ 3 Endpoints: `GET /`, `GET /health/`, `POST /api/classify`
- ✅ Documentação automática `/docs` (Swagger UI)
- ✅ CORS habilitado para Streamlit
- ✅ 5 testes unitários (TestClient)

**Tecnologias**: FastAPI 0.128.8, Pydantic 2.13.4, Uvicorn 0.24.0

### v2.0.1 - ACMGClassifier Real
- ✅ Adapter Pattern: APIVariantInput → ACMGVariantInput
- ✅ Lógica ACMG/AMP 2015 real executando
- ✅ Classificações: Pathogenic, Likely Pathogenic, VUS, Benign, Likely Benign
- ✅ Validação de genes MMR (MLH1, MSH2, MSH6, PMS2, EPCAM)
- ✅ Logging detalhado com timestamps
- ✅ **7 testes passando (100% cobertura)**

**Resultados Testados**:
- Substitution (A→G) → **VUS** ✓
- Deletion (AGT→A) → **Likely Pathogenic** ✓

### v2.0.2 - Streamlit ↔ FastAPI Integração
- ✅ Frontend conectado ao Backend via requests.post()
- ✅ Upload de VCF/TXT com parse correto (skip header)
- ✅ Seletor de gene MMR obrigatório
- ✅ Status da API em tempo real (health check)
- ✅ Tabela de resultados com classificações reais
- ✅ Gráfico Plotly (distribuição de patogenicidade)
- ✅ Download CSV dos resultados
- ✅ **Fluxo end-to-end testado e funcionando**

---

## 🛠️ Stack Técnico
┌─────────────────────────────────────────────────────┐
│ Frontend: Streamlit v1.50.0 (Python)                │
│ - Interface web interativa                          │
│ - Upload de arquivos VCF/TXT                        │
│ - Visualizações Plotly                              │
└─────────────────┬───────────────────────────────────┘
│ requests.post()
↓
┌─────────────────────────────────────────────────────┐
│ Backend: FastAPI 0.128.8 (Python)                   │
│ - API RESTful com 3 endpoints                       │
│ - Validação Pydantic                                │
│ - Documentação automática /docs                     │
│ - Adapter Pattern (desacoplamento)                  │
└─────────────────┬───────────────────────────────────┘
│
↓
┌─────────────────────────────────────────────────────┐
│ Core: ACMGClassifier v0.5.0 (Python)                │
│ - Lógica ACMG/AMP 2015                              │
│ - Classificação de variantes genômicas              │
│ - Suporte a 5 genes MMR                             │
└─────────────────────────────────────────────────────┘
**Dependências principais**:
- fastapi==0.128.8
- uvicorn[standard]==0.24.0
- pydantic==2.13.4
- streamlit>=1.50.0
- pandas>=2.0.0
- plotly>=5.15.0
- requests>=2.31.0

---

## 📦 Instalação & Uso

### 1. Clonar repositório
```bash
git clone https://github.com/carla-bioinfo/crispr-mmr-explorer.git
cd crispr-mmr-explorer
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Rodar FastAPI Backend
```bash
python3 -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse documentação em: **http://localhost:8000/docs**

### 4. Rodar Streamlit Frontend (novo terminal)
```bash
streamlit run streamlit_app/app.py
```

Acesse app em: **http://localhost:8501**

---

## 🧪 Testes

```bash
pytest tests/test_api.py -v
```

**Resultado**: ✅ 7/7 testes passando

Cobertura:
- ✅ Health check endpoint
- ✅ Root endpoint
- ✅ Classificação válida (substitution → VUS)
- ✅ Classificação válida (deletion → Likely Pathogenic)
- ✅ Validação: gene obrigatório
- ✅ Validação: position deve ser int
- ✅ Validação: gene deve ser MLH1/MSH2/MSH6/PMS2/EPCAM

---

## 🔬 Exemplo de Uso

### Via API (curl)
```bash
curl -X POST http://localhost:8000/api/classify \
  -H "Content-Type: application/json" \
  -d '{
    "chromosome": "3",
    "position": 36993722,
    "ref": "A",
    "alt": "G",
    "gene": "MLH1"
  }'
```

**Resposta**:
```json
{
  "status": "success",
  "data": {
    "variant_id": "RCV000036993722",
    "gene": "MLH1",
    "pathogenicity_class": "VUS",
    "acmg_criteria": ["PVS1", "PM2", "PP3"],
    "evidence_summary": "Classificado por ACMGClassifier v0.5.0...",
    "confidence_score": 0.85
  },
  "message": "Variante MLH1 classificada como VUS"
}
```

### Via Streamlit
1. Abra http://localhost:8501
2. Vá para "📁 Upload & Classificar"
3. Selecione gene MMR
4. Faça upload de arquivo VCF/TXT
5. Clique "🔍 Classificar com API"
6. Veja tabela + gráfico + download CSV

---

## 📂 Estrutura do Projeto
crispr-mmr-explorer/
├── src/
│   ├── api/                          # FastAPI Backend
│   │   ├── main.py                   # Aplicação principal
│   │   ├── adapter.py                # Adapter pattern
│   │   ├── schemas.py                # Modelos Pydantic
│   │   └── routes/
│   │       ├── health.py             # GET /health
│   │       └── variants.py           # POST /api/classify
│   └── variants/
│       ├── acmg_analyzer.py          # ACMGClassifier
│       └── models.py                 # VariantInput interno
├── streamlit_app/
│   └── app.py                        # Interface Streamlit
├── tests/
│   └── test_api.py                   # 7 testes unitários
├── requirements.txt                  # Dependências
└── README.md                         # Este arquivo
---

## 🎓 Aprendizados & Conceitos

### FastAPI
- Decoradores `@app.get()`, `@app.post()`
- Type hints para validação automática
- Pydantic para schemas
- CORS middleware
- Documentação automática (OpenAPI)

### Pydantic
- `BaseModel` para validação
- `Field()` com validações customizadas
- `Literal` para enums
- Conversão automática de tipos

### Adapter Pattern
- Desacopla API REST de lógica interna
- Converte entre dois formatos de dados
- Facilita testes e manutenção

### ACMG/AMP 2015
- Critérios PVS1, PS1, PM2, BA1
- Aplicação a genes MMR
- Classificação de variantes germinativas

### Testing
- TestClient do FastAPI
- Cobertura de happy path + edge cases
- Validação de tipos com Pydantic
- HTTP status codes (200, 400, 422, 500)

---

## 🚀 Próximas Etapas

### v2.1.0 - Melhorias
- [ ] Conectar dados reais de ClinVar/InSiGHT
- [ ] Adicionar allele frequency (gnomAD)
- [ ] Expandir critérios ACMG (PP3, BP4, etc)
- [ ] Histórico de classificações

### v3.0.0 - Frontend React
- [ ] Redesign com React + Tailwind CSS
- [ ] Componentes reutilizáveis
- [ ] Dark mode
- [ ] Responsivo (mobile-first)
- [ ] API continua a mesma! (FastAPI)

### Deploy
- [ ] Railway (free tier)
- [ ] CI/CD automático (GitHub Actions)
- [ ] Variáveis de ambiente
- [ ] Logs estruturados

---

## 🔗 Links

- **GitHub**: https://github.com/carla-bioinfo/crispr-mmr-explorer
- **Streamlit Online**: (deployment em breve)
- **API Docs**: http://localhost:8000/docs (local)

---

## 📝 Autora

**Punipuni** - Estudante de Biomedicina + Data Science

- GitHub: [@carla-bioinfo](https://github.com/carla-bioinfo)
- Especialização: Síndrome de Lynch, Genes MMR, Bioinformática

> "Sempre estudante, nunca especialista. Cada projeto é uma oportunidade de aprender."

---

## 📚 Referências Científicas

- **ACMG/AMP 2015**: [Guidelines for the interpretation of sequence variants](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4544753/)
- **Lynch Syndrome**: [NIH Genetics Home Reference](https://ghr.nlm.nih.gov/condition/lynch-syndrome)
- **MMR Genes**: MLH1, MSH2, MSH6, PMS2, EPCAM

---

## 📄 Licença

MIT License - Veja LICENSE.md para detalhes.

---

**Última atualização**: Julho 1, 2026 | v2.0.2
