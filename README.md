# 🧬 CRISPR-MMR Explorer v2.0.2

**Classificador ACMG/AMP 2015 para variantes germinativas do sistema Mismatch Repair**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-19+-blue.svg)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Tailwind](https://img.shields.io/badge/Tailwind-v4-06B6D4.svg)](https://tailwindcss.com/)

## 📋 Sobre

CRISPR-MMR Explorer é uma ferramenta web full-stack para **classificação clínica de variantes** no sistema Mismatch Repair (MLH1, MSH2, MSH6, PMS2, EPCAM) usando critérios ACMG/AMP 2015.

## 🏗️ Arquitetura
Frontend (React 19 + Vite + Tailwind v4)
↓ POST /api/classify
Backend (FastAPI Python)
↓ ACMG Calculation
Frontend renderiza resultado
## 🚀 Quick Start

### Backend
```bash
cd ~/crispr-mmr-explorer
source venv/bin/activate
cd src
python -m uvicorn api.main:app --reload --port 8000
```

### Frontend
```bash
cd ~/crispr-mmr-explorer/frontend
nvm use 20
npm run dev
```

Acesse: **http://localhost:5174**

## 📊 FASE 6 - Frontend Completo ✅

✅ Interface dark theme profissional  
✅ Formulário responsivo (gene, cromossomo, posição, ref/alt, freq)  
✅ Classificação ACMG em tempo real  
✅ Tailwind CSS v4 integrado  
✅ Axios + FastAPI integração  
✅ 7/7 testes backend passando  

## 🛠️ Stack

- **Frontend:** React 19 | Vite | Tailwind CSS v4 | Axios | Recharts
- **Backend:** FastAPI | Pydantic | Python 3.9
- **DevTools:** Node v20 | npm 10 | Git | nvm

## 📁 Estrutura
crispr-mmr-explorer/
├── frontend/          # React + Vite
│   ├── src/
│   │   ├── App.jsx
│   │   ├── VariantForm.jsx
│   │   └── ResultDisplay.jsx
│   └── package.json
├── src/               # FastAPI Backend
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   └── tests/
└── README.md
## 🔄 Fluxo

1. Usuário preenche formulário
2. Frontend envia POST → `/api/classify`
3. Backend calcula ACMG (PVS1, PM2, PP3, BP4)
4. Frontend renderiza resultado com classificação

## 📈 Status

| Fase | Status | Descrição |
|------|--------|-----------|
| 1-5 | ✅ | Backend + Testes |
| **6** | **✅** | **Frontend React + Tailwind** |
| 7+ | ⏳ | Gráficos + Export + Deploy |

## 👨‍💻 Autor

**Carla Rodrigues** (@carla-bioinfo)

Especialista em Bioinformática | Lynch Syndrome & MMR Genes | Building in Public

---

**Última atualização:** Julho 2026 | FASE 6 Completa
