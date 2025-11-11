import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Configuração da página
# -------------------------------------------------
st.set_page_config(page_title="Dashboard PET Física 2025", layout="wide")

# -------------------------------------------------
#
# -------------------------------------------------
st.markdown("""
<style>
/* === OCULTAR HEADER ORIGINAL === */
[data-testid="stHeader"] {
    background-color: transparent !important;
    border-bottom: none !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
}

/* === BOTÃO DE RECOLHER – FIXO NO TOPO === */
[data-testid="collapsedControl"] {
    position: fixed !important;
    top: 8px !important;
    left: 8px !important;
    z-index: 10000 !important;
    background: white !important;
    border: 1px solid #ddd !important;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.2) !important;
    color: #1f3a5f !important;
    font-size: 18px !important;
    font-weight: bold !important;
    cursor: pointer !important;
}

/* === SIDEBAR – OCUPA 100% DA TELA === */
[data-testid="stSidebar"] {
    top: 0 !important;
    height: 100vh !important;
    background-color: #ffffff !important;
    border-right: 1px solid #ddd !important;
    z-index: 999 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* === REMOVER TODO PADDING INTERNO === */
[data-testid="stSidebar"] > div {
    padding: 0 !important;
    margin: 0 !important;
}

/* === FORÇAR st.image E st.radio A SUBIREM === */
[data-testid="stSidebar"] .css-1d391kg,
[data-testid="stSidebar"] .css-1cpxl2t,
[data-testid="stSidebar"] .css-1offfwp {
    padding: 0 !important;
    margin: 0 !important;
}

/* === LOGO – SUBIR MUITO === */
[data-testid="stSidebar"] img {
    margin-top: -20px !important;
    margin-bottom: 8px !important;
    display: block;
    margin-left: auto;
    margin-right: auto;
}

/* === st.radio – SUBIR MUITO === */
[data-testid="stSidebar"] .stRadio {
    margin-top: -35px !important;
    padding-top: 0 !important;
}

/* === CAIXA AZUL – apenas no Início === */
.home-header {
    background: linear-gradient(135deg, #1f3a5f 0%, #2c5282 100%);
    padding: 1.8rem 2.5rem;
    border-radius: 16px;
    box-shadow: 0 6px 16px rgba(0,0,0,.18);
    margin: 1rem 0 2rem 0;
    color: white;
}
.home-header h1 {
    font-size: 2.3rem;
    font-weight: 800;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 14px;
}
.home-header .icon {
    font-size: 2.6rem;
}

/* === TÍTULOS DAS OUTRAS PÁGINAS === */
.page-title {
    font-size: 2.1rem;
    font-weight: 700;
    color: #1f3a5f;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
}
.page-title .icon {font-size: 2.2rem;}

/* === CONTEÚDO PRINCIPAL === */
.block-container {
    padding-top: 1rem !important;
    padding-left: 5rem !important;
    padding-right: 5rem !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Funções de cabeçalho
# -------------------------------------------------
def render_home_header():
    st.markdown("""
    <div class="home-header">
        <h1>
            <span class="icon">⚛️</span> Bem-vindo(a) ao Dashboard PET Física – UNIFAP
        </h1>
    </div>
    """, unsafe_allow_html=True)

def render_page_title(title, icon=""):
    st.markdown(f'<div class="page-title"><span class="icon">{icon}</span> {title}</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Sidebar (com st.image e st.radio – como no original)
# -------------------------------------------------
with st.sidebar:
    st.image("PET.png", width=200)
    menu = ["Início", "Atividades", "Cronograma", "Indicadores", "Detalhes das Atividades"]
    pagina = st.radio("Navegação", menu, label_visibility="collapsed")

# -------------------------------------------------
# Dados
# -------------------------------------------------
atividades = [
    {"Atividade": "Introdução à programação em Python", "Carga Horária": 100, "Início": "06/01/2025", "Fim": "31/12/2025"},
    {"Atividade": "Apostilas de Física", "Carga Horária": 100, "Início": "09/12/2024", "Fim": "31/12/2025"},
    {"Atividade": "Físicos da Alegria", "Carga Horária": 100, "Início": "06/01/2025", "Fim": "31/12/2025"},
    {"Atividade": "Iniciação Científica do PET Física", "Carga Horária": 100, "Início": "06/01/2025", "Fim": "31/12/2025"},
    {"Atividade": "Vídeo Aulas PET Física - UNIFAP", "Carga Horária": 100, "Início": "06/01/2025", "Fim": "31/12/2025"},
]
df = pd.DataFrame(atividades)
df["Início"] = pd.to_datetime(df["Início"], dayfirst=True)
df["Fim"] = pd.to_datetime(df["Fim"], dayfirst=True)

# -------------------------------------------------
# Páginas
# -------------------------------------------------
if pagina == "Início":
    render_home_header()
    st.markdown("""
    <div style="text-align:justify;font-size:18px;color:#333;line-height:1.7;">
    Este painel foi criado para promover a <b>transparência e acompanhamento</b> das atividades do grupo PET Física da Universidade Federal do Amapá (UNIFAP).
    Aqui você encontrará informações sobre as ações desenvolvidas ao longo de 2025, com foco em ensino, pesquisa, extensão e inovação científica.
    </div>
    <ul style="font-size:17px;margin-top:20px;color:#444;">
    <li><b>Introdução à Programação:</b> capacitação em Python para discentes e comunidade.</li>
    <li><b>Apostilas de Física:</b> elaboração de materiais didáticos gratuitos e acessíveis.</li>
    <li><b>Físicos da Alegria:</b> ações sociais e divulgação científica com empatia e solidariedade.</li>
    <li><b>Iniciação Científica:</b> incentivo à pesquisa, escrita científica e uso de LaTeX.</li>
    <li><b>Vídeo Aulas:</b> produção e publicação de conteúdos audiovisuais para ensino e popularização da física.</li>
    </ul>
    """, unsafe_allow_html=True)

else:
    if pagina == "Atividades":
        render_page_title("Lista de Atividades Planejadas", "")
        st.dataframe(df, use_container_width=True)

    elif pagina == "Cronograma":
        render_page_title("Cronograma das Atividades", "")
        fig = px.timeline(df, x_start="Início", x_end="Fim", y="Atividade", color="Atividade")
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    elif pagina == "Indicadores":
        render_page_title("Distribuição da Carga Horária", "")
        fig = px.pie(df, values="Carga Horária", names="Atividade")
        st.plotly_chart(fig, use_container_width=True)

    elif pagina == "Detalhes das Atividades":
        render_page_title("Detalhes das Atividades", "")
        atividade_sel = st.selectbox("Selecione uma atividade:", df["Atividade"])
        info = df[df["Atividade"] == atividade_sel].iloc[0]
        st.write(f"**Atividade:** {info['Atividade']}")
        st.write(f"**Carga Horária:** {info['Carga Horária']} horas")
        st.write(f"**Período:** {info['Início'].strftime('%d/%m/%Y')} - {info['Fim'].strftime('%d/%m/%Y')}")