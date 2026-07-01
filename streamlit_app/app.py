"""
CRISPR-MMR Explorer - Streamlit Dashboard v2.0.2
Interface web conectada a FastAPI Backend
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
import json

# Configurar página
st.set_page_config(
    page_title="CRISPR-MMR Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL da API (configurável)
API_URL = "http://localhost:8000"

# Título principal
st.title("🧬 CRISPR-MMR Explorer")
st.markdown("**Plataforma de análise de variantes no sistema Mismatch Repair**")
st.markdown("**Versão**: v2.0.2 com FastAPI Backend | **Status**: Production 🚀")

# Sidebar - Menu
st.sidebar.title("📋 Menu")
st.sidebar.markdown("---")

# Opções de navegação
page = st.sidebar.radio(
    "Selecione uma página:",
    ["🏠 Início", "📁 Upload & Classificar", "📊 Análise", "ℹ️ Sobre"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Configurações API")

# Seletor de gene (obrigatório para classificação)
selected_gene = st.sidebar.selectbox(
    "Selecione gene MMR:",
    ["MLH1", "MSH2", "MSH6", "PMS2", "EPCAM"],
    help="Gene a ser analisado"
)

# Status da API
try:
    health_response = requests.get(f"{API_URL}/health/", timeout=2)
    if health_response.status_code == 200:
        st.sidebar.success("✅ API Conectada")
    else:
        st.sidebar.error("❌ API Desconectada")
except:
    st.sidebar.error("❌ API Indisponível")

st.sidebar.markdown("---")

# ============= PÁGINA: INÍCIO =============
if page == "🏠 Início":
    st.subheader("Bem-vindo ao CRISPR-MMR Explorer!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        ### O que é?
        
        Plataforma de análise de variantes no sistema **Mismatch Repair (MMR)** 
        e **Síndrome de Lynch**.
        
        - 🔬 Classificação ACMG/AMP 2015 (Real!)
        - 📊 Visualizações interativas
        - 💾 Download de resultados
        - 🔌 Conectado a FastAPI Backend
        """)
    
    with col2:
        st.success("""
        ### Versão 2.0.2
        
        ✅ API FastAPI Integrada
        ✅ Classificação ACMG/AMP Real
        ✅ 7 Testes Passando
        ✅ Production-Ready
        """)

# ============= PÁGINA: UPLOAD & CLASSIFICAR =============
elif page == "📁 Upload & Classificar":
    st.subheader("📁 Envie um Arquivo VCF para Classificação ACMG/AMP Real")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("""
        ### Formato Esperado
        
        Arquivo de texto com colunas separadas por espaço:
CHR  POS      REF  ALT
    3    36993722 A    G
    3    36993722 AGT  A
""")
    
    with col2:
        st.warning(f"""
        ### Configurações
        
        - Gene Selecionado: **{selected_gene}**
        - Máximo: 100 variantes
        - Formato: TXT/VCF
        """)
    
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "📤 Arraste ou clique para selecionar arquivo",
        type=["vcf", "txt"],
        help="Arquivo TXT ou VCF com variantes"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ Arquivo carregado: **{uploaded_file.name}** ({uploaded_file.size} bytes)")
        
        # Ler arquivo
        file_content = uploaded_file.read().decode("utf-8")
        lines = [l for l in file_content.split("\n") if l.strip() and not l.startswith("#")]
        
        st.info(f"📊 Total de variantes: {len(lines)}")
        
        if st.button("🔍 Classificar com API", key="classify"):
            st.info("⏳ Enviando variantes para FastAPI Backend...")
            
            progress_bar = st.progress(0)
            results = []
            errors = []
            
            for idx, line in enumerate(lines[1:100]):  # Skip header
                parts = line.split()
                if len(parts) >= 4:
                    chromosome = parts[0]
                    position = int(parts[1])
                    ref = parts[2]
                    alt = parts[3]
                    
                    try:
                        # Fazer POST request à API
                        response = requests.post(
                            f"{API_URL}/api/classify",
                            json={
                                "chromosome": chromosome,
                                "position": position,
                                "ref": ref,
                                "alt": alt,
                                "gene": selected_gene
                            },
                            timeout=5
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            results.append({
                                "CHR": chromosome,
                                "POS": position,
                                "REF": ref,
                                "ALT": alt,
                                "Gene": selected_gene,
                                "Classificação": data["data"]["pathogenicity_class"],
                                "Critérios ACMG": ", ".join(data["data"]["acmg_criteria"]),
                                "Score": data["data"]["confidence_score"]
                            })
                        else:
                            errors.append(f"Erro HTTP {response.status_code}: {chromosome}:{position}")
                    
                    except Exception as e:
                        errors.append(f"Erro na variante {chromosome}:{position}: {str(e)}")
                
                # Atualizar progress bar
                progress_bar.progress((idx + 1) / min(len(lines), 100))
            
            if results:
                st.success(f"✅ {len(results)} variantes classificadas com sucesso!")
                
                # Exibir resultados em tabela
                df_results = pd.DataFrame(results)
                st.dataframe(df_results, use_container_width=True)
                
                # Gráfico de distribuição
                st.subheader("📊 Distribuição de Classificações")
                fig = px.pie(
                    df_results,
                    names="Classificação",
                    title="Distribuição de Patogenicidade",
                    hole=0.3
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Download de resultados
                csv = df_results.to_csv(index=False)
                st.download_button(
                    label="💾 Download Resultados (CSV)",
                    data=csv,
                    file_name="variantes_classificadas.csv",
                    mime="text/csv"
                )
            
            if errors:
                st.warning(f"⚠️ {len(errors)} variantes com erro:")
                for error in errors:
                    st.caption(f"  - {error}")

# ============= PÁGINA: ANÁLISE =============
elif page == "📊 Análise":
    st.subheader("📊 Análise de Variantes (Exemplo Mock)")
    
    # Dados de exemplo
    example_data = {
        "Gene": ["MLH1", "MLH1", "MSH2", "MSH6", "PMS2"],
        "Classificação": ["Pathogenic", "Likely Pathogenic", "VUS", "Benign", "Likely Benign"],
        "Score": [0.95, 0.85, 0.50, 0.15, 0.25],
        "Frequência": [5, 12, 8, 3, 2]
    }
    
    df = pd.DataFrame(example_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_bar = px.bar(df, x="Gene", y="Frequência", color="Classificação", title="Variantes por Gene")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        fig_scatter = px.scatter(df, x="Score", y="Frequência", color="Classificação", size="Frequência")
        st.plotly_chart(fig_scatter, use_container_width=True)

# ============= PÁGINA: SOBRE =============
elif page == "ℹ️ Sobre":
    st.subheader("ℹ️ Sobre CRISPR-MMR Explorer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🧬 Sobre Lynch Syndrome & MMR
        
        **Síndrome de Lynch** é predisposição hereditária ao câncer coloretal.
        
        Causada por variantes em genes **Mismatch Repair**:
        - MLH1
        - MSH2
        - MSH6
        - PMS2
        - EPCAM
        
        ### 📋 ACMG/AMP 2015
        Diretrizes internacionais para interpretação de variantes genéticas.
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 Stack Técnico
        
        **Frontend**: Streamlit (Python)
        **Backend**: FastAPI (Python)
        **Classificação**: ACMGClassifier v0.5.0
        **Testes**: pytest (7/7 passando)
        **Versionamento**: Git
        
        ### 📞 Contato
        
        Desenvolvido com ❤️ para bioinformática clínica.
        """)
