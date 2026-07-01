# 📝 CHANGELOG - CRISPR-MMR Explorer

> **Nota**: Documentado por uma **estudante em formação**. Sempre há espaço para melhorias.

---

## [2.0.2] - 2026-07-01

### ✅ Streamlit ↔ FastAPI Integration Completo

**O que foi feito:**
- Conectou Streamlit frontend à FastAPI backend via `requests.post()`
- Upload de VCF/TXT com parse correto (skip header)
- Seletor de gene MMR obrigatório no sidebar
- Status da API em tempo real (health check visual)
- Cada variante faz POST individual para `/api/classify`
- Tabela de resultados com classificações reais (CHR, POS, REF, ALT, Classificação, Critérios ACMG, Score)
- Gráfico Plotly mostrando distribuição de patogenicidade
- Botão "💾 Download Resultados (CSV)"

**Fluxo End-to-End Testado:**
Upload VCF → Parse (skip header) → POST /api/classify
↓
ACMGClassifier classifica
↓
Substitution (A→G) → VUS ✓
Deletion (AGT→A) → Likely Pathogenic ✓
↓
Resultados em tabela + gráfico + CSV
**Arquivos Modificados:**
- `streamlit_app/app.py` - Integração com API (requests.post, try/except, progress bar)
- `requirements.txt` - Adicionado requests>=2.31.0

**Observação Importante:**
- Nesta versão, o arquivo VCF deve ter **cabeçalho** (CHR POS REF ALT)
- O código pula a linha de cabeçalho automaticamente com `lines[1:100]`

---

## [2.0.1] - 2026-07-01

### ✅ ACMGClassifier Real Integrado

**O que foi feito:**
- Importou `ACMGClassifier` real de `src/variants/acmg_analyzer.py`
- Implementou Adapter Pattern: `APIVariantInput` → `ACMGVariantInput`
- Adapter converte dados HTTP para formato interno (clinvar_id, HGVS, tipo)
- Determina tipo automaticamente baseado em tamanho de ref/alt (deletion/insertion/substitution)
- ACMGClassifier executa lógica ACMG/AMP 2015 real
- Logging detalhado em cada passo (auditoria)
- Validação Pydantic com `Literal['MLH1', 'MSH2', 'MSH6', 'PMS2', 'EPCAM']`

**Resultados Reais Testados:**
Variante 1: chr3:36993722:A:G (Substitution em MLH1)

Tipo: substitution
Critérios ativados: PM2 (raro)
Resultado: VUS (sem critérios fortes) ✓

Variante 2: chr3:36993722:AGT:A (Deletion em MLH1)

Tipo: deletion (len(ref) > len(alt))
Critérios ativados: PVS1 (null variant)
Resultado: Likely Pathogenic ✓
**Testes: 7/7 Passando** (100% cobertura)
- `test_health_check` - GET /health/
- `test_root_endpoint` - GET /
- `test_classify_substitution_returns_vus` - Substitution → VUS
- `test_classify_deletion_returns_likely_pathogenic` - Deletion → Likely Pathogenic
- `test_classify_missing_gene` - Validação: gene obrigatório (HTTP 422)
- `test_classify_invalid_position` - Validação: position int (HTTP 422)
- `test_classify_invalid_gene` - Validação: gene MMR only (HTTP 422)

**Arquivos Criados/Modificados:**
- `src/api/adapter.py` - Novo (Adapter Pattern)
- `src/api/routes/variants.py` - Modificado (usa ACMGClassifier real)
- `src/api/schemas.py` - Modificado (validação Literal de genes)
- `tests/test_api.py` - Modificado (7 testes, happy path + edge cases)

---

## [2.0.0] - 2026-07-01

### ✅ FastAPI Backend com Endpoints RESTful

**O que foi feito:**
- Arquitetura modular: `main.py` + `routes/` + `schemas.py`
- 3 Endpoints implementados:
  - `GET /` - Root endpoint (lista endpoints disponíveis)
  - `GET /health/` - Health check (status da API)
  - `POST /api/classify` - Classificação de variantes (mock data)

**Documentação Automática:**
- `/docs` - Swagger UI (gerado automaticamente por FastAPI)
- `/redoc` - ReDoc (documentação alternativa)
- `/openapi.json` - Especificação OpenAPI (máquina-legível)

**Features:**
- CORS middleware (permite Streamlit fazer requests)
- Pydantic schemas com validação automática
- HTTP status codes corretos (200, 400, 422, 500)
- TestClient para testes sem rodar servidor real

**Testes: 5/7 Passando**
- `test_health_check` - Health endpoint
- `test_root_endpoint` - Root endpoint
- `test_classify_valid_variant` - Dados válidos (mock)
- `test_classify_missing_gene` - Validação obrigatória
- `test_classify_invalid_position` - Type validation

