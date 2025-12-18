import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import math

# -------------------------------------------------
# 1. Configuração da Página e Estilo Adaptativo
# -------------------------------------------------
st.set_page_config(page_title="Dashboard PET Física 2025", layout="wide")

st.markdown("""
<style>
    .custom-card {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .metric-title { color: var(--text-color); opacity: 0.8; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 8px; }
    .metric-value { color: var(--text-color); font-size: 28px; font-weight: 800; margin: 0; }
    .metric-sub { font-size: 14px; margin-top: 5px; }
    .trend-up { color: #28a745; font-weight: bold; }
    .trend-neutral { color: var(--text-color); opacity: 0.6; }

    /* Título da Sidebar Redimensionado e Alinhado à Esquerda */
    .sidebar-title {
        font-size: 1.9rem !important; /* Tamanho levemente ajustado para o alinhamento */
        font-weight: 800 !important;
        text-align: left !important; /* Movido para a esquerda */
        padding-left: 20px; /* Recuo da borda esquerda */
        color: var(--text-color);
        padding-top: 15px;
        padding-bottom: 15px;
        display: block;
        width: 100%;
    }
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 2. Dados de Simulação
# -------------------------------------------------
nomes_alunos_menu = sorted([
    "Angelo Haroldo Dos Santos", "Felipe De Souza Pereira", "Ian Rodrigo Colares Dias",
    "Jaimison Costa De Souza", "Joao Maciel Dos Santos", "Luiz Eduardo Barbosa",
    "Mayara Pamplona", "Theyllorran Gomes Araujo"
])

def get_student_data(nome):
    return {
        "ENTRADA": "10/02/2023", "DIAS": 452, "CRA_ATUAL": 8.5,
        "CRA_HIST": [7.2, 7.8, 8.2, 8.5], "SEMESTRES": ["2023.1", "2023.2", "2024.1", "2024.2"],
        "APRESENTACOES": 3, "PUBLICACOES": 2, "HORAS_REUNIAO": 68, "PRESENCA_PCT": 92,
        "TAREFAS_TOTAL": 25, "TAREFAS_ENTREGUES": 23,
        "CONTRIBUICOES": {
            "Minicursos": [3, 2, 3, 1, 4, 2, 1],
            "Palestras": [4, 4, 4, 4, 3, 2, 2],
            "Monitorias": [3, 4, 3, 5, 3, 4, 3]
        }
    }

# -------------------------------------------------
# 3. Funções de Gráficos (Incluindo Agulha)
# -------------------------------------------------

def plot_gauge_tasks(entregue, total):
    pct = (entregue / total) * 100
    
    # Cálculos para a Agulha (Trigonometria)
    theta = 180 - (pct * 1.8)
    r = 0.85 
    x_head = r * math.cos(math.radians(theta))
    y_head = r * math.sin(math.radians(theta))

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={'suffix': "%", 'font': {'size': 50, 'color': "var(--text-color)"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'visible': False},
            'bar': {'color': "rgba(0,0,0,0)"}, 
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [
                {'range': [0, 33.3], 'color': "#ea4335"},
                {'range': [33.3, 66.6], 'color': "#fbbc04"},
                {'range': [66.6, 100], 'color': "#28a745"}
            ],
        }
    ))

    fig.update_layout(
        shapes=[
            dict(type='line', x0=0, y0=0, x1=x_head, y1=y_head, 
                 line=dict(color='white', width=4), xref='x', yref='y'),
            dict(type='circle', x0=-0.05, y0=-0.05, x1=0.05, y1=0.05, 
                 fillcolor='white', line=dict(color='white'), xref='x', yref='y')
        ],
        xaxis=dict(range=[-1, 1], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-0.1, 1.1], showgrid=False, zeroline=False, visible=False),
        title={'text': "Taxa de Conclusão (Assiduidade)", 'x': 0.5, 'y': 0.9, 'xanchor': 'center'},
        paper_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=30, r=30, t=80, b=40),
        annotations=[go.layout.Annotation(x=0, y=-0.1, text=f"<b>{entregue} de {total} tarefas entregues</b>", showarrow=False, font=dict(size=14, color="gray"))]
    )
    return fig

def plot_cra_evolution(hist, semestres):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=semestres, y=hist, mode='lines+markers+text', 
        text=[f"<b>{v}</b>" for v in hist], textposition="top center",
        line=dict(color='#58A6FF', width=4), marker=dict(size=10, color='#58A6FF', line=dict(color='white', width=2)),
        fill='tozeroy', fillcolor='rgba(88, 166, 255, 0.1)'))
    fig.add_annotation(x=semestres[-1], y=hist[-1], text="Melhora de Rendimento", showarrow=True, arrowhead=2, bgcolor="#28a745", font=dict(color="white"))
    fig.update_layout(title="Evolução do CRA Semestral", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"), height=350, yaxis=dict(range=[0, 10]))
    return fig

def plot_monthly_activities(data):
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul']
    fig = go.Figure()
    colors = {'Minicursos': '#58A6FF', 'Palestras': '#BC8CFF', 'Monitorias': '#F78166'}
    for label, values in data.items():
        fig.add_trace(go.Bar(name=label, x=meses, y=values, marker_color=colors[label]))
    fig.update_layout(barmode='stack', title="Contribuições Mensais", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, font=dict(color="gray"), legend=dict(orientation="h", y=1.1))
    return fig

# -------------------------------------------------
# 4. Navegação e Sidebar
# -------------------------------------------------
if 'menu_principal' not in st.session_state: st.session_state.menu_principal = True

with st.sidebar:
    st.markdown('<span class="sidebar-title">⚛ PET Física</span>', unsafe_allow_html=True)
    st.markdown("---")
    if st.session_state.menu_principal:
        nav = st.radio("Navegação", ["Início", "Painel de Alunos"])
        if nav == "Painel de Alunos":
            st.session_state.menu_principal = False
            st.rerun()
    else:
        if st.button("← Voltar ao Início"):
            st.session_state.menu_principal = True
            st.rerun()
        st.subheader("Bolsistas")
        aluno_selecionado = st.radio("Selecione:", nomes_alunos_menu, label_visibility="collapsed")

# -------------------------------------------------
# 5. Renderização
# -------------------------------------------------
if st.session_state.menu_principal:
    st.title("Bem-vindo ao Dashboard PET Física UNIFAP")
    st.info("Acesse a aba 'Painel de Alunos' no menu lateral para visualizar as métricas.")
else:
    data = get_student_data(aluno_selecionado)
    st.header(f"Performance: {aluno_selecionado}")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="custom-card"><div class="metric-title">📅 Tempo no PET</div><div class="metric-value">{data["DIAS"]} DIAS</div><div class="metric-sub">Entrada: {data["ENTRADA"]}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="custom-card"><div class="metric-title">🎓 CRA Atual</div><div class="metric-value">{data["CRA_ATUAL"]} ↗</div><div class="metric-sub trend-up">Tendência de Alta</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="custom-card"><div class="metric-title">📚 Produção</div><div class="metric-value">{data["APRESENTACOES"]} Apres.</div><div class="metric-sub">Eventos e Artigos</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="custom-card"><div class="metric-title">🤝 Presença</div><div class="metric-value">{data["PRESENCA_PCT"]}%</div><div class="metric-sub">Reuniões Totais</div></div>', unsafe_allow_html=True)

    g1, g2 = st.columns([1.8, 1.2])
    with g1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_cra_evolution(data['CRA_HIST'], data['SEMESTRES']), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with g2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_gauge_tasks(data['TAREFAS_ENTREGUES'], data['TAREFAS_TOTAL']), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.plotly_chart(plot_monthly_activities(data['CONTRIBUICOES']), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("Dashboard PET Física UNIFAP © 2025")
