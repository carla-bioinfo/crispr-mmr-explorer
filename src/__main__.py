import sys
import os
from streamlit.web import cli as stcli

def main():
    # Descobre o caminho absoluto para o arquivo do dashboard
    # Isso evita problemas de caminhos relativos na hora de rodar no Docker
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_path = os.path.join(current_dir, "dashboard", "app.py")
    
    # Monta o comando que o Streamlit vai rodar internamente
    sys.argv = ["streamlit", "run", dashboard_path]
    
    # Inicia o servidor do Streamlit
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()