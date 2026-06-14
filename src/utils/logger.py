"""
Sistema de Logging para CRISPR-MMR Explorer
"""

import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logging(log_dir="logs", log_level="INFO"):
    """Configura o sistema de logging do projeto."""
    Path(log_dir).mkdir(exist_ok=True)
    log_filename = f"crispr_mmr_{datetime.now().strftime('%Y%m%d')}.log"
    log_filepath = os.path.join(log_dir, log_filename)
    logger = logging.getLogger("CRISPR_MMR")
    logger.setLevel(getattr(logging, log_level))
    
    if logger.hasHandlers():
        logger.handlers.clear()
    
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logger.info(f"🔧 Logger iniciado | Arquivo: {log_filepath}")
    return logger

def get_logger(name="CRISPR_MMR"):
    """Obtém um logger configurado para o projeto."""
    logger = logging.getLogger("CRISPR_MMR")
    if not logger.hasHandlers():
        setup_logging()
    return logger

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🧬 TESTANDO SISTEMA DE LOGGING")
    print("="*80 + "\n")
    logger = setup_logging(log_level="DEBUG")
    logger.debug("📌 DEBUG: Informação detalhada")
    logger.info("✅ INFO: Operação completada com sucesso")
    logger.warning("⚠️  WARNING: Algo não está ideal")
    logger.error("❌ ERROR: Operação falhou")
    print("\n" + "="*80)
    print("✅ Teste concluído!")
    print("="*80 + "\n")
