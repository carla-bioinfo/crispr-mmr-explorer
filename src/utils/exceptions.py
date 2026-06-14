"""
Custom Exceptions para CRISPR-MMR Explorer
===========================================

Define exceções específicas do projeto para tratamento de erros.
"""

class CRISPRMMRException(Exception):
    """Exceção base para o projeto."""
    pass


class VariantValidationError(CRISPRMMRException):
    """Erro ao validar uma variante."""
    pass


class ACMGClassificationError(CRISPRMMRException):
    """Erro ao classificar uma variante com ACMG."""
    pass


class DatabaseError(CRISPRMMRException):
    """Erro ao acessar o banco de dados."""
    pass


class FileProcessingError(CRISPRMMRException):
    """Erro ao processar arquivo CSV."""
    pass


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧬 TESTANDO CUSTOM EXCEPTIONS")
    print("="*80 + "\n")
    
    # Teste 1: Lançar exceção
    try:
        raise VariantValidationError("Gene inválido: XYZ123")
    except VariantValidationError as e:
        print(f"✅ Exceção capturada: {e}")
    
    # Teste 2: Lançar outra
    try:
        raise ACMGClassificationError("Frequência alélica inválida")
    except ACMGClassificationError as e:
        print(f"✅ Exceção capturada: {e}")
    
    print("\n" + "="*80)
    print("✅ Teste concluído!")
    print("="*80 + "\n")
