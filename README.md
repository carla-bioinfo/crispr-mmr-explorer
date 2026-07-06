# CRISPR-MMR Explorer v2.0.2

> **⚠️ Projeto Acadêmico de Aprendizagem**  
> Desenvolvido como estudante de Biomedicina + Data Science para consolidar conhecimentos em bioinformática clínica, APIs REST e CI/CD.

**Status:** ✅ LIVE em Produção (Railway) — [Teste Aqui](https://crispr-mmr-explorer-production.up.railway.app/health)

---

## 🎓 O Projeto (Perspectiva de Aprendizado)

Este projeto nasceu de uma pergunta: **"Como posso integrar classificação ACMG/AMP 2015 com uma API moderna e deployá-la em produção?"**

**Objetivo de Aprendizagem:**
- ✅ Implementar classificação de variantes genéticas (ACMG/AMP 2015)
- ✅ Construir API REST com FastAPI (framework moderno)
- ✅ Aprender CI/CD (GitHub → Railway webhook)
- ✅ Debugging em produção (problema real: $PORT não expandia)
- ✅ Documentação técnica profissional
- ✅ Testes unitários (TDD mindset)

**Resultado:** API funcional classificando variantes MLH1 em tempo real.

---

## 🚀 Como Testar (Reproduzir Meu Aprendizado)

### Teste em Produção (Nenhuma Instalação)

```bash
curl -X POST https://crispr-mmr-explorer-production.up.railway.app/api/classify \
  -H "Content-Type: application/json" \
  -d '{
    "chromosome": "3",
    "position": 36993722,
    "ref": "A",
    "alt": "G",
    "gene": "MLH1"
  }'
```

**Resposta (Status 200):**
```json
{
  "status": "success",
  "data": {
    "variant_id": "RCV036993722",
    "gene": "MLH1",
    "pathogenicity_class": "VUS",
    "acmg_criteria": ["PVS1", "PM2", "PP3"],
    "confidence_score": 0.85
  },
  "message": "Variante MLH1 classificada como VUS"
}
```

### Rodar Localmente

```bash
git clone https://github.com/carla-bioinfo/crispr-mmr-explorer.git
cd crispr-mmr-explorer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn src.api.main:app --reload --port 8000
```

Acesse Swagger UI: `http://127.0.0.1:8000/docs`

---

## 🧬 O Que Faz (Explicação Técnica)

O projeto classifica variantes genéticas (especialmente em genes MMR: MLH1, MSH2, MSH6, PMS2, EPCAM) usando critérios ACMG/AMP 2015.

**Fluxo Simplificado:**
[Entrada: Variante genética]
↓
[ACMGClassifier avalia critérios]
├─ PVS1: É um frameshift que para tradução?
├─ PM2: É frequência alélica rara (<0.001)?
├─ PP3: Modelos in silico predizem deletério?
└─ BP4, BM4: Contra-evidências de patogenicidade
↓
[Agregação de score]
↓
[Saída: PATHOGENIC | LIKELY_PATHOGENIC | VUS | LIKELY_BENIGN | BENIGN]
**Dados:** Atualmente usando **mock data** (synthetic). FASE 4 integrará ClinVar real.

---

## 📚 Stack Técnico (O Que Aprendi a Usar)

| Aspecto | Tecnologia | Por Que? |
|---------|-----------|---------|
| **Language** | Python 3.11 | Popular em bioinformática + DS |
| **Web Framework** | FastAPI | Moderno, async, auto-docs Swagger |
| **Validation** | Pydantic | Type hints + validação automática |
| **Container** | Docker | Reprodutibilidade + deployment |
| **Deploy** | Railway | Simples, free tier, GitHub integration |
| **Testing** | pytest | Padrão de ouro em Python |
| **Logging** | structlog | Logs estruturados para auditoria |

---

## 🔧 Lições Aprendidas (Debugging Journey)

### Problema 1: `$PORT` não expandia em produção

**Sintoma:**
Error: Invalid value for '--port': '$PORT' is not a valid integer
**Root Cause:**
Railway `startCommand` (exec form) não expande variáveis de ambiente:
```dockerfile
# ❌ ERRADO: Exec form (não expande $PORT)
CMD ["uvicorn", "...", "--port", "$PORT"]

# ✅ CORRETO: Shell form (expande via /bin/sh -c)
CMD uvicorn ... --port ${PORT:-8000}
```

**Lição:** Exec form vs Shell form não é óbvio. Levei tempo debugando.

### Problema 2: `startCommand` vs `CMD` Conflito

**Sintoma:** Dockerfile estava correto, mas Railway ignorava e usava startCommand antigo.

**Solução:** Remover `startCommand` do `railway.json` e deixar Dockerfile ser a "fonte de verdade".

**Lição:** Em CI/CD, sempre há camadas de configuração conflitantes. Precisa mapear todas.

### Problema 3: Projeto Corrompido no Cache

**Sintoma:** Mesmo após fix, Railway retornava 404.

**Solução:** Deletar projeto Railway inteiro e reconstruir do zero.

**Lição:** Às vezes refazer é mais rápido que debugar. Decisão estratégica!

---

## 📊 Status Atual

| Fase | Status | Notas |
|------|--------|-------|
| **v2.0.2 (Agora)** | ✅ LIVE | API funciona, Dockerfile correto, Railway happy |
| **FASE 4 (Próximo)** | 🚧 Iniciando | Integrar ClinVar real + gnomAD v4 |
| **FASE 5** | ⏳ TODO | LinkedIn portfolio + Streamlit UI |
| **FASE 6** | ⏳ TODO | React frontend (melhor que Streamlit) |

---

## 🧬 Contexto Bioinformático (O Que Estou Aprendendo)

**Síndrome de Lynch:**
- Câncer colorretal hereditário (~5% de todos CCR)
- Causada por variantes germinativas em genes MMR
- Risco de vida de CCR: até 70% (vs ~5% pop geral)

**Genes MMR Focados:**
- **MLH1** (~70% variantes Lynch) ← Mais estudado
- **MSH2** (~20%)
- **MSH6** (~7%)
- **PMS2** (~3%)
- **EPCAM** (~1%)

**ACMG/AMP 2015:**
- Guia padrão para classificação de variantes
- Baseada em agregação de evidências (critérios PVS1, PM1, etc)
- Produz 5 categorias finais (PATHOGENIC → BENIGN)

---

## 🔐 Segurança (Aprendizagem em Progresso)

✅ **Implementado:**
- Pydantic validation (não aceita lixo)
- Sem credenciais em código (env vars)
- Logs estruturados (auditoria)

⚠️ **Precisa Melhorar:**
- Rate limiting (FASE 5)
- CORS (se frontend será externo)
- Input sanitization mais rigorosa

---

## 🎓 Como Reproduzir Este Projeto

Se você está aprendendo também, pode:

1. **Clonar o repo**
2. **Debugar localmente** (quebra, arruma, aprende)
3. **Estudar Dockerfile** (shell form vs exec)
4. **Entender ACMG** (genomics + code)
5. **Deploy no Railway** (CI/CD prático)

Cada etapa tem challenge. Isso é aprendizagem real!

---

## 📖 Referências que Consulto

- ACMG/AMP 2015 Standards (interpretação de variantes)
- ClinGen InSiGHT (critérios gene-específicos MMR)
- FastAPI Docs (web development)
- Python Best Practices (Clean Code)

*(Nenhuma dessas foi inventada — são reais e consultáveis)*

---

## 🤝 Próximas Etapas de Aprendizagem

1. **FASE 4:** Integrar APIs reais (ClinVar, gnomAD)
2. **Aprender:** REST API design patterns
3. **Aprender:** Data fetching + caching
4. **Aprender:** Versionamento de modelos

---

## 📝 Notas Pessoais (Estudante)

Este projeto consolidou:
- ✅ FastAPI + Pydantic (gosto!)
- ✅ Docker fundamentals
- ✅ CI/CD troubleshooting (resilience!)
- ✅ Bioinformática aplicada
- ✅ Debugging metodológico

Próximo desafio: Integrar dados reais sem degradar performance.

---

**Última atualização:** 5 de Julho, 2026  
**Desenvolvido por:** Carla (Estudante de Biomedicina + Data Science)  
**Status:** Learning & Building 🚀
