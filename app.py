import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import numpy as np

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- 2. FONCTIONS UTILES (Définies au début pour éviter les erreurs) ---

def style_control_chart(fig, title, y_label):
    """Applique un style professionnel aux cartes de contrôle."""
    fig.update_layout(
        title=title,
        yaxis_title=y_label,
        xaxis_title="Sous-groupes",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        font=dict(family="-apple-system, sans-serif")
    )
    return fig

def calculate_all_metrics(u, tt, d, tm):
    """Calcule l'ensemble des indicateurs Lean et Industriels."""
    if u <= 0 or tt <= 0:
        return {k: 0 for k in ["ct", "dr", "dt", "oee", "lt", "wip", "fpy", "tva", "prod"]}
    
    ct = tt / u
    tva = (tt - tm) / tt           # Taux de Valeur Ajoutée
    fpy = (u - d) / u              # First Pass Yield (Qualité)
    oee = tva * 1.0 * fpy          # OEE (Dispo * Perf * Qualité)
    lt = tt / u                    # Lead Time
    wip = (u * ct) / tt            # Work In Progress
    prod = u / (tt / 60)           # Productivité (u/min)
    
    return {
        "ct": ct, "dr": (d/u)*100, "dt": (tm/tt)*100,
        "oee": oee * 100, "lt": lt, "wip": wip,
        "fpy": fpy * 100, "tva": tva * 100, "prod": prod
    }

