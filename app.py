import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- 2. HELPER FUNCTIONS (Must be defined before use) ---
def style_control_chart(fig, title, y_label):
    """Applies consistent styling to the control charts."""
    fig.update_layout(
        title=title,
        yaxis_title=y_label,
        xaxis_title="Sous-groupes",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        height=400
    )
    return fig

def calculate_all_metrics(u, tt, d, tm):
    """Core calculation engine for all Lean and Industrial metrics."""
    if u <= 0 or tt <= 0:
        return {k: 0 for k in ["ct", "dr", "dt", "oee", "lt", "wip", "fpy", "tva", "prod"]}
    
    ct = tt / u
    tva = (tt - tm) / tt           # Taux de Valeur Ajoutée
    fpy = (u - d) / u              # First Pass Yield
    oee = tva * 1.0 * fpy          # OEE (Disponibilité * Performance * Qualité)
    lt = tt / u                    # Lead Time
    wip = (u * ct) / tt            # WIP
    prod = u / (tt / 60)           # Productivité (u/min)
    dr = (d / u) * 100             # Defect Rate
    dt_rate = (tm / tt) * 100      # Downtime Rate
    
    return {
        "ct": ct, "dr": dr, "dt": dt_rate,
        "oee": oee * 100, "lt": lt, "wip": wip,
        "fpy": fpy * 100, "tva": tva * 100, "prod": prod
    }

# --- 3. ADAPTIVE CSS ---
st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div {
        animation: tabFadeIn 0.6s cubic-bezier(0.25, 1, 0.5, 1);
    }
    @keyframes tabFadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.1); 
        backdrop-filter: blur(10px);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 18px;
        padding: 20px 25px !important;
    }
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

# --- 4. HEADER ---
col_t, col_l = st.columns([3, 1])
with col_t:
    st.title("Lean Six Sigma")
    st.write("Analyse de la performance : Station de Lavage / Logistique")
with col_l:
    st.markdown('<div style="display: flex; justify-content: flex-end;"><div class="lss-logo">Σ</div></div>', unsafe_allow_html=True)

# --- 5. TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Round 1", "🚀 Round 2", "🏆 Comparaison & Contrôle"])

with tab1:
    c1, c2 = st.columns(2)
    u1 = c1.number_input("Unités (R1)", value=20)
    tt1 = c2.number_input("Temps Total (s) (R1)", value=300)
    d1 = c1.number_input("Défauts (R1)", value=8)
    tm1 = c2.number_input("Temps Mort (s) (R1)", value=60)
    res1 = calculate_all_metrics(u1, tt1, d1, tm1)

with tab2:
    c3, c4 = st.columns(2)
    u2 = c3.number_input("Unités (R2)", value=35)
    tt2 = c4.number_input("Temps Total (s) (R2)", value=300)
    d2 = c3.number_input("Défauts (R2)", value=2)
    tm2 = c4.number_input("Temps Mort (s) (R2)", value=30)
    res2 = calculate_all_metrics(u2, tt2, d2, tm2)

with tab3:
    st.subheader("Analyse de l'Amélioration")
    m1, m2, m3 = st.columns(3)
    m1.metric("Cycle Time", f"{res2['ct']:.1f}s", f"{res2['ct']-res1['ct']:.1f}s", delta_color="inverse")
    m2.metric("Defect Rate", f"{res2['dr']:.1f}%", f"{res2['dr']-res1['dr']:.1f}%", delta_color="inverse")
    m3.metric("Downtime", f"{res2['dt']:.1f}%", f"{res2['dt']-res1['dt']:.1f}%", delta_color="inverse")

    st.divider()
    st.subheader("Cartes de Contrôle X̄ & R (Stabilité)")
    
    # SPC Logic
    n_groups = 20
    x_vals = [random.gauss(res2['ct'], res2['ct']*0.04) for _ in range(n_groups)]
    r_vals = [abs(random.gauss(res2['ct']*0.08, res2['ct']*0.02)) for _ in range(n_groups)]
    
    avg_x, avg_r = np.mean(x_vals), np.mean(r_vals)
    UCLx, LCLx = avg_x + (0.577 * avg_r), avg_x - (0.577 * avg_r)
    UCLr, LCLr = 2.114 * avg_r, 0

    # Interpretation
    if all(LCLx < x < UCLx for x in x_vals):
        st.success("✅ INTERPRÉTATION : Processus sous contrôle statistique")
    else:
        st.error("⚠️ INTERPRÉTATION : Processus hors contrôle")

    cc1, cc2 = st.columns(2)
    with cc1:
        fig_x = go.Figure()
        fig_x.add_trace(go.Scatter(y=x_vals, mode='lines+markers', line_color='#0071e3'))
        fig_x.add_hline(y=avg_x, line_color="green")
        fig_x.add_hline(y=UCLx, line_color="red", line_dash="dash")
        fig_x.add_hline(y=LCLx, line_color="red", line_dash="dash")
        st.plotly_chart(style_control_chart(fig_x, "Carte des Moyennes (X̄)", "Secondes (moy)"), use_container_width=True)

    with cc2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(y=r_vals, mode='lines+markers', line_color='#bf5af2'))
        fig_r.add_hline(y=avg_r, line_color="green")
        fig_r.add_hline(y=UCLr, line_color="red", line_dash="dash")
        fig_r.add_hline(y=LCLr, line_color="red", line_dash="dash")
        st.plotly_chart(style_control_chart(fig_r, "Carte des Étendues (R)", "Variation (s)"), use_container_width=True)
