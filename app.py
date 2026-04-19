import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LSS Dashboard Pro", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADAPTIVE CSS (All Original Styling Preserved) ---
st.markdown("""
    <style>
    /* TAB SWITCHING ANIMATION */
    div[data-testid="stVerticalBlock"] > div {
        animation: tabFadeIn 0.6s cubic-bezier(0.25, 1, 0.5, 1);
    }
    @keyframes tabFadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Apple-style bold clean headers */
    h1 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 700;
        color: var(--text-color) !important;
        font-size: 3.5rem !important;
        margin-bottom: 0px !important;
        letter-spacing: -0.05rem;
    }
    
    h3 {
        font-weight: 600;
        color: var(--text-color) !important; 
        margin-top: 2rem !important;
        font-family: -apple-system, sans-serif;
    }

    /* Adaptive Glassmorphism KPI Cards */
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08); 
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 22px;
        padding: 25px 30px !important;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 50px 0 rgba(0, 0, 0, 0.15);
        background: rgba(128, 128, 128, 0.12);
    }
    
    .stDataFrame {
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(128, 128, 128, 0.1);
    }

    /* PURE CSS ANIMATED LOGO */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 20px;
    }
    .lss-logo {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #0071e3 0%, #bf5af2 100%);
        border-radius: 18px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 36px;
        font-weight: bold;
        font-family: -apple-system, sans-serif;
        box-shadow: 0 12px 24px rgba(0, 113, 227, 0.3);
        animation: logoPulse 3s infinite alternate ease-in-out;
    }
    .logo-text {
        font-family: -apple-system, sans-serif;
        font-weight: 600;
        font-size: 1.2rem;
        color: var(--text-color);
        line-height: 1.1;
        text-align: right;
    }
    @keyframes logoPulse {
        0% { transform: scale(1) rotate(0deg); box-shadow: 0 8px 20px rgba(0, 113, 227, 0.2); }
        100% { transform: scale(1.08) rotate(3deg); box-shadow: 0 18px 35px rgba(191, 90, 242, 0.4); }
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER SECTION ---
col_title, col_logo = st.columns([3, 1])
with col_title:
    st.title("Lean Six Sigma")
    st.markdown("<p style='color: #86868b; font-size: 1.3rem; margin-top: -10px;'>High-Performance Industrial Intelligence</p>", unsafe_allow_html=True)
with col_logo:
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text">LEAN<br>SIX SIGMA</div>
            <div class="lss-logo">Σ</div>
        </div>
    """, unsafe_allow_html=True)

# --- 4. DMAIC INTRODUCTION (NEW COMPONENT) ---
st.markdown("### 🎯 Simulation Lean Six Sigma – Approche DMAIC")
st.markdown("""
Cette interface analyse l'impact des optimisations sur une ligne de production.
Nous comparons une situation initiale (Round 1) à un processus amélioré (Round 2).
""")

col_goal1, col_goal2, col_goal3 = st.columns(3)
col_goal1.success("⏱ **Réduire le Temps** (Lead Time)")
col_goal2.error("❌ **Réduire les Défauts** (Qualité/FPY)")
col_goal3.info("📈 **Améliorer la Productivité** (OEE)")

st.divider()

# --- 5. CORE CALCULATION ENGINE (New Formulas Integrated) ---
def calculate_industrial_kpis(unites, temps_total, defauts, temps_mort):
    if unites <= 0 or temps_total <= 0:
        return [0] * 7
    
    # User's Precise Formulas
    cycle_time = temps_total / unites
    lead_time = temps_total / unites
    wip = (unites * cycle_time) / temps_total
    fpy = (unites - defauts) / unites
    va_rate = (temps_total - temps_mort) / temps_total
    productivite = unites / (temps_total / 60)
    
    # OEE Calculation (Disponibilité * Performance * Qualité)
    # Using VA Rate as Availability, FPY as Quality, and Performance assumed at 100%
    oee = va_rate * 1.0 * fpy
    
    return cycle_time, lead_time, wip, fpy, va_rate, productivite, oee

# --- 6. TABS NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["📊 Round 1 (Initial)", "🚀 Round 2 (Optimisé)", "🏆 Analyse & Contrôle"])

