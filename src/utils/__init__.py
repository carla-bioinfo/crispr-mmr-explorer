"""
Módulo utils - Utilities do CRISPR-MMR Explorer
===============================================

Exporta logger e exceptions para fácil importação:

    from src.utils import get_logger, VariantValidationError
"""

from src.utils.logger import get_logger, setup_logging
from src.utils.exceptions import (
    CRISPRMMRException,
    VariantValidationError,
    ACMGClassificationError,
    DatabaseError,
    FileProcessingError
)

__all__ = [
    "get_logger",
    "setup_logging",
    "CRISPRMMRException",
    "VariantValidationError",
    "ACMGClassificationError",
    "DatabaseError",
    "FileProcessingError"
]