# --- 3. STYLE CSS ADAPTATIF ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.05); 
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 15px;
        padding: 15px !important;
    }
    .lss-logo {
        width: 60px; height: 60px;
        background: linear-gradient(135deg, #0071e3 0%, #bf5af2 100%);
        border-radius: 12px;
        display: flex; justify-content: center; align-items: center;
        color: white; font-size: 28px; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. EN-TÊTE ---
col_t, col_l = st.columns([3, 1])
with col_t:
    st.title("Lean Six Sigma")
    st.write("Optimisation Industrielle & Maîtrise Statistique des Procédés (MSP/SPC)")
with col_l:
    st.markdown('<div style="display: flex; justify-content: flex-end;"><div class="lss-logo">Σ</div></div>', unsafe_allow_html=True)

# --- 5. ONGLETS ---
tab1, tab2, tab3 = st.tabs(["📊 Round 1 (Initial)", "🚀 Round 2 (Optimisé)", "🏆 Analyse SPC & Stabilité"])

with tab1:
    c1, c2 = st.columns(2)
    u1 = c1.number_input("Unités produites (R1)", value=20)
    tt1 = c2.number_input("Temps total (sec) (R1)", value=300)
    d1 = c1.number_input("Défauts (R1)", value=8)
    tm1 = c2.number_input("Temps mort (sec) (R1)", value=60)
    res1 = calculate_all_metrics(u1, tt1, d1, tm1)

with tab2:
    c3, c4 = st.columns(2)
    u2 = c3.number_input("Unités produites (R2)", value=35)
    tt2 = c4.number_input("Temps total (sec) (R2)", value=300)
    d2 = c3.number_input("Défauts (R2)", value=2)
    tm2 = c4.number_input("Temps mort (sec) (R2)", value=30)
    res2 = calculate_all_metrics(u2, tt2, d2, tm2)

with tab3:
    st.subheader("Analyse Approfondie : Cartes X̄ & R")
    
    # GÉNÉRATION DES DONNÉES SPC (Simulation Round 2)
    n_groups = 20
    x_vals = [random.gauss(res2['ct'], res2['ct']*0.05) for _ in range(n_groups)]
    # Simulation forcée de points hors limites pour l'interprétation
    x_vals[4] = res2['ct'] * 1.3  # Point haut
    x_vals[15] = res2['ct'] * 0.7 # Point bas
    
    r_vals = [abs(random.gauss(res2['ct']*0.1, res2['ct']*0.03)) for _ in range(n_groups)]
    
    avg_x, avg_r = np.mean(x_vals), np.mean(r_vals)
    UCLx, LCLx = avg_x + (0.577 * avg_r), avg_x - (0.577 * avg_r)
    UCLr, LCLr = 2.114 * avg_r, 0

    # CALCUL DES POINTS HORS LIMITES
    high_x = [i+1 for i, v in enumerate(x_vals) if v > UCLx]
    low_x = [i+1 for i, v in enumerate(x_vals) if v < LCLx]
    out_r = [i+1 for i, v in enumerate(r_vals) if v > UCLr]

    # SECTION INTERPRÉTATION (Conforme au Cahier des Charges)
    if not high_x and not low_x:
        st.success("✅ **INTERPRÉTATION : Processus sous contrôle statistique**")
    else:
        st.error("⚠️ **INTERPRÉTATION : Processus hors contrôle**")
        
        col_exp, col_ing = st.columns(2)
        with col_exp:
            st.markdown(f"""
            **A. Explication du résultat :**
            - **Points hors limites :** {len(high_x) + len(low_x)} point(s) détecté(s).
            - **Détails :** {len(high_x)} au-dessus de l'UCL, {len(low_x)} en-dessous de l'LCL.
            - **Localisation :** Groupes {', '.join(map(str, high_x + low_x))}.
            """)
        with col_ing:
            st.markdown(f"""
            **B. Interprétation Ingénieur :**
            - **Instabilité :** Variabilité élevée détectée.
            - **Causes :** Présence probable de **causes spéciales** (matériel, main d'œuvre).
            - **Statut :** Processus non maîtrisé nécessitant des actions correctives.
            """)

    # GRAPHIQUES
    cc1, cc2 = st.columns(2)
    with cc1:
        fig_x = go.Figure()
        fig_x.add_trace(go.Scatter(y=x_vals, mode='lines+markers', name='X̄', line_color='#0071e3'))
        fig_x.add_hline(y=avg_x, line_color="green", annotation_text="Moyenne")
        fig_x.add_hline(y=UCLx, line_color="red", line_dash="dash", label="UCL")
        fig_x.add_hline(y=LCLx, line_color="red", line_dash="dash", label="LCL")
        st.plotly_chart(style_control_chart(fig_x, "Carte X̄ (Stabilité de la Moyenne)", "Secondes"), use_container_width=True)

    with cc2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(y=r_vals, mode='lines+markers', name='R', line_color='#bf5af2'))
        fig_r.add_hline(y=avg_r, line_color="green", annotation_text="R̄")
        fig_r.add_hline(y=UCLr, line_color="red", line_dash="dash", label="UCL")
        st.plotly_chart(style_control_chart(fig_r, "Carte R (Maîtrise de la Variabilité)", "Dispersion"), use_container_width=True)

    # ANALYSE CARTE R & CONCLUSION
    st.divider()
    c_bot1, c_bot2 = st.columns(2)
    with c_bot1:
        st.markdown(f"""
        **C. Analyse de la Carte R :**
        {'✅ Variabilité stable (aucun point hors UCL).' if not out_r else '❌ Variabilité instable sur certains groupes.'}
        La dispersion intra-groupe est un indicateur clé de la répétabilité du processus.
        """)
        st.markdown("""
        **D. Lien Lean Six Sigma & DMAIC :**
        Dans la phase **Control**, nous cherchons à pérenniser les gains du Round 2. 
        L'objectif est d'éliminer les causes spéciales pour atteindre la stabilité.
        """)
    with c_bot2:
        st.markdown(f"""
        **E. Comparaison & Conclusion :**
        - **Évolution :** L'OEE est passé de {res1['oee']:.1f}% à {res2['oee']:.1f}%.
        - **Bilan :** Gain de performance majeur, mais la stabilité statistique doit encore être sécurisée.
        - **Action :** Identifier l'origine des écarts sur les groupes {', '.join(map(str, high_x + low_x))}.
        """)

    # TABLEAU RÉCAPITULATIF FINAL
    st.markdown("### Synthèse des Gains (Avant vs Après)")
    metrics = ["OEE (%)", "Lead Time (s)", "WIP", "Productivité"]
    df = pd.DataFrame({
        "Métrique": metrics,
        "R1 (Initial)": [res1['oee'], res1['lt'], res1['wip'], res1['prod']],
        "R2 (Optimisé)": [res2['oee'], res2['lt'], res2['wip'], res2['prod']]
    })
    st.table(df)
