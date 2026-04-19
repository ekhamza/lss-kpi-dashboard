import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- 2. ADAPTIVE CSS (Original Glassmorphism & Animations) ---
st.markdown("""
    <style>
    /* Tab transition animation */
    div[data-testid="stVerticalBlock"] > div {
        animation: tabFadeIn 0.6s cubic-bezier(0.25, 1, 0.5, 1);
    }
    @keyframes tabFadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Apple-style typography */
    h1 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 700;
        font-size: 3rem !important;
        margin-bottom: 0px !important;
    }
    h3 { font-weight: 600; margin-top: 1.5rem !important; }

    /* Glassmorphism Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.1); 
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 18px;
        padding: 20px 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
    }

    /* Animated Sigma Logo */
    .logo-container { display: flex; align-items: center; justify-content: flex-end; gap: 15px; }
    .lss-logo {
        width: 65px; height: 65px;
        background: linear-gradient(135deg, #0071e3 0%, #bf5af2 100%);
        border-radius: 16px;
        display: flex; justify-content: center; align-items: center;
        color: white; font-size: 32px; font-weight: bold;
        animation: logoPulse 2.5s infinite alternate ease-in-out;
    }
    @keyframes logoPulse {
        0% { transform: scale(1); }
        100% { transform: scale(1.05); }
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER SECTION ---
col_title, col_logo = st.columns([3, 1])
with col_title:
    st.title("Lean Six Sigma")
    st.markdown("<p style='color: #86868b; font-size: 1.2rem; margin-top: -5px;'>Industrial Simulation Dashboard</p>", unsafe_allow_html=True)
with col_logo:
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text" style="font-family: -apple-system; font-weight: 600; text-align: right;">LEAN<br>SIX SIGMA</div>
            <div class="lss-logo">Σ</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- 4. CORE ENGINE (All Original + All New Formulas) ---
def calculate_metrics(unites, temps_total, defauts, temps_mort):
    if unites <= 0 or temps_total <= 0:
        return {k: 0 for k in ["ct", "dr", "dt", "oee", "lt", "wip", "fpy", "tva", "prod"]}
    
    # Existing variables
    cycle_time = temps_total / unites
    defect_rate = (defauts / unites) * 100
    downtime_rate = (temps_mort / temps_total) * 100
    
    # --- NEW ADDED INDICATORS (Your exact formulas) ---
    # OEE = Disponibilité × Performance × Qualité
    # (Disponibilité = TVA, Qualité = FPY, Performance = 100%)
    fpy = (unites - defauts) / unites
    tva = (temps_total - temps_mort) / temps_total
    oee = tva * 1.0 * fpy
    
    lead_time = temps_total / unites
    wip = (unites * cycle_time) / temps_total
    productivite = unites / (temps_total / 60)
    
    return {
        "ct": cycle_time, "dr": defect_rate, "dt": downtime_rate,
        "oee": oee * 100, "lt": lead_time, "wip": wip,
        "fpy": fpy * 100, "tva": tva * 100, "prod": productivite
    }

# --- 5. INTERFACE TABS ---
tab1, tab2, tab3 = st.tabs(["Round 1 (Initial)", "Round 2 (Optimisé)", "Analyse Comparative"])

# ==========================================
# ROUND 1
# ==========================================
with tab1:
    st.subheader("Data Collection - Round 1")
    c1, c2 = st.columns(2)
    with c1:
        u1 = st.number_input("Unités produites (R1)", value=20, key="u1")
        tt1 = st.number_input("Temps total (sec) (R1)", value=300, key="tt1")
    with c2:
        d1 = st.number_input("Défauts (R1)", value=8, key="d1")
        tm1 = st.number_input("Temps mort (sec) (R1)", value=60, key="tm1")
    
    r1 = calculate_metrics(u1, tt1, d1, tm1)
    
    st.markdown("### Performance Mesurée (Original)")
    k1, k2, k3 = st.columns(3)
    k1.metric("⏱️ Cycle Time", f"{r1['ct']:.1f}s")
    k2.metric("⚠️ Taux Défauts", f"{r1['dr']:.1f}%")
    k3.metric("🛑 Temps mort", f"{r1['dt']:.1f}%")

    st.markdown("### Indicateurs Industriels (Added)")
    n1, n2, n3, n4 = st.columns(4)
    n1.metric("OEE", f"{r1['oee']:.1f}%")
    n2.metric("First Pass Yield", f"{r1['fpy']:.1f}%")
    n3.metric("WIP", f"{r1['wip']:.2f}")
    n4.metric("Productivité", f"{r1['prod']:.1f} u/min")

# ==========================================
# ROUND 2
# ==========================================
with tab2:
    st.subheader("Data Collection - Round 2")
    c3, c4 = st.columns(2)
    with c3:
        u2 = st.number_input("Unités produites (R2)", value=35, key="u2")
        tt2 = st.number_input("Temps total (sec) (R2)", value=300, key="tt2")
    with c4:
        d2 = st.number_input("Défauts (R2)", value=2, key="d2")
        tm2 = st.number_input("Temps mort (sec) (R2)", value=30, key="tm2")
        
    r2 = calculate_metrics(u2, tt2, d2, tm2)
    
    st.markdown("### Performance Mesurée (Original)")
    k4, k5, k6 = st.columns(3)
    k4.metric("⏱️ Cycle Time", f"{r2['ct']:.1f}s")
    k5.metric("⚠️ Taux Défauts", f"{r2['dr']:.1f}%")
    k6.metric("🛑 Temps mort", f"{r2['dt']:.1f}%")

    st.markdown("### Indicateurs Industriels (Added)")
    n5, n6, n7, n8 = st.columns(4)
    n5.metric("OEE", f"{r2['oee']:.1f}%")
    n6.metric("First Pass Yield", f"{r2['fpy']:.1f}%")
    n7.metric("WIP", f"{r2['wip']:.2f}")
    n8.metric("Productivité", f"{r2['prod']:.1f} u/min")

# ==========================================
# ANALYSIS & CHARTS
# ==========================================
with tab3:
    st.subheader("Synthèse des Améliorations")
    
    # Delta Row
    comp1, comp2, comp3, comp4 = st.columns(4)
    comp1.metric("OEE", f"{r2['oee']:.1f}%", f"{r2['oee']-r1['oee']:.1f}%")
    comp2.metric("Lead Time", f"{r2['lt']:.1f}s", f"{r2['lt']-r1['lt']:.1f}s", delta_color="inverse")
    comp3.metric("Taux VA", f"{r2['tva']:.1f}%", f"{r2['tva']-r1['tva']:.1f}%")
    comp4.metric("Productivité", f"{r2['prod']:.1f}", f"{r2['prod']-r1['prod']:.1f}")

    st.divider()

    # Detailed Comparison Table
    metrics_list = ["Cycle Time", "Lead Time", "WIP", "FPY (Qualité)", "Taux VA", "OEE", "Productivité"]
    r1_values = [r1['ct'], r1['lt'], r1['wip'], r1['fpy'], r1['tva'], r1['oee'], r1['prod']]
    r2_values = [r2['ct'], r2['lt'], r2['wip'], r2['fpy'], r2['tva'], r2['oee'], r2['prod']]
    
    df_compare = pd.DataFrame({
        "Métrique": metrics_list,
        "Avant (R1)": [f"{v:.2f}" for v in r1_values],
        "Après (R2)": [f"{v:.2f}" for v in r2_values],
        "Impact (%)": [f"{((r2_values[i]-r1_values[i])/r1_values[i]*100):+.1f}%" if r1_values[i] != 0 else "0%" for i in range(len(metrics_list))]
    })
    st.dataframe(df_compare, use_container_width=True, hide_index=True)

    # Visual Charts
    st.markdown("### Visualisation de la Performance")
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        fig_oee = px.bar(x=["R1", "R2"], y=[r1['oee'], r2['oee']], title="Progression OEE (%)", color=["R1", "R2"], color_discrete_map={"R1":"#86868b","R2":"#0071e3"})
        st.plotly_chart(fig_oee, use_container_width=True)
    with v_col2:
        fig_lt = px.bar(x=["R1", "R2"], y=[r1['lt'], r2['lt']], title="Réduction Lead Time (sec)", color=["R1", "R2"], color_discrete_map={"R1":"#86868b","R2":"#bf5af2"})
        st.plotly_chart(fig_lt, use_container_width=True)

    # Statistical Control
    st.subheader("Carte de Contrôle (Stabilité R2)")
    n_points = 20
    sim_data = [random.gauss(r2['ct'], r2['ct']*0.05) for _ in range(n_points)]
    fig_cc = go.Figure(go.Scatter(y=sim_data, mode='lines+markers', line_color='#0071e3'))
    fig_cc.add_hline(y=sum(sim_data)/n_points, line_color="#34c759", annotation_text="Moyenne")
    st.plotly_chart(fig_cc, use_container_width=True)
