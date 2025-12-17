import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# -------------------------------------------------
# 1. Configuração da Página e Estilo Adaptativo
# -------------------------------------------------
st.set_page_config(page_title="Dashboard PET Física 2025", layout="wide")

# CSS utilizando variáveis nativas do Streamlit (--secondary-background-color, --text-color, etc.)
st.markdown("""
<style>
    /* Card que se adapta automaticamente ao tema */
    .custom-card {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Textos dinâmicos */
    .metric-title { 
        color: var(--text-color); 
        opacity: 0.8;
        font-size: 13px; 
        font-weight: bold; 
        text-transform: uppercase; 
        margin-bottom: 8px; 
    }
    .metric-value { 
        color: var(--text-color); 
        font-size: 28px; 
        font-weight: 800; 
        margin: 0; 
    }
    .metric-sub { font-size: 14px; margin-top: 5px; }
    .trend-up { color: #28a745; font-weight: bold; }
    .trend-neutral { color: var(--text-color); opacity: 0.6; }

    /* Ajuste para remover margens extras do Streamlit */
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 2. Dados e Lógica de Simulação
# -------------------------------------------------
TODAY = datetime.date(2025, 11, 26)

nomes_alunos_menu = sorted([
    "Angelo Haroldo Dos Santos", "Felipe De Souza Pereira", "Ian Rodrigo Colares Dias",
    "Jaimison Costa De Souza", "Joao Maciel Dos Santos", "Luiz Eduardo Barbosa",
    "Mayara Pamplona", "Theyllorran Gomes Araujo"
])

def get_student_data(nome):
    # Mock de dados para demonstração
    return {
        "ENTRADA": "10/02/2023",
        "DIAS": 452,
        "CRA_ATUAL": 8.5,
        "CRA_HIST": [7.2, 7.8, 8.2, 8.5],
        "SEMESTRES": ["2023.1", "2023.2", "2024.1", "2024.2"],
        "APRESENTACOES": 3,
        "PUBLICACOES": 2,
        "HORAS_REUNIAO": 68,
        "PRESENCA_PCT": 92,
        "TAREFAS_TOTAL": 25,
        "TAREFAS_ENTREGUES": 23,
        "CONTRIBUICOES": {
            "Minicursos": [3, 2, 3, 1, 4, 2, 1],
            "Palestras": [4, 4, 4, 4, 3, 2, 2],
            "Monitorias": [3, 4, 3, 5, 3, 4, 3]
        }
    }

# -------------------------------------------------
# 3. Funções de Gráficos (Respeitando o Tema)
# -------------------------------------------------
def plot_cra_evolution(hist, semestres):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=semestres, y=hist, mode='lines+markers+text',
        text=[f"<b>{v}</b>" for v in hist], textposition="top center",
        line=dict(color='#58A6FF', width=4),
        marker=dict(size=10, color='#58A6FF', line=dict(color='white', width=2)),
        fill='tozeroy', fillcolor='rgba(88, 166, 255, 0.1)'
    ))
    
    fig.add_annotation(x=semestres[-1], y=hist[-1], text="Melhora de Rendimento",
                       showarrow=True, arrowhead=2, bgcolor="#28a745", font=dict(color="white"))
    
    fig.update_layout(
        title="Evolução do CRA/IRA Semestral",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="sans-serif"), height=350, margin=dict(l=0, r=0, t=50, b=0),
        yaxis=dict(range=[0, 10], gridcolor="rgba(128,128,128,0.2)"), 
        xaxis=dict(gridcolor="rgba(128,128,128,0.2)")
    )
    return fig

def plot_gauge_tasks(entregue, total):
    pct = (entregue/total)*100
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=pct,
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "#28a745"},
            'bgcolor': "rgba(128,128,128,0.1)",
            'steps': [
                {'range': [0, 50], 'color': "#ea4335"},
                {'range': [50, 85], 'color': "#fbbc04"},
                {'range': [85, 100], 'color': "#28a745"}]
        }
    ))
    fig.update_layout(
        title={'text': "Taxa de Conclusão", 'x': 0.5, 'y': 0.8},
        paper_bgcolor='rgba(0,0,0,0)',
        height=350, margin=dict(l=20, r=20, t=80, b=0),
        annotations=[go.layout.Annotation(x=0.5, y=0.1, text=f"{entregue} de {total} tarefas", showarrow=False)]
    )
    return fig

def plot_monthly_activities(data):
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul']
    fig = go.Figure()
    colors = {'Minicursos': '#58A6FF', 'Palestras': '#BC8CFF', 'Monitorias': '#F78166'}
    
    for label, values in data.items():
        fig.add_trace(go.Bar(name=label, x=meses, y=values, marker_color=colors[label]))

    fig.update_layout(
        barmode='stack', title="Contribuições Mensais (Atividades)",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=400, margin=dict(t=50),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.2)")
    return fig

# -------------------------------------------------
# 4. Navegação e Sidebar
# -------------------------------------------------
if 'menu_principal' not in st.session_state:
    st.session_state.menu_principal = True

with st.sidebar:
    st.title("⚛ PET Física")
    st.markdown("---")
    if st.session_state.menu_principal:
        menu = st.radio("Navegação", ["Início", "Alunos"])
        if menu == "Alunos":
            st.session_state.menu_principal = False
            st.rerun()
    else:
        if st.button("← Voltar ao Menu"):
            st.session_state.menu_principal = True
            st.rerun()
        st.subheader("Bolsistas")
        aluno_selecionado = st.radio("Selecione:", nomes_alunos_menu, label_visibility="collapsed")

# -------------------------------------------------
# 5. Renderização Principal
# -------------------------------------------------
if st.session_state.menu_principal:
    st.title("Bem-vindo ao Dashboard PET Física")
    st.write("Utilize o menu lateral para navegar entre as seções e visualizar o desempenho dos alunos.")
    st.info("Dica: Este painel adapta-se automaticamente ao tema claro ou escuro do seu sistema.")
else:
    data = get_student_data(aluno_selecionado)
    st.header(f"{aluno_selecionado}")
    
    # LINHA 1: Cards de Métricas (KPIs)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""<div class="custom-card">
            <div class="metric-title">📅 Tempo no PET</div>
            <div class="metric-value">{data['DIAS']} DIAS</div>
            <div class="metric-sub trend-neutral">Entrada: {data['ENTRADA']}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="custom-card">
            <div class="metric-title">🎓 Média CRA Atual</div>
            <div class="metric-value">{data['CRA_ATUAL']} ↗</div>
            <div class="metric-sub trend-up">Tendência de Alta</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="custom-card">
            <div class="metric-title">📚 Produção</div>
            <div class="metric-value">{data['APRESENTACOES']} Apres. | {data['PUBLICACOES']} Publ.</div>
            <div class="metric-sub trend-neutral">Atividades registradas</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="custom-card">
            <div class="metric-title">🤝 Reuniões</div>
            <div class="metric-value">{data['HORAS_REUNIAO']}h Totais</div>
            <div class="metric-sub trend-up">{data['PRESENCA_PCT']}% Presença</div>
        </div>""", unsafe_allow_html=True)

    # LINHA 2: Gráficos de Evolução e Assiduidade
    g1, g2 = st.columns([2, 1])
    with g1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_cra_evolution(data['CRA_HIST'], data['SEMESTRES']), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with g2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_gauge_tasks(data['TAREFAS_ENTREGUES'], data['TAREFAS_TOTAL']), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # LINHA 3: Atividades Mensais
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.plotly_chart(plot_monthly_activities(data['CONTRIBUICOES']), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.caption(f"Dashboard atualizado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")


    # Rodapé

st.sidebar.markdown("---")

st.sidebar.caption("Dashboard PET Física UNIFAP © 2025")