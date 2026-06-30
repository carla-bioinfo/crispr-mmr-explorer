# Changelog

Todas as mudanças notáveis neste projeto estão documentadas neste arquivo.

## [1.0.0] - 2026-06-30

### ✨ Added
- GitHub Actions CI/CD com testes automáticos a cada push
- Badge de status dos testes no README
- Coverage check automático (≥80%)
- Pydantic V2 migration completa (Etapa 0.7)
- Refatoração de __main__ para função testável (Etapa 0.8)

### 🔧 Changed
- Todos os @validator → @field_validator (Pydantic V2)
- Padrão ConfigDict para configuração de modelos
- Estrutura de testes reorganizada

### 🐛 Fixed
- Zero warnings Pydantic
- Coverage aumentada de 86% → 94%
- Tratamento de erros robusto em todos os módulos

### 📊 Metrics
- **Coverage**: 94% ✅
- **Tests**: 43/43 passando ✅
- **Python**: 3.9
- **Status**: Production Ready ✅

---

## [0.5.0] - 2026-06-17

### ✨ Added
- ACMG/AMP 2015 Variant Classifier
- Pydantic validation models
- Logging e exception handling
- Code coverage tracking

### 📝 Notes
Para histórico completo de versões anteriores, veja as tags no GitHub.
