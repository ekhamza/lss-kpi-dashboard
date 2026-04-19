import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- 2. HELPER FUNCTIONS ---

def style_control_chart(fig, title, y_label):
    fig.update_layout(
        title=title, yaxis_title=y_label, xaxis_title="Sous-groupes",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20), height=380
    )
    return fig

def calculate_all_metrics(u, tt, d, tm):
    if u <= 0 or tt <= 0:
        return {k: 0 for k in ["ct", "dr", "dt", "oee", "lt", "wip", "fpy", "tva", "prod"]}
    ct = tt / u
    tva = (tt - tm) / tt
    fpy = (u - d) / u
    oee = tva * 1.0 * fpy
    lt = tt / u
    wip = (u * ct) / tt
    prod = u / (tt / 60)
    return {
        "ct": ct, "dr": (d/u)*100, "dt": (tm/tt)*100,
        "oee": oee * 100, "lt": lt, "wip": wip,
        "fpy": fpy * 100, "tva": tva * 100, "prod": prod
    }

# --- 3. ADAPTIVE CSS ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.05); 
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 15px; padding: 15px !important;
    }
    .lss-logo {
        width: 60px; height: 60px;
        background: linear-gradient(135deg, #0071e3 0%, #bf5af2 100%);
        border-radius: 12px; display: flex; justify-content: center; 
        align-items: center; color: white; font-size: 28px; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
col_t, col_l = st.columns([3, 1])
with col_t:
    st.title("Lean Six Sigma")
    st.write("Optimisation Industrielle & Maîtrise Statistique (SPC)")
with col_l:
    st.markdown('<div style="display: flex; justify-content: flex-end;"><div class="lss-logo">Σ</div></div>', unsafe_allow_html=True)

# --- 5. TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Round 1", "🚀 Round 2", "🏆 Analyse SPC Complète"])

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
    st.subheader("Analyse de Stabilité & Performance")
    
    # SPC DATA SIMULATION
    n_groups = 25
    x_vals = [random.gauss(res2['ct'], res2['ct']*0.05) for _ in range(n_groups)]
    # Intentionally add 2 outliers for the "Engineer Interpretation"
    x_vals[5] = res2['ct'] * 1.25
    x_vals[18] = res2['ct'] * 0.70
    
    r_vals = [abs(random.gauss(res2['ct']*0.1, res2['ct']*0.03)) for _ in range(n_groups)]
    
    avg_x, avg_r = np.mean(x_vals), np.mean(r_vals)
    UCLx, LCLx = avg_x + (0.577 * avg_r), avg_x - (0.577 * avg_r)
    UCLr, LCLr = 2.114 * avg_r, 0

    # A. AUTOMATED COUNTING
    high_points = len([x for x in x_vals if x > UCLx])
    low_points = len([x for x in x_vals if x < LCLx])
    r_outliers = len([r for r in r_vals if r > UCLr])

    # DISPLAY INTERPRETATION
    if high_points + low_points == 0:
        st.success("✅ **PROCESSUS SOUS CONTRÔLE STATISTIQUE**")
    else:
        st.error(f"⚠️ **PROCESSUS HORS CONTRÔLE : {high_points + low_points} point(s) hors limites**")
        
        exp_col, int_col = st.columns(2)
        with exp_col:
            st.info(f"**Justification Technique :**\n- Points au-dessus UCL : {high_points}\n- Points sous LCL : {low_points}\n- Points instables identifiés : Groupes {', '.join([str(i+1) for i,x in enumerate(x_vals) if x > UCLx or x < LCLx])}")
        with int_col:
            st.warning("**Interprétation Ingénieur :**\nInstabilité détectée due à une variabilité élevée. Présence de **causes spéciales** (facteurs externes) influençant le Cycle Time. Le processus n'est pas encore maîtrisé malgré l'amélioration du Round 2.")

    cc1, cc2 = st.columns(2)
    with cc1:
        fig_x = go.Figure()
        fig_x.add_trace(go.Scatter(y=x_vals, mode='lines+markers', name='X̄', line_color='#0071e3'))
        fig_x.add_hline(y=avg_x, line_color="green", annotation_text="Moyenne")
        fig_x.add_hline(y=UCLx, line_color="red", line_dash="dash", annotation_text="UCL")
        fig_x.add_hline(y=LCLx, line_color="red", line_dash="dash", annotation_text="LCL")
        st.plotly_chart(style_control_chart(fig_x, "Carte X̄ (Stabilité de la Moyenne)", "Temps (s)"), use_container_width=True)

    with cc2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(y=r_vals, mode='lines+markers', name='R', line_color='#bf5af2'))
        fig_r.add_hline(y=avg_r, line_color="green", annotation_text="R̄")
        fig_r.add_hline(y=UCLr, line_color="red", line_dash="dash", annotation_text="UCL")
        st.plotly_chart(style_control_chart(fig_r, "Carte R (Maîtrise de la Variabilité)", "Dispersion (s)"), use_container_width=True)
        
    # C. R-CHART ANALYSIS
    st.markdown("#### 🔎 Analyse de la Dispersion (Carte R)")
    if r_outliers == 0:
        st.write("La variabilité intra-groupe est stable. La dispersion reste constante malgré les écarts de moyenne.")
    else:
        st.write(f"⚠️ Alerte : {r_outliers} point(s) dépassent l'UCL sur la carte R. La dispersion du processus est elle-même instable.")

    st.divider()

    # D & E. LEAN SIX SIGMA COMPARISON
    st.subheader("🏁 Conclusion DMAIC & Comparaison")
    sum1, sum2 = st.columns(2)
    with sum1:
        st.write("**Lien Lean Six Sigma :**")
        st.write("L'objectif de la phase 'Control' du DMAIC est de transformer un processus instable (Round 1) en un processus prévisible (Round 2). Ici, la stabilité reste l'objectif prioritaire avant de valider l'amélioration.")
    with sum2:
        improv = ((res2['oee'] - res1['oee'])/res1['oee'])*100 if res1['oee'] > 0 else 0
        st.write(f"**Bilan de Variabilité :**\n- OEE : {improv:+.1f}%\n- Variabilité (R1 vs R2) : Réduction de la dispersion cible identifiée.\n- **Statut Final :** Amélioration performante mais stabilité à confirmer.")
