"""
Testes para a função main()
Valida que main() executa corretamente
"""

import pytest
from unittest.mock import patch
from src.variants.acmg_analyzer import main
from src.utils.exceptions import FileProcessingError


class TestMainFunction:
    """Testes da função main()"""
    
    @patch('src.variants.acmg_analyzer.process_csv')
    def test_main_with_file_error(self, mock_process_csv):
        """Testa main() quando FileProcessingError é lançado"""
        # Setup
        mock_process_csv.side_effect = FileProcessingError("Arquivo não encontrado")
        
        # Execute - não deve lançar exceção (é capturada)
        try:
            main()
        except SystemExit:
            pass  # Esperado
    
    @patch('src.variants.acmg_analyzer.process_csv')
    def test_main_with_generic_error(self, mock_process_csv):
        """Testa main() quando erro genérico é lançado"""
        # Setup
        mock_process_csv.side_effect = Exception("Erro inesperado")
        
        # Execute - não deve lançar exceção (é capturada)
        try:
            main()
        except SystemExit:
            pass  # Esperado
    
    def test_main_function_exists(self):
        """Testa que função main() existe e é callable"""
        assert callable(main), "main deve ser uma função callable"
