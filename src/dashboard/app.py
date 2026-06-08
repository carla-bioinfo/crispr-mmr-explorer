import streamlit as st

def render_page():
    st.set_page_config(
        page_title="CRISPR-MMR Explorer",
        page_icon="🧬",
        layout="wide"
    )

    st.title("🧬 Bem-vindo ao CRISPR-MMR Explorer")
    st.markdown("---")
    
    st.write(
        "Esta é uma plataforma bioinformática para análise dos genes do sistema "
        "**Mismatch Repair (MMR)** e exploração de variantes ligadas à **Síndrome de Lynch**."
    )
    
    st.info("Status do Sistema: Ambiente Docker inicializado com sucesso! 🚀")

if __name__ == "__main__":
    render_page()