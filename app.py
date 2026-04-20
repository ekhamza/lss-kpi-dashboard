import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- 2. ADAPTIVE CSS ---
st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div { animation: tabFadeIn 0.6s cubic-bezier(0.25, 1, 0.5, 1); }
    @keyframes tabFadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    h1 { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; font-size: 3rem !important; margin-bottom: 0px !important; }
    h3 { font-weight: 600; margin-top: 1.5rem !important; }
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.1); backdrop-filter: blur(10px);
        border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 18px;
        padding: 20px 25px !important; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1); transition: all 0.4s ease-in-out;
    }
    div[data-testid="stMetric"]:hover { transform: translateY(-5px); background: rgba(128, 128, 128, 0.15); }
    .logo-container { display: flex; align-items: center; justify-content: flex-end; gap: 15px; }
    .lss-logo {
        width: 65px; height: 65px; background: linear-gradient(135deg, #0071e3 0%, #bf5af2 100%);
        border-radius: 16px; display: flex; justify-content: center; align-items: center;
        color: white; font-size: 32px; font-weight: bold; animation: logoPulse 2.5s infinite alternate ease-in-out;
    }
    @keyframes logoPulse { 0% { transform: scale(1); } 100% { transform: scale(1.05); } }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER SECTION (Avec ajouts du camarade) ---
col_title, col_logo = st.columns([3, 1])
with col_title:
    st.title("Simulation Lean Six Sigma")
    st.markdown("<p style='color: #86868b; font-size: 1.2rem; margin-top: -5px;'>Approche DMAIC : Optimisation de la Performance Industrielle.</p>", unsafe_allow_html=True)
with col_logo:
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text" style="font-family: -apple-system; font-weight: 600; text-align: right;">LEAN<br>SIX SIGMA</div>
            <div class="lss-logo">Σ</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
Cette application simule une ligne de production avec et sans Lean Six Sigma  
afin d’analyser l’impact sur la performance industrielle.
""")

st.subheader("🎯 Objectifs")
obj_col1, obj_col2, obj_col3 = st.columns(3)
obj_col1.success("⏱ Réduire le temps")
obj_col2.error("❌ Réduire les défauts")
obj_col3.info("📈 Améliorer la productivité")

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. CALCULATION ENGINE ---
def calculate_all_metrics(production, total_time, defects, downtime):
    cycle_time = total_time / production if production > 0 else 0
    defect_rate = (defects / production) * 100 if production > 0 else 0
    downtime_rate = (downtime / total_time) * 100 if total_time > 0 else 0
    
    lead_time_kpi = total_time / production if production > 0 else 0
    fpy = (production - defects) / production if production > 0 else 0
    va_rate = (total_time - downtime) / total_time if total_time > 0 else 0
    wip = (production * cycle_time) / total_time if total_time > 0 else 0
    productivity = production / (total_time / 60) if total_time > 0 else 0
    oee = va_rate * 1.0 * fpy 
    
    return {
        "ct": cycle_time, "dr": defect_rate, "dt": downtime_rate,
        "lt": lead_time_kpi, "fpy": fpy * 100, "va": va_rate * 100,
        "wip": wip, "prod": productivity, "oee": oee * 100
    }

# --- 5. TABS SETUP ---
tab1, tab2, tab3 = st.tabs(["📊 Round 1 (Initial)", "🚀 Round 2 (Optimisé)", "🏆 Analyse SPC & Stabilité"])

# ==========================================
# TAB 1: ROUND 1
# ==========================================
with tab1:
    st.subheader("Initial Data Collection")
    col1, col2 = st.columns(2)
    with col1:
        prod1 = st.number_input("Production (Units) - R1", value=20, min_value=0, step=1)
        time1 = st.number_input("Total Time (sec) - R1", value=300, min_value=0, step=10)
    with col2:
        defects1 = st.number_input("Defects - R1", value=8, min_value=0, step=1)
        downtime1 = st.number_input("Temps mort (sec) - R1", value=60, min_value=0, step=5)

    res1 = calculate_all_metrics(prod1, time1, defects1, downtime1)
    
    k1, k2, k3 = st.columns(3)
    k1.metric("⏱️ Cycle Time", f"{res1['ct']:.1f}s")
    k2.metric("⚠️ Defect Rate", f"{res1['dr']:.1f}%")
    k3.metric("OEE", f"{res1['oee']:.1f}%")

# ==========================================
# TAB 2: ROUND 2
# ==========================================
with tab2:
    st.subheader("Post-Optimization Data")
    col3, col4 = st.columns(2)
    with col3:
        prod2 = st.number_input("Production (Units) - R2", value=35, min_value=0, step=1)
        time2 = st.number_input("Total Time (sec) - R2", value=300, min_value=0, step=10)
    with col4:
        defects2 = st.number_input("Defects - R2", value=2, min_value=0, step=1)
        downtime2 = st.number_input("Temps mort (sec) - R2", value=30, min_value=0, step=5)

    res2 = calculate_all_metrics(prod2, time2, defects2, downtime2)
    
    k4, k5, k6 = st.columns(3)
    k4.metric("⏱️ Cycle Time", f"{res2['ct']:.1f}s")
    k5.metric("⚠️ Defect Rate", f"{res2['dr']:.1f}%")
    k6.metric("OEE", f"{res2['oee']:.1f}%")

# ==========================================
# TAB 3: SPC & CAHIER DES CHARGES
# ==========================================
with tab3:
    st.subheader("Cartes de Contrôle X̄ & R (Stabilité R2)")
    
    # 1. SIMULATION DES DONNÉES SPC
    n_groups = 20
    
    # Simulation R1 (Forte Variabilité)
    r1_x_vals = [random.gauss(res1['ct'], res1['ct']*0.15) for _ in range(n_groups)]
    r1_avg_r = np.mean([abs(random.gauss(res1['ct']*0.2, res1['ct']*0.05)) for _ in range(n_groups)])

    # Simulation R2 (Faible variabilité, mais on force les points hors limites demandés par le prof)
    x_vals = [random.gauss(res2['ct'], res2['ct']*0.02) for _ in range(n_groups)]
    r_vals = [abs(random.gauss(res2['ct']*0.06, res2['ct']*0.01)) for _ in range(n_groups)]
    
    avg_x, avg_r = np.mean(x_vals), np.mean(r_vals)
    UCLx, LCLx = avg_x + (0.577 * avg_r), avg_x - (0.577 * avg_r)
    UCLr, LCLr = 2.114 * avg_r, 0
    
    # FORÇAGE DE L'EXEMPLE DU CAHIER DES CHARGES
    x_vals[4] = UCLx + 0.5  # 1er point au-dessus UCL (Groupe 5)
    x_vals[11] = UCLx + 0.3 # 2ème point au-dessus UCL (Groupe 12)
    x_vals[16] = LCLx - 0.4 # 1 point sous LCL (Groupe 17)
    
    r_vals[8] = UCLr + 0.2  # On force un point instable sur la carte R pour illustrer le point C

    # 2. IDENTIFICATION DES POINTS HORS LIMITES
    high_x = [i+1 for i, v in enumerate(x_vals) if v > UCLx]
    low_x = [i+1 for i, v in enumerate(x_vals) if v < LCLx]
    out_r = [i+1 for i, v in enumerate(r_vals) if v > UCLr]

    # --- AFFICHAGE DES GRAPHIQUES ---
    def style_fig(fig, title):
        fig.update_layout(title=title, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=True, margin=dict(l=20, r=20, t=40, b=20))
        return fig

    cc1, cc2 = st.columns(2)
    with cc1:
        fig_x = go.Figure(go.Scatter(y=x_vals, mode='lines+markers', name='X̄ (Cycle Time)', line_color='#0071e3'))
        fig_x.add_hline(y=avg_x, line_color="green", annotation_text="Moyenne")
        fig_x.add_hline(y=UCLx, line_color="red", line_dash="dash", annotation_text="UCL")
        fig_x.add_hline(y=LCLx, line_color="red", line_dash="dash", annotation_text="LCL")
        st.plotly_chart(style_fig(fig_x, "Carte X̄ (Moyennes)"), use_container_width=True)
    with cc2:
        fig_r = go.Figure(go.Scatter(y=r_vals, mode='lines+markers', name='R (Étendue)', line_color='#bf5af2'))
        fig_r.add_hline(y=avg_r, line_color="green", annotation_text="R̄")
        fig_r.add_hline(y=UCLr, line_color="red", line_dash="dash", annotation_text="UCL")
        st.plotly_chart(style_fig(fig_r, "Carte R (Étendues)"), use_container_width=True)

    st.divider()

    # =========================================================
    # BLOC D'INTERPRÉTATION (RÉPONDANT AU CAHIER DES CHARGES)
    # =========================================================
    st.error(f"❌ **INTERPRÉTATION : Processus hors contrôle**")
    
    col_A, col_B = st.columns(2)
    
    # POINT A & B
    with col_A:
        st.markdown("#### ✔ A. Explication du résultat")
        st.markdown(f"""
        - **Nombre de points hors limites :** {len(high_x) + len(low_x)}
        - **Où se trouvent ces points :** - **{len(high_x)} point(s) dépassent UCL** (Groupes {', '.join(map(str, high_x))})
          - **{len(low_x)} point(s) est/sont sous LCL** (Groupe {', '.join(map(str, low_x))})
        - **Bilan :** Donc processus instable.
        """)

    with col_B:
        st.markdown("#### ✔ B. Interprétation Ingénieur")
        st.markdown("""
        - Instabilité due à une **variabilité élevée** ponctuelle.
        - Présence de **causes spéciales** (ex: panne machine, erreur opérateur, matière défectueuse).
        - Le processus n'est actuellement **pas maîtrisé** d'un point de vue statistique.
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    col_C, col_D = st.columns(2)

    # POINT C & D
    with col_C:
        st.markdown("#### ✔ C. Analyse de la carte R")
        if out_r:
            st.markdown(f"""
            - **Variabilité :** Instable.
            - **Détail :** {len(out_r)} point(s) (Groupe {', '.join(map(str, out_r))}) dépasse(nt) l'UCL de la carte R.
            - **Problème :** L'étendue (dispersion) au sein d'un même sous-groupe est trop forte, ce qui empêche de garantir une qualité constante.
            """)
        else:
            st.markdown("- **Variabilité :** Stable en intra-groupe (aucun point au-dessus de l'UCL R).")

    with col_D:
        st.markdown("#### ✔ D. Lien avec Lean Six Sigma")
        st.markdown("""
        - **Avant amélioration (R1) :** Processus totalement instable avec beaucoup de défauts.
        - **Après amélioration (R2) :** Gain de performance prouvé, mais l'**objectif de la phase 'Control' du DMAIC** est d'atteindre et maintenir la *stabilité*.
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # POINT E & F
    st.info("#### ✔ E. Comparaison Avant / Après")
    c_e1, c_e2, c_e3 = st.columns(3)
    c_e1.metric("Variabilité R1 (Étendue Moy)", f"{r1_avg_r:.2f}s")
    c_e2.metric("Variabilité R2 (Étendue Moy)", f"{avg_r:.2f}s", delta=f"{(avg_r-r1_avg_r):.2f}s (Baisse)", delta_color="inverse")
    with c_e3:
        st.markdown("""
        **Conclusion Comparaison :**
        - Variabilité globale en forte baisse (↓).
        - Le processus est *plus* stable qu'avant, mais nécessite encore des ajustements.
        """)

    st.warning("#### ✔ F. Conclusion Claire")
    st.markdown("""
    1. **État actuel :** Processus non maîtrisé (Présence de causes spéciales).
    2. **Actions nécessaires :** Enquêter sur les groupes hors limites, identifier la cause racine et appliquer un Poka-Yoke ou standard de travail.
    3. **Objectif final :** Stabilité totale (zéro point hors limite) avant clôture du projet DMAIC.
    """)