**Arquivos Criados:**
- `src/api/main.py` - Aplicação FastAPI
- `src/api/routes/health.py` - Health check endpoint
- `src/api/routes/variants.py` - Classificação endpoint (v1: mock)
- `src/api/schemas.py` - Modelos Pydantic
- `tests/test_api.py` - Testes unitários

---

## [1.5.0] - 2026-06-30

### ✅ Streamlit Dashboard v1.5.0 COMPLETO

**Versão anterior** (não modificada nesta sessão):
- Dashboard interativo com 4 páginas
- Upload de VCF/TXT com mock classification
- Gráficos Plotly
- Mock data (sem conexão com API)

---

## 📊 Métricas Atuais

| Métrica | Valor |
|---------|-------|
| **Total de Commits** | 5 (v2.0.0, v2.0.1, v2.0.2 + README + merge) |
| **Testes Passando** | 7/7 (100%) |
| **Cobertura de Testes** | Happy path + edge cases (validação, tipos) |
| **Endpoints** | 3 (/, /health/, /api/classify) |
| **Genes MMR Suportados** | 5 (MLH1, MSH2, MSH6, PMS2, EPCAM) |
| **Linhas de Código** | ~1500 (API + Streamlit + testes) |

---

## 🚀 Próximas Etapas Recomendadas

### v2.1.0 - Backend Melhorias
- [ ] Conectar ClinVar real (em vez de clinvar_id mock)
- [ ] Adicionar allele frequency (gnomAD)
- [ ] Expandir critérios ACMG (PP3, BP4, etc)
- [ ] Histórico de classificações (banco de dados)

### v3.0.0 - Frontend React
- [ ] Redesign com React + Tailwind CSS
- [ ] Componentes reutilizáveis
- [ ] Dark mode nativo
- [ ] Responsivo (mobile-first)
- [ ] FastAPI continua inalterado! (desacoplamento)

### Deploy
- [ ] Railway (free tier) - FastAPI + Streamlit
- [ ] CI/CD automático (GitHub Actions)
- [ ] Variáveis de ambiente (.env)
- [ ] Logs estruturados (JSON)

---

## 🎓 Conceitos Aprendidos Nesta Sessão

### Architecture & Design Patterns
- **Separation of Concerns**: API (FastAPI) desacoplada de Interface (Streamlit)
- **Adapter Pattern**: `APIVariantInput` → `ACMGVariantInput`
- **RESTful Principles**: HTTP methods, status codes, JSON responses
- **Type Safety**: Pydantic para validação automática

### FastAPI
- Decoradores `@app.get()`, `@app.post()`
- Type hints → validação automática
- CORS middleware
- Documentação automática (OpenAPI/Swagger)
- TestClient para testes sem servidor

### Pydantic
- `BaseModel` para schemas
- `Field()` com validações
- `Literal` para enums
- Conversão automática de tipos
- Error handling (HTTP 422)

### Testing
- TestClient do Starlette
- Cobertura: happy path + edge cases
- Validação de tipos
- HTTP status codes

### Bioinformatics (ACMG/AMP 2015)
- Critérios PVS1, PS1, PM2, BA1
- Aplicação a genes MMR
- Tipos de variantes (deletion/insertion/substitution)
- Classificação de variantes germinativas

---

## ⚠️ Observações Importantes

### Sempre Estudante, Nunca Especialista
- Este projeto foi desenvolvido durante processo de aprendizado
- Código pode não ser perfeito — é iterativo
- Feedback e melhorias são bem-vindos
- Foco em aprender **padrões profissionais**, não apenas "fazer funcionar"

### Limitações Atuais
1. **Dados Mock**: clinvar_id e HGVS são gerados, não reais
2. **Allele Frequency**: Não integrado (gnomAD)
3. **Critérios ACMG**: Subset básico (PVS1, PS1, PM2, BA1)
4. **Interface**: Streamlit é rápido mas não é production UI
5. **Deploy**: Ainda local (Railway será próximo passo)

### Como Contribuir / Melhorar
1. Abra issues no GitHub
2. Sugira refatorações
3. Adicione dados reais (ClinVar, InSiGHT)
4. Implemente frontend React

---

## 🔗 Links Úteis

- **GitHub**: https://github.com/carla-bioinfo/crispr-mmr-explorer
- **ACMG/AMP 2015**: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4544753/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pydantic**: https://docs.pydantic.dev/

---

**Última atualização**: Julho 1, 2026 | v2.0.2

Desenvolvido com ❤️ por uma estudante em bioinformática.
