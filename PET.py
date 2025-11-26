import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# -------------------------------------------------
# Configuração da página e Estado da Sessão
# -------------------------------------------------
st.set_page_config(page_title="Dashboard PET Física 2025", layout="wide")

# Inicializa o estado de visualização do menu
if 'menu_principal' not in st.session_state:
    st.session_state.menu_principal = True
# Variável para armazenar a página atual
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = "Início"
# A variável 'conta_pagina' não é mais necessária, mas a mantemos para segurança.
if 'conta_pagina' not in st.session_state:
    st.session_state.conta_pagina = "Principal"


# -------------------------------------------------
# Estilos (Destaque Azul Aplicado)
# -------------------------------------------------
st.markdown("""
<style>
/* VARIÁVEIS DE COR */
:root {
    --pet-blue: #1f3a5f; /* Azul escuro do PET/cabeçalho */
    --light-bg: #f0f2f6; /* Cor de fundo claro padrão (var(--background-color-tertiary)) */
    --hover-bg: #e1e4e8; /* Um tom um pouco mais escuro para o hover */
}

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
    background: var(--background-color-tertiary) !important; 
    border: 1px solid var(--border-color-subtle) !important;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.2) !important;
    color: var(--pet-blue) !important; 
    font-size: 18px !important;
    font-weight: bold !important;
    cursor: pointer !important;
}

/* === SIDEBAR – OCUPA 100% DA TELA === */
[data-testid="stSidebar"] {
    top: 0 !important;
    height: 100vh !important;
    background-color: var(--background-color-secondary) !important; 
    border-right: 1px solid var(--border-color-subtle) !important;
    z-index: 999 !important;
    padding: 0 !important; 
    margin: 0 !important;
}

/* === REMOVER TODO PADDING INTERNO DA SIDEBAR === */
[data-testid="stSidebar"] > div {
    padding: 0 !important;
    margin: 0 !important;
}

/* === LOGO – AJUSTADO PARA SUBIR MAIS === */
[data-testid="stSidebar"] img {
    margin-top: 5px !important; 
    margin-bottom: 8px !important;
    display: block;
    margin-left: auto;
    margin-right: auto;
}

/* === TÍTULO "Navegação" (Sua Conta) === */
.sidebar-title {
    font-size: 1rem; 
    font-weight: 600;
    color: var(--text-color-secondary) !important; 
    padding: 5px 1rem 5px 1rem;
    margin-top: 15px !important; 
    margin-bottom: 0px !important;
    display: block;
}

/* === TÍTULO "Lista de Alunos" do submenu (AJUSTADO) === */
[data-testid="stSidebar"] h3 {
    color: var(--text-color) !important;
    padding-left: 1rem;
    padding-right: 1rem;
    font-size: 1.2rem; 
    /* Reduz a margem superior do título para aproximá-lo do logo/título acima */
    margin-top: 5px !important; 
    margin-bottom: 5px !important; /* Margem inferior para separá-lo do botão */
}

/* === BOTÃO/CONTEÚDO ABAIXO DO TÍTULO (NOVO AJUSTE) === */
/* Esta regra mira o container do botão 'Voltar ao Menu Principal' e os elementos de rádio */
div[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:nth-child(2) > div:nth-child(2) {
    /* Puxa o conteúdo (que inclui o botão) para mais perto do título H3. */
    padding-top: 0px !important; 
    margin-top: -5px !important;
}

/* === ESTILO PARA st.radio (Links) (MARGEM -50px MANTIDA) === */
.stRadio {
    padding-top: 0px !important;
    /* Margem negativa agressiva MANTIDA, a sobreposição será corrigida abaixo */
    margin-top: -50px !important; 
}

/* Oculta os botões de rádio nativos */
.stRadio [data-testid="stFormSubmitButton"] + div label > div:first-child,
.stRadio label > div:first-child {
    display: none !important;
}

/* Estilo de background e padding para as opções de rádio (Links) */
.stRadio label {
    padding: 0.35rem 1rem !important; 
    margin-bottom: 2px; 
    border-radius: 6px; 
    font-size: 1.1rem; 
    color: var(--text-color) !important; 
    transition: background-color 0.2s, color 0.2s;
    width: 100%; 
    display: flex; 
    align-items: center; 
    cursor: pointer;
}

/* Estilo de Hover */
.stRadio label:hover {
    background-color: var(--hover-bg) !important; 
}

/* ================================================= */
/* === REMOÇÃO DO ITEM SELECIONÁVEL VAZIO ENTRE "NAVEGAÇÃO" E "INÍCIO" (Menu Principal) === */
/* Oculta o primeiro elemento dentro do grupo de rádio (o rótulo colapsado) */
.stRadio div[role="radiogroup"] > div:nth-child(1) {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* === CORREÇÃO CRÍTICA DO ESPAÇO VAZIO DO SUBMENU DE ALUNOS (ITEM FANTASMA OCULTO) === */
/* Mira o container do st.radio com a chave 'submenu_alunos' e remove o primeiro elemento (o indesejado) */
[data-testid="stSidebar"] [data-testid="stRadioGroup-submenu_alunos"] > div:nth-child(1) {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* === CORREÇÃO DA SOBREPOSIÇÃO: REMOVE O ESTADO DE SELEÇÃO INICIAL DO PRIMEIRO ALUNO === */
/* O div:nth-child(2) é o primeiro item REAL da lista (Angelo Haroldo), após o fantasma ser ocultado. */
/* Anula o estilo 'st-bq' (selecionado) neste primeiro item para impedir que ele sobreponha o botão. */
[data-testid="stSidebar"] [data-testid="stRadioGroup-submenu_alunos"] > div:nth-child(2) > label.st-bq {
    background-color: transparent !important; /* Remove o fundo */
    font-weight: 400 !important; /* Remove o negrito */
    color: var(--text-color) !important; /* Volta para a cor de texto normal */
}

/* Garante que o span interno do primeiro aluno também volte ao normal */
[data-testid="stSidebar"] [data-testid="stRadioGroup-submenu_alunos"] > div:nth-child(2) > label.st-bq span {
    color: var(--text-color) !important; 
}


/* ================================================= */
/* === ESTILO DA OPÇÃO SELECIONADA (DESTAQUE AZUL - 100% WIDE) === */

/* Aplica o background AZUL no label.st-bq (o item selecionado) */
.stRadio div > label.st-bq {
    background-color: var(--pet-blue) !important; /* ⬅ AZUL APLICADO */
    border-radius: 6px !important; 
    font-weight: 700 !important; 
    color: white !important; 
    width: 100% !important; 
    padding: 0.35rem 1rem !important; 
}

/* Seletor de ALTA ESPECIFICIDADE para garantir que o fundo cinza seja sobreposto */
div[data-testid="stSidebar"] div[role="radiogroup"] > label.st-bq {
    background-color: var(--pet-blue) !important; /* ⬅ AZUL APLICADO */
}

/* Garante que o texto dentro do label selecionado seja branco */
.stRadio div > label.st-bq span {
    font-weight: 700 !important;
    color: white !important; 
}

/* Garante que o container do texto dentro do label selecionado não tenha fundo cinza */
.stRadio div > label.st-bq > div:last-child {
    background-color: transparent !important;
    color: white !important;
}

/* Remove qualquer sombreamento ou borda extra que o Streamlit possa adicionar */
.stRadio label.st-bq div[data-baseweb="radio"] {
    box-shadow: none !important;
    border: none !important;
}

/* === Estilo Específico para o Submenu de Alunos (DESTAQUE AZUL) === */
/* O submenu-alunos é a classe que envolve o radio do submenu */
.submenu-alunos .stRadio div > label.st-bq { 
    background-color: var(--pet-blue) !important; /* ⬅ AZUL APLICADO */
    border-radius: 6px !important; 
    font-weight: 700 !important;
    color: white !important;
    padding: 0.35rem 1rem !important;
}
.submenu-alunos .stRadio div > label.st-bq span { 
    font-weight: 700 !important;
    color: white !important;
}


/* === CAIXA AZUL – apenas no Início === */
.home-header {
    background: linear-gradient(135deg, var(--pet-blue) 0%, #2c5282 100%);
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
    color: var(--pet-blue); 
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
}
.page-title .icon {font-size: 2.2rem;}

/* === CORREÇÃO DE TEXTO NO CORPO PRINCIPAL === */
.block-container p, .block-container ul li, .block-container div[style*="font-size:18px"] {
    color: var(--text-color) !important; 
}
.block-container div[style*="background-color: #f0f2f6"] {
    background-color: var(--background-color-tertiary) !important;
    color: var(--text-color) !important; 
}


/* === CONTEÚDO PRINCIPAL === */
.block-container {
    padding-top: 1rem !important;
    padding-left: 5rem !important;
    padding-right: 5rem !important;
}

/* Oculta os botões Log out/Configurações usados anteriormente */
[key="logout_btn"], [key="settings_btn"] {
    display: none !important;
}
/* ================================================= */
/* === CORREÇÃO DEFINITIVA DO ESPAÇO FANTASMA NO MENU PRINCIPAL === */
.stRadio > div[role="radiogroup"] > div:first-child {
    display: none !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

.stRadio > div[role="radiogroup"] > div:nth-child(2) {
    margin-top: -8px !important;
    padding-top: 0 !important;
}

.sidebar-title {
    margin-bottom: 2px !important;
    padding-bottom: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Funções de cabeçalho, Dados e Lógica da Página
# -------------------------------------------------


def render_home_header():
    st.markdown("""
    <div class="home-header">
        <h1>
            <span class="icon">⚛</span> Bem-vindo(a) ao Dashboard PET Física – UNIFAP
        </h1>
    </div>
    """, unsafe_allow_html=True)


def render_page_title(title, icon=""):
    st.markdown(
        f'<div class="page-title"><span class="icon">{icon}</span> {title}</div>', unsafe_allow_html=True)


atividades = [
    {"Atividade": "Introdução à programação em Python",
        "Carga Horária": 100, "Início": "06/01/2025", "Fim": "31/12/2025"},
    {"Atividade": "Apostilas de Física", "Carga Horária": 100,
        "Início": "09/12/2024", "Fim": "31/12/2025"},
    {"Atividade": "Físicos da Alegria", "Carga Horária": 100,
        "Início": "06/01/2025", "Fim": "31/12/2025"},
    {"Atividade": "Iniciação Científica do PET Física",
        "Carga Horária": 100, "Início": "06/01/2025", "Fim": "31/12/2025"},
    {"Atividade": "Vídeo Aulas PET Física - UNIFAP", "Carga Horária": 100,
        "Início": "06/01/2025", "Fim": "31/12/2025"},
]
df = pd.DataFrame(atividades)
df["Início"] = pd.to_datetime(df["Início"], dayfirst=True)
df["Fim"] = pd.to_datetime(df["Fim"], dayfirst=True)

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

dados_alunos = [
    {"Nome": "Ana Silva", "Atividade": "Introdução à programação em Python",
        "Status": "Em Andamento", "Progresso (%)": 75, "Horas Registradas": 60},
    {"Nome": "Ana Silva", "Atividade": "Apostilas de Física",
        "Status": "Concluído", "Progresso (%)": 100, "Horas Registradas": 100},
    {"Nome": "Bruno Costa", "Atividade": "Introdução à programação em Python",
        "Status": "Em Andamento", "Progresso (%)": 50, "Horas Registradas": 50},
    {"Nome": "Bruno Costa", "Atividade": "Físicos da Alegria",
        "Status": "Não Iniciado", "Progresso (%)": 0, "Horas Registradas": 0},
    {"Nome": "Carla Dias", "Atividade": "Vídeo Aulas PET Física - UNIFAP",
        "Status": "Em Andamento", "Progresso (%)": 80, "Horas Registradas": 70},
    {"Nome": "Carla Dias", "Atividade": "Iniciação Científica do PET Física",
        "Status": "Em Andamento", "Progresso (%)": 30, "Horas Registradas": 30},
    {"Nome": "Carla Dias", "Atividade": "Apostilas de Física",
        "Status": "Em Andamento", "Progresso (%)": 20, "Horas Registradas": 20},
    {"Nome": "Angelo Haroldo Dos Santos Bonfim Junior", "Atividade": "Introdução à programação em Python",
        "Status": "Em Andamento", "Progresso (%)": 90, "Horas Registradas": 90},
]
df_alunos = pd.DataFrame(dados_alunos)
nomes_alunos_com_dados = df_alunos["Nome"].unique().tolist()
nomes_alunos_com_dados.sort()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.image("PET.png", width=200)
    
    # Opções do Menu Principal
    opcoes_menu_principal = ["Início", "Alunos", "Detalhes das Atividades"]

    if st.session_state.menu_principal:
        st.markdown('<span class="sidebar-title">Navegação</span>', unsafe_allow_html=True)
        
        # Determina o índice atual, com fallback seguro para a primeira opção
        try:
            indice_atual_main = opcoes_menu_principal.index(st.session_state.pagina_atual)
        except ValueError:
            indice_atual_main = 0 
        
        # === st.radio para o Menu Principal ===
        pagina_selecionada = st.radio(
            "Navegação Principal",
            opcoes_menu_principal,
            index=indice_atual_main,
            key="main_menu",
            label_visibility="collapsed",
        )
        
        # Lógica de Transição para o Submenu de Alunos
        if pagina_selecionada == "Alunos":
            # Define o primeiro aluno da lista como a página inicial do submenu
            st.session_state.pagina_atual = nomes_alunos_menu[0]
            st.session_state.menu_principal = False
            st.rerun()
        else:
            st.session_state.pagina_atual = pagina_selecionada

    else: # Submenu de Alunos
        st.markdown("### 👤 Lista de Alunos")

        # Botão Voltar ao Menu Principal
        with st.container(border=False):
            if st.button("⬅ Voltar ao Menu Principal", key="btn_voltar_menu"):
                st.session_state.menu_principal = True
                st.session_state.pagina_atual = "Início"
                st.rerun()

        st.markdown('<div class="submenu-alunos">', unsafe_allow_html=True)

        # Determina o índice atual do aluno (limpa espaços extras antes da comparação)
        index_aluno = 0
        try:
            # Encontra o índice na lista de alunos do menu
            pagina_limpa = st.session_state.pagina_atual.strip()
            nomes_limpos = [nome.strip() for nome in nomes_alunos_menu]
            index_aluno = nomes_limpos.index(pagina_limpa)
        except ValueError:
            # Se o valor atual da sessão não for um aluno válido, usa o primeiro
            index_aluno = 0 

        # === st.radio para o Submenu de Alunos ===
        pagina_selecionada_aluno = st.radio(
            "Selecione um Aluno",
            nomes_alunos_menu,
            index=index_aluno,
            key="submenu_alunos",
            label_visibility="collapsed")

        # Garante que a página atual seja o nome do aluno selecionado (mantendo a string original)
        st.session_state.pagina_atual = pagina_selecionada_aluno

        st.markdown('</div>', unsafe_allow_html=True)


pagina = st.session_state.pagina_atual

# -------------------------------------------------
# Páginas
# -------------------------------------------------

if pagina == "Início":
    render_home_header()
    st.markdown("""
    <div style="text-align:justify;font-size:18px;line-height:1.7;">
    Este painel foi criado para promover a <b>transparência e acompanhamento</b> das atividades do grupo PET Física da Universidade Federal do Amapá (UNIFAP).
    Aqui você encontrará informações sobre as ações desenvolvidas ao longo de 2025, com foco em ensino, pesquisa, extensão e inovação científica.
    </div>
    <ul style="font-size:17px;margin-top:20px;">
    <li><b>Introdução à Programação:</b> capacitação em Python para discentes e comunidade.</li>
    <li><b>Apostilas de Física:</b> elaboração de materiais didáticos gratuitos e acessíveis.</li>
    <li><b>Físicos da Alegria:</b> ações sociais e divulgação científica com empatia e solidariedade.</li>
    <li><b>Iniciação Científica:</b> incentivo à pesquisa, escrita científica e uso de LaTeX.</li>
    <li><b>Vídeo Aulas:</b> produção e publicação de conteúdos audiovisuais para ensino e popularização da física.</li>
    </ul>
    """, unsafe_allow_html=True)

elif pagina == "Detalhes das Atividades":
    render_page_title("Detalhes e Progresso das Atividades", "🔎")

    col_sel_atividade, col_sel_aluno = st.columns(2)

    with col_sel_atividade:
        atividade_sel = st.selectbox(
            "Selecione uma atividade:", df["Atividade"])

    with col_sel_aluno:
        opcoes_alunos_detalhes = ["Todos os Alunos"] + nomes_alunos_com_dados
        aluno_sel = st.selectbox(
            "Selecione o aluno para filtrar:", opcoes_alunos_detalhes)

    if not df[df["Atividade"] == atividade_sel].empty:
        info = df[df["Atividade"] == atividade_sel].iloc[0]
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 8px;">
        *Atividade:* {info['Atividade']} | *Carga Horária:* {info['Carga Horária']}h | *Período:* {info['Início'].strftime('%d/%m/%Y')} - {info['Fim'].strftime('%d/%m/%Y')}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Atividade selecionada não encontrada.")

    st.divider()

    df_filtrado_atividade = df_alunos[df_alunos["Atividade"] == atividade_sel].copy(
    )

    if aluno_sel != "Todos os Alunos":
        df_final = df_filtrado_atividade[df_filtrado_atividade["Nome"] == aluno_sel]
        st.markdown(f"### Desempenho de *{aluno_sel}* em {atividade_sel}")
    else:
        df_final = df_filtrado_atividade
        st.markdown(f"### Desempenho de Todos os Alunos em {atividade_sel}")

    if not df_final.empty:
        colunas_tabela = ["Nome", "Status",
                            "Progresso (%)", "Horas Registradas"]
        if aluno_sel != "Todos os Alunos":
            colunas_tabela.remove("Nome")

        st.dataframe(
            df_final[colunas_tabela],
            use_container_width=True,
            hide_index=True
        )

        if len(df_final["Nome"].unique()) >= 1:
            st.markdown("### Gráfico de Progresso")

            if aluno_sel != "Todos os Alunos":
                fig_progresso = px.pie(
                    df_final,
                    names=['Progresso Registrado', 'Faltante'],
                    values=[
                        df_final["Progresso (%)"].iloc[0], 100 - df_final["Progresso (%)"].iloc[0]],
                    title=f"Progresso de {aluno_sel} (%)",
                    color_discrete_sequence=['#1f3a5f', '#ccc'],
                )
                fig_progresso.update_traces(
                    textinfo='percent+value', texttemplate='%{value}%')
            else:
                fig_progresso = px.bar(
                    df_final,
                    x="Nome",
                    y="Progresso (%)",
                    color="Status",
                    title=f"Progresso dos alunos em {atividade_sel}",
                    range_y=[0, 100],
                    color_discrete_map={
                        'Concluído': 'green', 'Em Andamento': 'orange', 'Não Iniciado': 'red'}
                )
                fig_progresso.update_layout(
                    xaxis_title="Aluno", yaxis_title="Progresso (%)")

            st.plotly_chart(fig_progresso, use_container_width=True)

    else:
        if aluno_sel != "Todos os Alunos":
            st.info(
                f"O aluno *{aluno_sel}* não tem registros de participação na atividade *{atividade_sel}*.")
        else:
            st.info(
                f"Nenhum aluno encontrado com registro de desempenho na atividade *{atividade_sel}*.")

elif pagina in nomes_alunos_menu:
    aluno_selecionado = pagina

    render_page_title(
        f"Desempenho Individual de {aluno_selecionado.strip()}", "👤")

    # Garante que o nome do aluno selecionado corresponda ao nome nos dados, ignorando espaços extras
    nome_nos_dados = [
        n for n in nomes_alunos_com_dados if n.strip() == aluno_selecionado.strip()]

    if nome_nos_dados:
        # Pega o nome padronizado do df_alunos
        nome_completo = nome_nos_dados[0]
        df_do_aluno = df_alunos[df_alunos["Nome"] == nome_completo]

        st.markdown(f"### Resumo de {nome_completo}")

        total_atividades = df_do_aluno.shape[0]
        progresso_medio = df_do_aluno["Progresso (%)"].mean()
        horas_totais = df_do_aluno["Horas Registradas"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Atividades", f"{total_atividades}")
        col2.metric("Progresso Médio", f"{progresso_medio:.1f}%")
        col3.metric("Total de Horas", f"{horas_totais}h")

        st.divider()

        st.markdown(f"### Detalhes das Atividades")
        st.dataframe(
            df_do_aluno[["Atividade", "Status",
                            "Progresso (%)", "Horas Registradas"]],
            use_container_width=True,
            hide_index=True # Adicionando hide_index para consistência e clareza
        )

        st.markdown("### Gráfico de Progresso")
        fig_progresso = px.bar(
            df_do_aluno,
            x="Atividade",
            y="Progresso (%)",
            color="Atividade",
            title="Progresso por Atividade",
            range_y=[0, 100]
        )
        st.plotly_chart(fig_progresso, use_container_width=True)
    else:
        st.warning(
            f"Dados de desempenho para *{aluno_selecionado.strip()}* não encontrados no DataFrame df_alunos. Por favor, adicione as informações deste aluno ao seu dados_alunos no script para que o painel funcione.")

elif pagina == "Alunos":
    # Garante que a transição para o submenu inicie na página do primeiro aluno, não em "Alunos"
    # Embora a lógica acima trate disso, essa checagem previne um estado inválido se o rerender for muito rápido
    st.session_state.menu_principal = False
    st.session_state.pagina_atual = nomes_alunos_menu[0]
    st.rerun()