# ==========================================
# TAB 1: ROUND 1
# ==========================================
with tab1:
    st.subheader("Collecte des Données - Situation Actuelle")
    col1, col2 = st.columns(2)
    
    with col1:
        u1 = st.number_input("Unités produites - R1", value=20, min_value=0, step=1, key="u1")
        tt1 = st.number_input("Temps total (sec) - R1", value=300, min_value=0, step=10, key="tt1")
    with col2:
        d1 = st.number_input("Nombre de défauts - R1", value=8, min_value=0, step=1, key="d1")
        tm1 = st.number_input("Temps mort (sec) - R1", value=60, min_value=0, step=5, key="tm1")

    # Execute Logic
    ct1, lt1, wip1, fpy1, va1, p1, oee1 = calculate_industrial_kpis(u1, tt1, d1, tm1)
    
    st.markdown("### Indicateurs Clés (KPIs)")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("OEE (Rendement)", f"{oee1*100:.1f}%")
    kpi2.metric("First Pass Yield", f"{fpy1*100:.1f}%")
    kpi3.metric("Productivité", f"{p1:.1f} u/min")

# ==========================================
# TAB 2: ROUND 2
# ==========================================
with tab2:
    st.subheader("Collecte des Données - Post-Amélioration")
    col3, col4 = st.columns(2)
    
    with col3:
        u2 = st.number_input("Unités produites - R2", value=35, min_value=0, step=1, key="u2")
        tt2 = st.number_input("Temps total (sec) - R2", value=300, min_value=0, step=10, key="tt2")
    with col4:
        d2 = st.number_input("Nombre de défauts - R2", value=2, min_value=0, step=1, key="d2")
        tm2 = st.number_input("Temps mort (sec) - R2", value=30, min_value=0, step=5, key="tm2")

    # Execute Logic
    ct2, lt2, wip2, fpy2, va2, p2, oee2 = calculate_industrial_kpis(u2, tt2, d2, tm2)
    
    st.markdown("### Indicateurs Clés (KPIs)")
    kpi4, kpi5, kpi6 = st.columns(3)
    kpi4.metric("OEE (Rendement)", f"{oee2*100:.1f}%")
    kpi5.metric("First Pass Yield", f"{fpy2*100:.1f}%")
    kpi6.metric("Productivité", f"{p2:.1f} u/min")

