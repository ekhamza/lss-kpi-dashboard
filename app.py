import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- 2. ADAPTIVE CSS (Glassmorphism, Animations, and Typography) ---
st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div {
        animation: tabFadeIn 0.6s cubic-bezier(0.25, 1, 0.5, 1);
    }
    @keyframes tabFadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    h1 { font-family: -apple-system, sans-serif; font-weight: 700; font-size: 3rem !important; }
    h3 { font-weight: 600; margin-top: 1.5rem !important; }

    /* Glassmorphism KPI Cards */
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.1); 
        backdrop-filter: blur(10px);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 18px;
        padding: 20px 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    div[data-testid="stMetric"]:hover { transform: translateY(-5px); }
    
    .logo-container { display: flex; align-items: center; justify-content: flex-end; gap: 15px; }
    .lss-logo {
        width: 65px; height: 65px;
        background: linear-gradient(135deg, #0071e3 0%, #bf5af2 100%);
        border-radius: 16px;
        display: flex; justify-content: center; align-items: center;
        color: white; font-size: 32px; font-weight: bold;
        animation: logoPulse 2.5s infinite alternate ease-in-out;
    }
    @keyframes logoPulse { 0% { transform: scale(1); } 100% { transform: scale(1.05); } }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
col_title, col_logo = st.columns([3, 1])
with col_title:
    st.title("Lean Six Sigma")
    st.markdown("<p style='color: #86868b; font-size: 1.2rem; margin-top: -5px;'>Industrial Intelligence & SPC Dashboard</p>", unsafe_allow_html=True)
with col_logo:
    st.markdown('<div class="logo-container"><div class="logo-text" style="text-align:right; font-family:-apple-system;">LEAN<br>SIX SIGMA</div><div class="lss-logo">Σ</div></div>', unsafe_allow_html=True)

st.divider()

# --- 4. CALCULATION ENGINE ---
def calculate_all_metrics(u, tt, d, tm):
    if u <= 0 or tt <= 0:
        return {k: 0 for k in ["ct", "dr", "dt", "oee", "lt", "wip", "fpy", "tva", "prod"]}
    
    ct = tt / u
    tva = (tt - tm) / tt           # Taux de Valeur Ajoutée
    fpy = (u - d) / u              # First Pass Yield
    oee = tva * 1.0 * fpy          # OEE
    lt = tt / u                    # Lead Time
    wip = (u * ct) / tt            # WIP
    prod = u / (tt / 60)           # Productivité
    dr = (d / u) * 100             # Defect Rate
    dt_rate = (tm / tt) * 100      # Downtime Rate
    
    return {
        "ct": ct, "dr": dr, "dt": dt_rate,
        "oee": oee * 100, "lt": lt, "wip": wip,
        "fpy": fpy * 100, "tva": tva * 100, "prod": prod
    }

# --- 5. TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Round 1", "🚀 Round 2", "🏆 Analyse & Contrôle"])

# ROUND 1
with tab1:
    st.subheader("Situation Initiale")
    c1, c2 = st.columns(2)
    with c1:
        u1 = st.number_input("Unités (R1)", value=20, key="u1")
        tt1 = st.number_input("Temps Total (s) (R1)", value=300, key="tt1")
    with c2:
        d1 = st.number_input("Défauts (R1)", value=8, key="d1")
        tm1 = st.number_input("Temps Mort (s) (R1)", value=60, key="tm1")
    
    res1 = calculate_all_metrics(u1, tt1, d1, tm1)
    
    st.markdown("### Performance Mesurée")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Cycle Time", f"{res1['ct']:.1f}s")
    m2.metric("OEE", f"{res1['oee']:.1f}%")
    m3.metric("WIP", f"{res1['wip']:.2f}")
    m4.metric("Prod", f"{res1['prod']:.1f} u/min")

# ROUND 2
with tab2:
    st.subheader("Processus Optimisé")
    c3, c4 = st.columns(2)
    with c3:
        u2 = st.number_input("Unités (R2)", value=35, key="u2")
        tt2 = st.number_input("Temps Total (s) (R2)", value=300, key="tt2")
    with c4:
        d2 = st.number_input("Défauts (R2)", value=2, key="d2")
        tm2 = st.number_input("Temps Mort (s) (R2)", value=30, key="tm2")
        
    res2 = calculate_all_metrics(u2, tt2, d2, tm2)
    
    st.markdown("### Performance Mesurée")
    m5, m6, m7, m8 = st.columns(4)
    m5.metric("Cycle Time", f"{res2['ct']:.1f}s")
    m6.metric("OEE", f"{res2['oee']:.1f}%")
    m7.metric("WIP", f"{res2['wip']:.2f}")
    m8.metric("Prod", f"{res2['prod']:.1f} u/min")

# TAB 3: ANALYSIS & SPC
with tab3:
    st.subheader("Analyse de Performance Globale")
    
    # Visual Comparison Row
    gv1, gv2, gv3, gv4 = st.columns(4)
    def bar_fig(label, r1_val, r2_val, color):
        fig = px.bar(x=["R1", "R2"], y=[r1_val, r2_val], color=["R1", "R2"], 
                     color_discrete_map={"R1":"#86868b","R2":color}, height=300)
        fig.update_layout(title=label, showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
        return fig

    gv1.plotly_chart(bar_fig("OEE (%)", res1['oee'], res2['oee'], "#0071e3"), use_container_width=True)
    gv2.plotly_chart(bar_fig("Lead Time (s)", res1['lt'], res2['lt'], "#5e5ce6"), use_container_width=True)
    gv3.plotly_chart(bar_fig("WIP", res1['wip'], res2['wip'], "#bf5af2"), use_container_width=True)
    gv4.plotly_chart(bar_fig("Productivité", res1['prod'], res2['prod'], "#32d74b"), use_container_width=True)

    st.divider()

    # --- SPC SECTION: X-BAR & R CHARTS ---
    st.subheader("Cartes de Contrôle Statistiques (Stabilité R2)")
    
    n_groups = 20
    # Simulate data based on Round 2 CT
    x_values = [random.gauss(res2['ct'], res2['ct']*0.04) for _ in range(n_groups)]
    r_values = [abs(random.gauss(res2['ct']*0.08, res2['ct']*0.02)) for _ in range(n_groups)]
    
    avg_x = np.mean(x_values)
    avg_r = np.mean(r_values)
    
    # Constants for n=5: A2=0.577, D3=0, D4=2.114
    UCLx, LCLx = avg_x + (0.577 * avg_r), avg_x - (0.577 * avg_r)
    UCLr, LCLr = 2.114 * avg_r, 0
    
    # INTERPRETATION LOGIC
    if all(LCLx < x < UCLx for x in x_values):
        st.success("✅ **INTERPRÉTATION :** Processus sous contrôle statistique")
    else:
        st.error("⚠️ **INTERPRÉTATION :** Processus hors contrôle")

    cc1, cc2 = st.columns(2)
    with cc1:
        fig_x = go.Figure()
        fig_x.add_trace(go.Scatter(y=x_values, mode='lines+markers', name='X-bar', line_color='#0071e3'))
        fig_x.add_hline(y=avg_x, line_color="green", annotation_text="X̄")
        fig_x.add_hline(y=UCLx, line_color="red", line_dash="dash", annotation_text="UCL")
        fig_x.add_hline(y=LCLx, line_color="red", line_dash="dash", annotation_text="LCL")
        fig_x.update_layout(title="Carte X-bar (Moyenne)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_x, use_container_width=True)
        
    with cc2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(y=r_values, mode='lines+markers', name='Range', line_color='#bf5af2'))
        fig_r.add_hline(y=avg_r, line_color="green", annotation_text="R̄")
        fig_r.add_hline(y=UCLr, line_color="red", line_dash="dash", annotation_text="UCL")
        fig_r.add_hline(y=LCLr, line_color="red", line_dash="dash", annotation_text="LCL")
        fig_r.update_layout(title="Carte R (Étendue)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_r, use_container_width=True)

    # Detailed Table Summary
    st.markdown("### Synthèse des Métriques")
    metrics = ["OEE (%)", "Lead Time (s)", "WIP", "Taux VA (%)", "FPY (%)", "Productivité"]
    r1_dat = [res1['oee'], res1['lt'], res1['wip'], res1['tva'], res1['fpy'], res1['prod']]
    r2_dat = [res2['oee'], res2['lt'], res2['wip'], res2['tva'], res2['fpy'], res2['prod']]
    
    df = pd.DataFrame({
        "Métrique": metrics,
        "Avant (R1)": [f"{v:.2f}" for v in r1_dat],
        "Après (R2)": [f"{v:.2f}" for v in r2_dat],
        "Impact": [f"{((r2_dat[i]-r1_dat[i])/r1_dat[i]*100):+.1f}%" if r1_dat[i] != 0 else "0%" for i in range(len(metrics))]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)
