import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# -------------------------------------------------
# Configuração da página
# -------------------------------------------------
st.set_page_config(page_title="Dashboard PET Física 2025", layout="wide")

# Estado da sessão
if 'menu_principal' not in st.session_state:
    st.session_state.menu_principal = True
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = "Início"

# Data atual
TODAY = datetime.date(2025, 11, 26)

# -------------------------------------------------
# Estilo Dark Mode + Design PET Física
# -------------------------------------------------
st.markdown("""
<style>
    :root {
        --pet-blue: #1f3a5f;
        --dark-bg: #0E1117;
        --panel-bg: #1E1E1E;
        --hover: #262730;
    }
    .css-1d391kg, .css-1cpxl2t, body { background-color: var(--dark-bg) !important; }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stSidebar"] { background-color: #16181d; border-right: 1px solid #333; }
    .stRadio > div { gap: 0.4rem; }
    .stRadio label { 
        padding: 0.6rem 1rem !important; 
        border-radius: 8px; 
        transition: all 0.2s;
    }
    .stRadio label:hover { background-color: var(--hover) !important; }
    .stRadio div[role="radiogroup"] > label[data-checked="true"] {
        background: var(--pet-blue) !important; 
        color: white !important; 
        font-weight: 600 !important;
    }
    .home-header {
        background: linear-gradient(135deg, var(--pet-blue) 0%, #2c5282 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        margin: 1rem 0 2rem 0;
        color: white;
    }
    .home-header h1 { font-size: 2.4rem; margin: 0; display: flex; align-items: center; gap: 16px; }
    .page-title { font-size: 2.2rem; font-weight: 700; color: var(--pet-blue); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 12px; }
    .white-title { font-size: 2.2rem; font-weight: 700; color: white !important; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 12px; }
    .block-container { padding-top: 1.5rem !important; }
    .stDataFrame, .stPlotlyChart > div { background-color: var(--panel-bg); border-radius: 12px; padding: 12px; }
    [data-testid="stMetric"] { background: var(--panel-bg); border-radius: 12px; padding: 12px; }
    [data-testid="stMetric"] label { color: #cccccc !important; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Dados (Atividades, Alunos e Métricas)
# -------------------------------------------------
atividades = [
    {"Atividade": "Introdução à programação em Python", "Carga Horária": 100, "Início": "06/01/2025", "Fim": "31/12/2025"},
    {"Atividade": "Apostilas de Física", "Carga Horária": 100, "Início": "09/12/2024", "Fim": "31/12/2025"},
    {"Atividade": "Físicos da Alegria", "Carga Horária": 100, "Início": "06/01/2025", "Fim": "31/12/2025"},
    {"Atividade": "Iniciação Científica do PET Física", "Carga Horária": 100, "Início": "06/01/2025", "Fim": "31/12/2025"},
    {"Atividade": "Vídeo Aulas PET Física - UNIFAP", "Carga Horária": 100, "Início": "06/01/2025", "Fim": "31/12/2025"},
]
df_atividades = pd.DataFrame(atividades)
df_atividades["Início"] = pd.to_datetime(df_atividades["Início"], dayfirst=True)
df_atividades["Fim"] = pd.to_datetime(df_atividades["Fim"], dayfirst=True)

nomes_alunos_menu = [
    "Angelo Haroldo Dos Santos ",
    "Felipe De Souza Pereira",
    "Ian Rodrigo Colares Dias",
    "Jaimison Costa De Souza",
    "Joao Maciel Dos Santos",
    "Luiz Eduardo Barbosa",
    "Mayara Pamplona ",
    "Theyllorran Gomes Araujo"
]
nomes_alunos_menu.sort()

nome_para_dados = {
    "Angelo Haroldo Dos Santos ": "Angelo Haroldo Dos Santos Bonfim Junior",
    "Felipe De Souza Pereira": "Felipe De Souza Pereira",
    "Ian Rodrigo Colares Dias": "Ian Rodrigo Colares Dias",
    "Jaimison Costa De Souza": "Jaimison Costa De Souza",
    "Joao Maciel Dos Santos": "Joao Maciel Dos Santos",
    "Luiz Eduardo Barbosa": "Luiz Eduardo Barbosa",
    "Mayara Pamplona ": "Mayara Pamplona ",
    "Theyllorran Gomes Araujo": "Theyllorran Gomes Araujo",
}

# Métricas por aluno
dados_metricas_alunos = {nome.strip(): {
    "ENTRADA": datetime.date(2023, 3, 1), "SAIDA": None,
    "CRAS": [(2023.1, 8.5), (2023.2, 9.0), (2024.1, 9.2), (2024.2, 9.3)],
    "CONGRESSOS": 3, "TRABALHOS_PUBLICADOS": 1, "MINICURSOS_MINISTRADOS": 4,
    "REUNIOES_PRESENTE": 25, "TOTAL_REUNIOES": 30, "TAREFAS_ATRIBUIDAS": 25, "TAREFAS_ENTREGUES": 23,
} for nome in nomes_alunos_menu}

# Exemplo realista para alguns alunos
dados_metricas_alunos["Felipe De Souza Pereira"].update({
    "ENTRADA": datetime.date(2024, 8, 1), "CRAS": [(2024.2, 7.8)],
    "CONGRESSOS": 1, "MINICURSOS_MINISTRADOS": 2, "REUNIOES_PRESENTE": 10, "TOTAL_REUNIOES": 12,
    "TAREFAS_ATRIBUIDAS": 8, "TAREFAS_ENTREGUES": 7
})

# Dados de progresso nas atividades (exemplo)
dados_alunos = [
    {"Nome": "Angelo Haroldo Dos Santos Bonfim Junior", "Atividade": "Introdução à programação em Python", "Status": "Em Andamento", "Progresso (%)": 90, "Horas Registradas": 90},
    {"Nome": "Felipe De Souza Pereira", "Atividade": "Introdução à programação em Python", "Status": "Em Andamento", "Progresso (%)": 75, "Horas Registradas": 75},
]
df_alunos = pd.DataFrame(dados_alunos)

# -------------------------------------------------
# Funções Auxiliares
# -------------------------------------------------
def render_home_header():
    st.markdown("""
    <div class="home-header">
        <h1>⚛ Bem-vindo(a) ao Dashboard PET Física – UNIFAP</h1>
    </div>
    """, unsafe_allow_html=True)

def render_page_title(title, icon="", white=False):
    classe = "white-title" if white or st.session_state.pagina_atual.strip() in nomes_alunos_menu else "page-title"
    st.markdown(f'<div class="{classe}"><span style="font-size:2.4rem">{icon}</span> {title}</div>', unsafe_allow_html=True)

def criar_gauge(valor, titulo, texto_central, texto_inferior):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor,
        number={'suffix': "%", 'font': {'size': 50, 'color': 'white'}},
        title={'text': titulo, 'font': {'size': 16, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "gray", 'tickfont': {'color': 'lightgray'}},
            'bar': {'color': "white", 'thickness': 0.18},
            'bgcolor': "#1E1E1E",
            'steps': [
                {'range': [0, 33.33], 'color': '#D3404B'},
                {'range': [33.33, 66.66], 'color': '#FFC700'},
                {'range': [66.66, 100], 'color': '#00B050'},
            ],
        }
    ))
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="#1E1E1E",
        font={'color': "white"},
        annotations=[
            go.layout.Annotation(x=0.5, y=0.38, xref="paper", yref="paper", text=texto_central, showarrow=False, font={'size': 20, 'color': 'white'}),
            go.layout.Annotation(x=0.5, y=-0.15, xref="paper", yref="paper", text=texto_inferior, showarrow=False, font={'size': 12, 'color': '#aaa'})
        ]
    )
    return fig

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.image("PET.png", width=200, caption="PET Física UNIFAP")

    if st.session_state.menu_principal:
        opcao = st.radio(
            "Menu Principal",
            ["Início", "Alunos", "Detalhes das Atividades"],
            label_visibility="collapsed"
        )
        if opcao == "Alunos":
            st.session_state.menu_principal = False
            st.session_state.pagina_aluno = nomes_alunos_menu[0]
            st.session_state.pagina_atual = nomes_alunos_menu[0]
            st.rerun()
        else:
            st.session_state.pagina_atual = opcao
    else:
        st.markdown("### Alunos")
        if st.button("Voltar ao Menu"):
            st.session_state.menu_principal = True
            st.session_state.pagina_atual = "Início"
            st.rerun()

        aluno = st.radio(
            "Selecione o aluno",
            nomes_alunos_menu,
            index=nomes_alunos_menu.index(st.session_state.pagina_atual) if st.session_state.pagina_atual in nomes_alunos_menu else 0,
            label_visibility="collapsed"
        )
        st.session_state.pagina_atual = aluno

pagina = st.session_state.pagina_atual

# -------------------------------------------------
# PÁGINAS
# -------------------------------------------------
if pagina == "Início":
    render_home_header()
    st.markdown("""
    <div style="text-align:justify; font-size:18px; line-height:1.8; color:white;">
    Este painel foi criado para promover a <strong>transparência e acompanhamento</strong> das atividades do grupo PET Física da Universidade Federal do Amapá (UNIFAP).
    Aqui você encontrará informações sobre ensino, pesquisa, extensão e inovação científica ao longo de 2025.
    </div>
    <ul style="font-size:17px; margin-top:20px; color:white;">
        <li><b>Introdução à Programação:</b> capacitação em Python</li>
        <li><b>Apostilas de Física:</b> materiais didáticos gratuitos</li>
        <li><b>Físicos da Alegria:</b> ações sociais e divulgação científica</li>
        <li><b>Iniciação Científica:</b> pesquisa e escrita científica</li>
        <li><b>Vídeo Aulas:</b> produção de conteúdo audiovisual</li>
    </ul>
    """, unsafe_allow_html=True)

elif pagina == "Detalhes das Atividades":
    render_page_title("Detalhes das Atividades", "Análise")
    col1, col2 = st.columns(2)
    with col1:
        atividade = st.selectbox("Atividade", df_atividades["Atividade"])
    with col2:
        aluno_filtro = st.selectbox("Filtrar por aluno", ["Todos os Alunos"] + sorted(df_alunos["Nome"].unique()))

    info = df_atividades[df_atividades["Atividade"] == atividade].iloc[0]
    st.markdown(f"**{info['Atividade']}** • {info['Carga Horária']}h • {info['Início'].strftime('%d/%m/%Y')} - {info['Fim'].strftime('%d/%m/%Y')}")

    df_filtrado = df_alunos[df_alunos["Atividade"] == atividade]
    if aluno_filtro != "Todos os Alunos":
        df_filtrado = df_filtrado[df_filtrado["Nome"] == aluno_filtro]

    if not df_filtrado.empty:
        st.dataframe(df_filtrado[["Nome", "Status", "Progresso (%)", "Horas Registradas"]], use_container_width=True, hide_index=True)
        fig = px.bar(df_filtrado, x="Nome", y="Progresso (%)", color="Status", range_y=[0,100],
                     color_discrete_map={"Concluído": "green", "Em Andamento": "orange"})
        fig.update_layout(paper_bgcolor="#1E1E1E", plot_bgcolor="#1E1E1E", font_color="white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum registro encontrado.")

elif pagina in nomes_alunos_menu:
    aluno_menu = pagina.strip()
    nome_real = nome_para_dados.get(aluno_menu, aluno_menu)
    metricas = dados_metricas_alunos.get(aluno_menu, {})
    df_aluno = df_alunos[df_alunos["Nome"] == nome_real]

    render_page_title(f"Desempenho de {aluno_menu}", "Perfil", white=True)

    if not metricas:
        st.warning("Métricas detalhadas ainda não cadastradas para este aluno.")
    else:
        entrada = metricas["ENTRADA"]
        saida = metricas["SAIDA"] or TODAY
        dias = (saida - entrada).days
        anos, meses = dias // 365, (dias % 365) // 30
        tempo = f"{anos}a {meses}m" if anos or meses else f"{dias} dias"

        df_cra = pd.DataFrame(metricas["CRAS"], columns=["Semestre", "CRA"])
        cra_medio = round(df_cra["CRA"].mean(), 2) if not df_cra.empty else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Tempo no PET", tempo)
        col2.metric("Média CRA", cra_medio)
        col3.metric("Congressos", metricas["CONGRESSOS"])
        col4.metric("Trabalhos Publicados", metricas["TRABALHOS_PUBLICADOS"])

        st.divider()
        col5, col6, col7 = st.columns(3)
        col5.metric("Minicursos Ministrados", metricas["MINICURSOS_MINISTRADOS"])

        taxa_reunioes = round(metricas["REUNIOES_PRESENTE"] / metricas["TOTAL_REUNIOES"] * 100, 1) if metricas["TOTAL_REUNIOES"] > 0 else 0
        col6.plotly_chart(criar_gauge(taxa_reunioes, "Assiduidade em Reuniões", "Presente",
                                      f"{metricas['REUNIOES_PRESENTE']} de {metricas['TOTAL_REUNIOES']}"), use_container_width=True)

        taxa_tarefas = round(metricas["TAREFAS_ENTREGUES"] / metricas["TAREFAS_ATRIBUIDAS"] * 100, 1) if metricas["TAREFAS_ATRIBUIDAS"] > 0 else 0
        col7.plotly_chart(criar_gauge(taxa_tarefas, "Conclusão de Tarefas", "Entregue",
                                      f"{metricas['TAREFAS_ENTREGUES']} de {metricas['TAREFAS_ATRIBUIDAS']}"), use_container_width=True)

        # NOVO GRÁFICO: Contribuições Mensais (Atividades)
        st.markdown("### Contribuições Mensais (Atividades)")

        dados_contribuicoes = pd.DataFrame({
            'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul'],
            'Minicursos': [2.0, 1.5, 2.0, 2.5, 3.0, 1.5, 1.0],
            'Palestras':  [1.0, 1.2, 1.8, 2.0, 1.5, 1.8, 1.2],
            'Monitorias': [3.0, 3.5, 3.0, 3.2, 4.0, 3.5, 2.8]
        })

        fig = go.Figure()

        fig.add_trace(go.Bar(name='Minicursos', x=dados_contribuicoes['Mês'], y=dados_contribuicoes['Minicursos'],
                             marker_color='#4FC3F7', text=dados_contribuicoes['Minicursos'], textposition='inside'))
        fig.add_trace(go.Bar(name='Palestras', x=dados_contribuicoes['Mês'], y=dados_contribuicoes['Palestras'],
                             marker_color='#BA68C8', text=dados_contribuicoes['Palestras'], textposition='inside'))
        fig.add_trace(go.Bar(name='Monitorias', x=dados_contribuicoes['Mês'], y=dados_contribuicoes['Monitorias'],
                             marker_color='#FF8A65', text=dados_contribuicoes['Monitorias'], textposition='inside'))

        fig.update_traces(texttemplate='%{text:.1f}', textfont_size=12)
        fig.update_layout(
            barmode='stack',
            yaxis_title="Quantidade",
            paper_bgcolor="#1E1E1E",
            plot_bgcolor="#1E1E1E",
            font_color="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=40, t=80, b=40),
            height=500
        )
        fig.update_yaxes(range=[0, 11], gridcolor="#333")
        fig.update_xaxes(gridcolor="#333")

        st.plotly_chart(fig, use_container_width=True)

    if not df_aluno.empty:
        st.markdown("### Progresso nas Atividades")
        st.dataframe(df_aluno[["Atividade", "Status", "Progresso (%)", "Horas Registradas"]], use_container_width=True, hide_index=True)
        fig_bar = px.bar(df_aluno, x="Atividade", y="Progresso (%)", color="Atividade", range_y=[0,100])
        fig_bar.update_layout(paper_bgcolor="#1E1E1E", plot_bgcolor="#1E1E1E", font_color="white")
        st.plotly_chart(fig_bar, use_container_width=True)

# Rodapé
st.sidebar.markdown("---")
st.sidebar.caption("Dashboard PET Física UNIFAP © 2025")