# ==========================================
# TAB 3: COMBINED ANALYSIS & CONTROL
# ==========================================
with tab3:
    st.subheader("Synthèse de la Performance")
    
    # Deltas Row
    diff_ct = ct2 - ct1
    diff_oee = (oee2 - oee1) * 100
    diff_p = p2 - p1

    comp1, comp2, comp3 = st.columns(3)
    comp1.metric("Cycle Time", f"{ct2:.1f}s", delta=f"{diff_ct:.1f}s", delta_color="inverse")
    comp2.metric("OEE Global", f"{oee2*100:.1f}%", delta=f"{diff_oee:.1f}%")
    comp3.metric("Productivité", f"{p2:.1f} u/min", delta=f"{diff_p:.1f}")
    
    st.markdown("<hr style='border: 0.5px solid rgba(128,128,128,0.2);'>", unsafe_allow_html=True)

    # --- COMPARISON TABLE (DataFrame) ---
    st.subheader("Tableau de Bord Comparatif")
    metrics = ["OEE (%)", "Lead Time (s)", "WIP", "First Pass Yield (%)", "Taux VA (%)", "Productivité"]
    before = [oee1*100, lt1, wip1, fpy1*100, va1*100, p1]
    after = [oee2*100, lt2, wip2, fpy2*100, va2*100, p2]
    
    df_compare = pd.DataFrame({
        "Métrique Industrielle": metrics,
        "Avant (R1)": [f"{v:.2f}" for v in before],
        "Après (R2)": [f"{v:.2f}" for v in after],
        "Impact (%)": [f"{((after[i]-before[i])/before[i]*100):+.1f}%" if before[i] != 0 else "N/A" for i in range(len(metrics))]
    })
    st.dataframe(df_compare, use_container_width=True, hide_index=True)

    # --- BAR CHARTS VISUALIZATION ---
    st.markdown("<br>", unsafe_allow_html=True)
    chart_col1, chart_col2, chart_col3 = st.columns(3)

    def apple_chart_style(fig, title_text):
        fig.update_layout(
            title=title_text,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_family="-apple-system, BlinkMacSystemFont",
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.15)')
        return fig

    with chart_col1:
        f1 = px.bar(x=["R1", "R2"], y=[oee1*100, oee2*100], color=["R1", "R2"], text_auto='.1f',
                    color_discrete_map={"R1": "#86868b", "R2": "#0071e3"})
        st.plotly_chart(apple_chart_style(f1, "Évolution OEE (%)"), use_container_width=True)

    with chart_col2:
        f2 = px.bar(x=["R1", "R2"], y=[fpy1*100, fpy2*100], color=["R1", "R2"], text_auto='.1f',
                    color_discrete_map={"R1": "#86868b", "R2": "#ff3b30"})
        st.plotly_chart(apple_chart_style(f2, "Qualité (FPY) %"), use_container_width=True)

    with chart_col3:
        f3 = px.bar(x=["R1", "R2"], y=[p1, p2], color=["R1", "R2"], text_auto='.1f',
                    color_discrete_map={"R1": "#86868b", "R2": "#bf5af2"})
        st.plotly_chart(apple_chart_style(f3, "Productivité"), use_container_width=True)

    # ==========================================
    # STATISTICAL CONTROL CHARTS (FULL LOGIC)
    # ==========================================
    st.markdown("<br><br><hr style='border: 0.5px solid rgba(128,128,128,0.2);'>", unsafe_allow_html=True)
    st.subheader("Cartes de Contrôle (X̄ & R) – Stabilité Post-Optimisation")
    st.info("Simulation de 20 sous-groupes (n=5) basée sur la performance du Round 2.")

    # Constants for n=5
    A2, D3, D4 = 0.577, 0, 2.114
    n_subgroups = 20
    
    # Data Generation
    x_bar_vals = []
    r_vals = []
    sigma = ct2 * 0.05 if ct2 > 0 else 1
    
    for _ in range(n_subgroups):
        samples = [random.gauss(ct2, sigma) for _ in range(5)]
        x_bar_vals.append(sum(samples) / 5)
        r_vals.append(max(samples) - min(samples))
        
    x_double_bar = sum(x_bar_vals) / n_subgroups
    r_bar = sum(r_vals) / n_subgroups
    
    # Limits
    ucl_x, lcl_x = x_double_bar + A2 * r_bar, x_double_bar - A2 * r_bar
    ucl_r, lcl_r = D4 * r_bar, D3 * r_bar

    cc1, cc2 = st.columns(2)
    
    with cc1:
        fig_x = go.Figure()
        fig_x.add_trace(go.Scatter(y=x_bar_vals, mode='lines+markers', line=dict(color='#0071e3', width=2)))
        fig_x.add_hline(y=ucl_x, line_dash="dash", line_color="#ff3b30", annotation_text="UCL")
        fig_x.add_hline(y=lcl_x, line_dash="dash", line_color="#ff3b30", annotation_text="LCL")
        fig_x.add_hline(y=x_double_bar, line_color="#34c759", annotation_text="X̄")
        st.plotly_chart(apple_chart_style(fig_x, "Carte des Moyennes (X̄)"), use_container_width=True)

    with cc2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(y=r_vals, mode='lines+markers', line=dict(color='#bf5af2', width=2)))
        fig_r.add_hline(y=ucl_r, line_dash="dash", line_color="#ff3b30", annotation_text="UCL")
        fig_r.add_hline(y=r_bar, line_color="#34c759", annotation_text="R̄")
        st.plotly_chart(apple_chart_style(fig_r, "Carte des Étendues (R)"), use_container_width=True)

    # Footer
    st.markdown("<br><p style='text-align: center; color: #86868b; font-size: 0.9rem;'>Lean Six Sigma Management System | Advanced Industrial Engineering Division</p>", unsafe_allow_html=True)
