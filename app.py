import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# --- CONFIGURATION INITIALE ---
st.set_page_config(
    page_title="Lean Six Sigma Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS PERSONNALISÉ (Style Apple / Glassmorphism) ---
# Ce bloc assure l'esthétique minimaliste et professionnelle
st.markdown("""
    <style>
    /* Animation d'entrée */
    .stApp {
        animation: fadeIn 1.2s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Titres et Typographie */
    h1 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica;
        font-weight: 700;
        letter-spacing: -0.05rem;
        margin-bottom: 0px !important;
    }
    .subtitle {
        color: #86868b;
        font-size: 1.2rem;
        font-weight: 400;
        margin-top: -10px;
        margin-bottom: 30px;
    }

    /* Cartes KPI Glassmorphism */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px !important;
        transition: transform 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
    }

    /* Onglets / Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 10px;
        color: #86868b;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 113, 227, 0.1) !important;
        color: #0071e3 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SECTION 1 : INTRODUCTION DMAIC (Nouveau)
# ==========================================
st.title("Simulation Lean Six Sigma")
st.markdown("<div class='subtitle'>Optimisation Industrielle – Approche DMAIC</div>", unsafe_allow_html=True)

st.markdown("""
Cette application simule une ligne de production (votre projet de station de lavage ou logistique) 
pour analyser l'impact du **Lean Six Sigma** sur la performance globale.
""")

# Objectifs visuels
col_obj1, col_obj2, col_obj3 = st.columns(3)
with col_obj1:
    st.success("⏱ **Réduire le temps** (Cycle Time)")
with col_obj2:
    st.error("❌ **Réduire les défauts** (Qualité)")
with col_obj3:
    st.info("📈 **Améliorer la productivité**")

st.divider()

# ==========================================
# SECTION 2 : LOGIQUE DE CALCUL & STYLE
# ==========================================
def calculate_metrics(production, lead_time, defects, downtime):
    # Calculs basés sur vos besoins en génie industriel
    ct = lead_time / production if production > 0 else 0
    dr = (defects / production) * 100 if production > 0 else 0
    dt = (downtime / lead_time) * 100 if lead_time > 0 else 0
    return ct, dr, dt

def apply_chart_style(fig, title, y_label):
    fig.update_layout(
        title=title,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="-apple-system",
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified"
    )
    fig.update_xaxes(showgrid=False, linecolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(title_text=y_label, showgrid=True, gridcolor='rgba(128,128,128,0.1)')
    return fig

# ==========================================
# SECTION 3 : INTERFACE UTILISATEUR (TABS)
# ==========================================
t1, t2, t3 = st.tabs(["📊 Round 1 (Initial)", "🚀 Round 2 (Optimisé)", "🏆 Comparaison & Contrôle"])

# --- ROUND 1 ---
with t1:
    st.subheader("Données de Base (Situation Actuelle)")
    c1, c2 = st.columns(2)
    with c1:
        p1 = st.number_input("Unités produites (R1)", value=20, key="p1")
        lt1 = st.number_input("Temps total (sec) (R1)", value=300, key="lt1")
    with c2:
        def1 = st.number_input("Nombre de défauts (R1)", value=8, key="def1")
        dt1 = st.number_input("Temps mort (sec) (R1)", value=60, key="dt1")
    
    res_ct1, res_dr1, res_dt1 = calculate_metrics(p1, lt1, def1, dt1)
    
    # Affichage immédiat
    m1, m2, m3 = st.columns(3)
    m1.metric("Cycle Time", f"{res_ct1:.1f}s")
    m2.metric("Defect Rate", f"{res_dr1:.1f}%")
    m3.metric("Downtime", f"{res_dt1:.1f}%")

# --- ROUND 2 ---
with t2:
    st.subheader("Données après Amélioration (Future)")
    c3, c4 = st.columns(2)
    with c3:
        p2 = st.number_input("Unités produites (R2)", value=35, key="p2")
        lt2 = st.number_input("Temps total (sec) (R2)", value=300, key="lt2")
    with c4:
        def2 = st.number_input("Nombre de défauts (R2)", value=2, key="def2")
        dt2 = st.number_input("Temps mort (sec) (R2)", value=30, key="dt2")
        
    res_ct2, res_dr2, res_dt2 = calculate_metrics(p2, lt2, def2, dt2)
    
    m4, m5, m6 = st.columns(3)
    m4.metric("Cycle Time", f"{res_ct2:.1f}s")
    m5.metric("Defect Rate", f"{res_dr2:.1f}%")
    m6.metric("Downtime", f"{res_dt2:.1f}%")

# --- COMPARISON & CONTROL CHARTS ---
with t3:
    st.subheader("Analyse de l'Amélioration")
    
    # KPIs Comparatifs
    k1, k2, k3 = st.columns(3)
    k1.metric("Cycle Time", f"{res_ct2:.1f}s", delta=f"{res_ct2-res_ct1:.1f}s", delta_color="inverse")
    k2.metric("Defect Rate", f"{res_dr2:.1f}%", delta=f"{res_dr2-res_dr1:.1f}%", delta_color="inverse")
    k3.metric("Downtime", f"{res_dt2:.1f}%", delta=f"{res_dt2-res_dt1:.1f}%", delta_color="inverse")

    st.markdown("---")
    
    # Cartes de Contrôle (Statistique Industrielle)
    st.subheader("Cartes de Contrôle $\\bar{X}$ & $R$ (Stabilité)")
    st.info("Ces graphiques utilisent une simulation de 20 sous-groupes basée sur vos résultats du Round 2.")
    
    # Simulation logic
    n_subgroups = 20
    x_bar, r_val = [], []
    sigma = res_ct2 * 0.05 if res_ct2 > 0 else 1
    
    for _ in range(n_subgroups):
        samples = [random.gauss(res_ct2, sigma) for _ in range(5)]
        x_bar.append(sum(samples)/5)
        r_val.append(max(samples)-min(samples))
        
    # Calcul des limites (Constantes pour n=5: A2=0.577, D4=2.114)
    x_double_bar = sum(x_bar)/20
    r_bar = sum(r_val)/20
    ucl_x, lcl_x = x_double_bar + 0.577*r_bar, x_double_bar - 0.577*r_bar
    ucl_r = 2.114 * r_bar
    
    gc1, gc2 = st.columns(2)
    
    with gc1:
        fig_x = go.Figure()
        fig_x.add_trace(go.Scatter(y=x_bar, mode='lines+markers', line_color='#0071e3', name='Moyenne'))
        fig_x.add_hline(y=ucl_x, line_dash="dash", line_color="#ff3b30", annotation_text="UCL")
        fig_x.add_hline(y=lcl_x, line_dash="dash", line_color="#ff3b30", annotation_text="LCL")
        fig_x.add_hline(y=x_double_bar, line_color="#34c759", annotation_text="X̄")
        st.plotly_chart(apply_chart_style(fig_x, "Carte des Moyennes ($\\bar{X}$)", "Secondes"), use_container_width=True)

    with gc2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(y=r_val, mode='lines+markers', line_color='#bf5af2', name='Étendue'))
        fig_r.add_hline(y=ucl_r, line_dash="dash", line_color="#ff3b30", annotation_text="UCL")
        fig_r.add_hline(y=r_bar, line_color="#34c759", annotation_text="R̄")
        st.plotly_chart(apply_chart_style(fig_r, "Carte des Étendues ($R$)", "Variation (sec)"), use_container_width=True)

    # Footer minimalist
    st.markdown("<br><p style='text-align: center; color: #86868b;'>Lean Six Sigma Dashboard | DMAIC Approach</p>", unsafe_allow_html=True)
