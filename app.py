"""
CRISPR-MMR Explorer - Dashboard Streamlit
Plataforma interativa para exploração de variantes MMR e Síndrome de Lynch
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.variants.database import VariantDatabase

# Configuração da página
st.set_page_config(
    page_title="CRISPR-MMR Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e descrição
st.title("🧬 CRISPR-MMR Explorer")
st.markdown("Uma plataforma bioinformática para análise de variantes MMR e Síndrome de Lynch")

# Sidebar com navegação
st.sidebar.title("📊 Menu")
page = st.sidebar.radio(
    "Escolha uma seção:",
    ["🏠 Home", "📋 Variantes", "📊 Análises", "🧬 Por Gene", "ℹ️ Sobre"]
)

# ============================================================================
# FUNÇÕES AUXILIARES - SEM CACHE (Evita thread-safety issues)
# ============================================================================

def get_variants_dataframe():
    """Retorna todos os variantes como DataFrame."""
    db = VariantDatabase()
    sql = """
    SELECT id, clinvar_id, gene, hgvs, classificacao, tipo, 
           acmg_classification, pontos, created_at
    FROM variants
    ORDER BY gene, clinvar_id
    """
    db.cursor.execute(sql)
    columns = ['ID', 'ClinVar ID', 'Gene', 'HGVS', 'Classificação', 'Tipo', 
               'ACMG', 'Pontos', 'Data']
    data = db.cursor.fetchall()
    db.close()
    return pd.DataFrame(data, columns=columns)

# ============================================================================
# PÁGINA: HOME
# ============================================================================

if page == "🏠 Home":
    st.markdown("---")
    
    # Estatísticas principais
    db = VariantDatabase()
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Total de variantes
    db.cursor.execute("SELECT COUNT(*) FROM variants")
    total = db.cursor.fetchone()[0]
    col1.metric("📊 Total de Variantes", total)
    
    # Patogênicas
    db.cursor.execute("SELECT COUNT(*) FROM variants WHERE acmg_classification LIKE '%Pathogenic%'")
    pathogenic = db.cursor.fetchone()[0]
    col2.metric("⚠️ Patogênicas", pathogenic)
    
    # Genes únicos
    db.cursor.execute("SELECT COUNT(DISTINCT gene) FROM variants")
    genes = db.cursor.fetchone()[0]
    col3.metric("🧬 Genes MMR", genes)
    
    # Pontos médios
    db.cursor.execute("SELECT AVG(pontos) FROM variants")
    avg_pts = db.cursor.fetchone()[0]
    col4.metric("📈 Pontos Médios", f"{avg_pts:.2f}")
    
    db.close()
    
    st.markdown("---")
    
    # Gráfico de distribuição ACMG
    df = get_variants_dataframe()
    acmg_counts = df['ACMG'].value_counts()
    
    fig = px.pie(
        values=acmg_counts.values,
        names=acmg_counts.index,
        title="Distribuição de Classificação ACMG",
        color_discrete_map={
            "Pathogenic (P)": "#d32f2f",
            "Likely Pathogenic (LP)": "#f57c00",
            "Benign (B)": "#388e3c"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PÁGINA: VARIANTES
# ============================================================================

elif page == "📋 Variantes":
    st.header("📋 Todas as Variantes")
    
    df = get_variants_dataframe()
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gene_filter = st.multiselect(
            "🧬 Filtrar por Gene:",
            options=sorted(df['Gene'].unique()),
            default=sorted(df['Gene'].unique())
        )
    
    with col2:
        acmg_filter = st.multiselect(
            "⚠️ Filtrar por ACMG:",
            options=sorted(df['ACMG'].unique()),
            default=sorted(df['ACMG'].unique())
        )
    
    with col3:
        type_filter = st.multiselect(
            "🔤 Filtrar por Tipo:",
            options=sorted(df['Tipo'].unique()),
            default=sorted(df['Tipo'].unique())
        )
    
    # Aplicar filtros
    df_filtered = df[
        (df['Gene'].isin(gene_filter)) &
        (df['ACMG'].isin(acmg_filter)) &
        (df['Tipo'].isin(type_filter))
    ]
    
    st.markdown(f"**Mostrando {len(df_filtered)} de {len(df)} variantes**")
    
    # Tabela
    st.dataframe(df_filtered, use_container_width=True, height=400)
    
    # Download CSV
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="📥 Baixar como CSV",
        data=csv,
        file_name="variantes_filtradas.csv",
        mime="text/csv"
    )

# ============================================================================
# PÁGINA: ANÁLISES
# ============================================================================

elif page == "📊 Análises":
    st.header("📊 Análises Estatísticas")
    
    df = get_variants_dataframe()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por Gene
        gene_counts = df['Gene'].value_counts().sort_index()
        fig_gene = px.bar(
            x=gene_counts.index,
            y=gene_counts.values,
            title="Variantes por Gene",
            labels={"x": "Gene", "y": "Quantidade"}
        )
        st.plotly_chart(fig_gene, use_container_width=True)
    
    with col2:
        # Distribuição por Tipo
        type_counts = df['Tipo'].value_counts()
        fig_type = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="Variantes por Tipo",
            labels={"x": "Tipo", "y": "Quantidade"}
        )
        st.plotly_chart(fig_type, use_container_width=True)
    
    # Pontos por Gene
    st.subheader("Distribuição de Pontos por Gene")
    fig_pts = px.box(
        df,
        x='Gene',
        y='Pontos',
        title="Score de Patogenicidade por Gene",
        color='Gene'
    )
    st.plotly_chart(fig_pts, use_container_width=True)

# ============================================================================
# PÁGINA: POR GENE
# ============================================================================

elif page == "🧬 Por Gene":
    st.header("🧬 Análise por Gene MMR")
    
    genes = ['MLH1', 'MSH2', 'MSH6', 'PMS2']
    selected_gene = st.selectbox("Selecione um gene:", genes)
    
    # Query do gene selecionado
    db = VariantDatabase()
    sql = "SELECT clinvar_id, hgvs, acmg_classification, pontos FROM variants WHERE gene = ?"
    db.cursor.execute(sql, (selected_gene,))
    results = db.cursor.fetchall()
    db.close()
    
    st.subheader(f"Gene: {selected_gene}")
    st.write(f"**Total de variantes: {len(results)}**")
    
    # Tabela
    df_gene = pd.DataFrame(
        results,
        columns=['ClinVar ID', 'HGVS', 'ACMG', 'Pontos']
    )
    st.dataframe(df_gene, use_container_width=True)
    
    # Info sobre o gene
    gene_info = {
        'MLH1': 'MutL homolog 1 - Gene mais frequentemente mutado em Lynch',
        'MSH2': 'MutS homolog 2 - Segundo gene mais comum em Lynch',
        'MSH6': 'MutS homolog 6 - Presentations atípicas de Lynch',
        'PMS2': 'PMS1 homolog 2 - Penetrância mais baixa'
    }
    st.info(f"ℹ️ {gene_info[selected_gene]}")

# ============================================================================
# PÁGINA: SOBRE
# ============================================================================

elif page == "ℹ️ Sobre":
    st.header("ℹ️ Sobre este Projeto")
    
    st.markdown("""
    ### 🎯 Objetivo
    Plataforma bioinformática para exploração e análise de variantes no sistema 
    Mismatch Repair (MMR) e Síndrome de Lynch (HNPCC).
    
    ### 🧬 Genes Cobertos
    - **MLH1**: MutL homolog 1
    - **MSH2**: MutS homolog 2
    - **MSH6**: MutS homolog 6
    - **PMS2**: PMS1 homolog 2
    - **EPCAM**: Epithelial Cell Adhesion Molecule
    
    ### 📊 Dados
    - Variantes de: ClinVar, InSiGHT
    - Classificação: ACMG/AMP guidelines
    - Total: 10 variantes (Fase 3A)
    
    ### 🛠️ Stack Tecnológico
    - **Backend**: Python 3.9 + SQLite
    - **Frontend**: Streamlit
    - **Dados**: pandas, plotly
    - **Versionamento**: Git/GitHub
    
    ### 👤 Autor
    Carla Rodrigues - Bioinformática Clínica
    
    ### 📝 Licença
    MIT License
    """)

st.markdown("---")
st.markdown("**CRISPR-MMR Explorer** | v0.3.0 | Junho 2026")
