import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import numpy as np

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- 2. STYLE CSS ADAPTATIF ---
st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div { animation: tabFadeIn 0.6s cubic-bezier(0.25, 1, 0.5, 1); }
    @keyframes tabFadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    h1 { font-family: -apple-system, sans-serif; font-weight: 700; font-size: 3rem !important; margin-bottom: 0px !important; }
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.1); backdrop-filter: blur(10px);
        border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 18px;
        padding: 20px 25px !important; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
    }
    .logo-container { display: flex; align-items: center; justify-content: flex-end; gap: 15px; }
    .lss-logo {
        width: 65px; height: 65px; background: linear-gradient(135deg, #0071e3 0%, #bf5af2 100%);
        border-radius: 16px; display: flex; justify-content: center; align-items: center;
        color: white; font-size: 32px; font-weight: bold; animation: logoPulse 2.5s infinite alternate ease-in-out;
    }
    @keyframes logoPulse { 0% { transform: scale(1); } 100% { transform: scale(1.05); } }
    </style>
""", unsafe_allow_html=True)

# --- 3. EN-TÊTE & INTRODUCTION (Style Camarade) ---
col_title, col_logo = st.columns([3, 1])
with col_title:
    st.title("Simulation Lean Six Sigma")
    st.markdown("<p style='color: #86868b; font-size: 1.2rem; margin-top: -5px;'>Approche DMAIC : Maîtrise Statistique des Procédés.</p>", unsafe_allow_html=True)
with col_logo:
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text" style="font-family: -apple-system; text-align: right;">LEAN<br><b>SIX SIGMA</b></div>
            <div class="lss-logo">Σ</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("Cette application simule l'impact du Lean Six Sigma sur une ligne de production en comparant deux états.")

st.subheader("🎯 Objectifs")
obj_col1, obj_col2, obj_col3 = st.columns(3)
obj_col1.success("⏱ Réduire le temps")
obj_col2.error("❌ Réduire les défauts")
obj_col3.info("📈 Améliorer la productivité")

# --- 4. MOTEUR DE CALCUL ---
def calculate_metrics(production, time, defects, downtime):
    ct = time / production if production > 0 else 0
    fpy = (production - defects) / production if production > 0 else 0
    va = (time - downtime) / time if time > 0 else 0
    oee = va * 1.0 * fpy
    return {"ct": ct, "oee": oee * 100, "prod": production / (time / 60) if time > 0 else 0}

# --- 5. ONGLETS ---
tab1, tab2, tab3 = st.tabs(["📊 Round 1", "🚀 Round 2", "🏆 Analyse SPC Complète"])

with tab1:
    st.subheader("Collecte R1")
    c1, c2 = st.columns(2)
    p1 = c1.number_input("Unités (R1)", value=20)
    t1 = c2.number_input("Temps (s) (R1)", value=300)
    d1 = c1.number_input("Défauts (R1)", value=8)
    dt1 = c2.number_input("Temps mort (s) (R1)", value=60)
    res1 = calculate_metrics(p1, t1, d1, dt1)

with tab2:
    st.subheader("Collecte R2")
    c3, c4 = st.columns(2)
    p2 = c3.number_input("Unités (R2)", value=35)
    t2 = c4.number_input("Temps (s) (R2)", value=300)
    d2 = c3.number_input("Défauts (R2)", value=2)
    dt2 = c4.number_input("Temps mort (s) (R2)", value=30)
    res2 = calculate_metrics(p2, t2, d2, dt2)

# --- 6. TAB 3 : AMÉLIORATION CARTE X-BAR & R ---
with tab3:
    st.subheader("Cartes de Contrôle (MSP / SPC)")
    
    # Simulation des données
    n = 20
    x_vals = [random.gauss(res2['ct'], res2['ct']*0.03) for _ in range(n)]
    r_vals = [abs(random.gauss(res2['ct']*0.08, res2['ct']*0.02)) for _ in range(n)]
    
    # Calcul des limites
    avg_x, avg_r = np.mean(x_vals), np.mean(r_vals)
    UCLx, LCLx = avg_x + (0.577 * avg_r), avg_x - (0.577 * avg_r)
    UCLr, LCLr = 2.114 * avg_r, 0

    # Forçage des points hors limites (Cahier des charges)
    x_vals[5] = UCLx + 0.4
    x_vals[12] = UCLx + 0.2
    x_vals[18] = LCLx - 0.3

    # Graphique X-Bar
    fig_x = go.Figure()
    fig_x.add_trace(go.Scatter(y=x_vals, mode='lines+markers', name='Moyenne (X̄)', line_color='#0071e3'))
    fig_x.add_hline(y=avg_x, line_color="green", annotation_text=f"X̄: {avg_x:.2f}")
    fig_x.add_hline(y=UCLx, line_color="red", line_dash="dash", annotation_text=f"UCL: {UCLx:.2f}")
    fig_x.add_hline(y=LCLx, line_color="red", line_dash="dash", annotation_text=f"LCL: {LCLx:.2f}")
    
    # Graphique R
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatter(y=r_vals, mode='lines+markers', name='Étendue (R)', line_color='#bf5af2'))
    fig_r.add_hline(y=avg_r, line_color="green", annotation_text=f"R̄: {avg_r:.2f}")
    fig_r.add_hline(y=UCLr, line_color="red", line_dash="dash", annotation_text=f"UCL: {UCLr:.2f}")
    fig_r.add_hline(y=LCLr, line_color="red", line_dash="dash", annotation_text=f"LCL: {LCLr:.2f}")

    cc1, cc2 = st.columns(2)
    cc1.plotly_chart(fig_x.update_layout(title="Carte X̄ (Stabilité de la moyenne)"), use_container_width=True)
    cc2.plotly_chart(fig_r.update_layout(title="Carte R (Maîtrise de la dispersion)"), use_container_width=True)

    # --- SECTION INTERPRÉTATION & BILAN ---
    st.error("⚠️ **INTERPRÉTATION : Processus hors contrôle**")
    
    col_A, col_B = st.columns(2)
    with col_A:
        st.markdown(f"""
        **A. Explication du résultat :**
        - **3 points hors limites** identifiés.
        - 2 points dépassent l'**UCL** (Groupes 6, 13).
        - 1 point est sous l'**LCL** (Groupe 19).
        - Le processus est statistiquement **instable**.
        """)
    with col_B:
        st.markdown("""
        **B. Interprétation Ingénieur :**
        - Instabilité due à une variabilité imprévue.
        - Présence de **causes spéciales** (matériel, main d'œuvre).
        - Actions requises : Standardisation et Poka-Yoke.
        """)

    st.divider()
    
    st.info("#### ✔ Lien DMAIC & Conclusion")
    st.markdown(f"""
    Le passage du Round 1 au Round 2 a permis d'augmenter l'OEE (**{res1['oee']:.1f}% → {res2['oee']:.1f}%**). 
    Cependant, la carte SPC montre que la stabilité n'est pas encore parfaite. 
    **Conclusion :** Le processus est amélioré mais doit être mieux maîtrisé.
    """)
