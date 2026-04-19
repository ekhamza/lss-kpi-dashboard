import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- 2. ADAPTIVE CSS (Original Apple-style + Glassmorphism) ---
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
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 700;
        color: var(--text-color) !important;
        font-size: 3rem !important;
        margin-bottom: 0px !important;
    }
    
    h3 {
        font-weight: 600;
        color: var(--text-color) !important; 
        margin-top: 1.5rem !important;
    }

    /* Adaptive Glassmorphism KPI Cards */
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.1); 
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 18px;
        padding: 20px 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.2);
        background: rgba(128, 128, 128, 0.15);
    }

    /* PURE CSS ANIMATED LOGO */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 15px;
    }
    .lss-logo {
        width: 65px; height: 65px;
        background: linear-gradient(135deg, #0071e3 0%, #bf5af2 100%);
        border-radius: 16px;
        display: flex; justify-content: center; align-items: center;
        color: white; font-size: 32px; font-weight: bold;
        box-shadow: 0 10px 20px rgba(0, 113, 227, 0.2);
        animation: logoPulse 2.5s infinite alternate ease-in-out;
    }
    @keyframes logoPulse {
        0% { transform: scale(1); box-shadow: 0 5px 15px rgba(0, 113, 227, 0.2); }
        100% { transform: scale(1.05); box-shadow: 0 15px 30px rgba(191, 90, 242, 0.4); }
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER & DMAIC INTRO ---
col_title, col_logo = st.columns([3, 1])
with col_title:
    st.title("Lean Six Sigma")
    st.markdown("<p style='color: #86868b; font-size: 1.2rem; margin-top: -5px;'>Simulation de Ligne de Production – Approche DMAIC</p>", unsafe_allow_html=True)
with col_logo:
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text" style="font-family: -apple-system, sans-serif; font-weight: 600; text-align: right;">LEAN<br>SIX SIGMA</div>
            <div class="lss-logo">Σ</div>
        </div>
    """, unsafe_allow_html=True)

# Objectives Section (From Classmate Code)
col_obj1, col_obj2, col_obj3 = st.columns(3)
col_obj1.success("⏱ **Réduire le temps**")
col_obj2.error("❌ **Réduire les défauts**")
col_obj3.info("📈 **Améliorer la productivité**")

st.divider()

# --- 4. CALCULATION LOGIC (New Industrial Formulas) ---
def calculate_all_kpis(units, total_time, defects, downtime):
    if units <= 0 or total_time <= 0:
        return [0] * 7
    
    # User's Precise Formulas
    cycle_time = total_time / units
    lead_time = total_time / units 
    wip = (units * cycle_time) / total_time
    fpy = (units - defects) / units
    va_rate = (total_time - downtime) / total_time
    productivity = units / (total_time / 60)
    
    # OEE = Disponibilité (VA Rate) * Performance (1.0) * Qualité (FPY)
    oee = va_rate * 1.0 * fpy
    
    return oee, lead_time, wip, fpy, va_rate, productivity, cycle_time

# --- 5. TABS INTERFACE ---
tab1, tab2, tab3 = st.tabs(["Round 1 (Initial)", "Round 2 (Optimisé)", "Analyse Comparative"])

# ==========================================
# ROUND 1 DATA
# ==========================================
with tab1:
    st.subheader("Collecte des Données Initiales")
    c1, c2 = st.columns(2)
    with c1:
        u1 = st.number_input("Unités produites - R1", value=20, key="u1")
        tt1 = st.number_input("Temps total (sec) - R1", value=300, key="tt1")
    with c2:
        def1 = st.number_input("Défauts - R1", value=8, key="def1")
        dt1 = st.number_input("Temps mort (sec) - R1", value=60, key="dt1")
    
    # Calculate
    oee1, lt1, wip1, fpy1, va1, prod1, ct1 = calculate_all_kpis(u1, tt1, def1, dt1)
    
    st.markdown("### Performance Mesurée")
    m1, m2, m3 = st.columns(3)
    m1.metric("OEE (Rendement)", f"{oee1*100:.1f}%")
    m2.metric("First Pass Yield", f"{fpy1*100:.1f}%")
    m3.metric("Productivité", f"{prod1:.1f} u/min")

# ==========================================
# ROUND 2 DATA
# ==========================================
with tab2:
    st.subheader("Données Post-Optimisation")
    c3, c4 = st.columns(2)
    with c3:
        u2 = st.number_input("Unités produites - R2", value=35, key="u2")
        tt2 = st.number_input("Temps total (sec) - R2", value=300, key="tt2")
    with c4:
        def2 = st.number_input("Défauts - R2", value=2, key="def2")
        dt2 = st.number_input("Temps mort (sec) - R2", value=30, key="dt2")
        
    # Calculate
    oee2, lt2, wip2, fpy2, va2, prod2, ct2 = calculate_all_kpis(u2, tt2, def2, dt2)
    
    st.markdown("### Performance Mesurée")
    m4, m5, m6 = st.columns(3)
    m4.metric("OEE (Rendement)", f"{oee2*100:.1f}%")
    m5.metric("First Pass Yield", f"{fpy2*100:.1f}%")
    m6.metric("Productivité", f"{prod2:.1f} u/min")

# ==========================================
# COMBINED ANALYSIS (VISUALS & CHARTS)
# ==========================================
with tab3:
    st.subheader("Le Pouvoir du Lean Six Sigma")
    
    # Top Comparison Row
    comp1, comp2, comp3 = st.columns(3)
    comp1.metric("Cycle Time", f"{ct2:.1f}s", f"{ct2-ct1:.1f}s", delta_color="inverse")
    comp2.metric("OEE", f"{oee2*100:.1f}%", f"{(oee2-oee1)*100:.1f}%")
    comp3.metric("Productivité", f"{prod2:.1f}", f"{prod2-prod1:.1f}")
    
    st.markdown("<hr style='border: 0.5px solid rgba(128,128,128,0.2);'>", unsafe_allow_html=True)

    # --- COMPARISON TABLE ---
    kpi_names = ["OEE (%)", "Lead Time (s)", "WIP", "First Pass Yield (%)", "Taux VA (%)", "Productivité"]
    r1_vals = [oee1*100, lt1, wip1, fpy1*100, va1*100, prod1]
    r2_vals = [oee2*100, lt2, wip2, fpy2*100, va2*100, prod2]
    
    df_table = pd.DataFrame({
        "Métrique": kpi_names,
        "Avant (R1)": [f"{v:.1f}" for v in r1_vals],
        "Après (R2)": [f"{v:.1f}" for v in r2_vals],
        "Amélioration": [f"{((r2_vals[i]-r1_vals[i])/r1_vals[i]*100):+.1f}%" if r1_vals[i] != 0 else "0%" for i in range(len(r1_vals))]
    })
    st.dataframe(df_table, use_container_width=True, hide_index=True)

    # --- BAR CHARTS (The Visuals) ---
    st.markdown("<br>", unsafe_allow_html=True)
    viz_col1, viz_col2, viz_col3 = st.columns(3)

    def style_fig(fig, title):
        fig.update_layout(title=title, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                          showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
        fig.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
        return fig

    with viz_col1:
        f1 = px.bar(x=["Round 1", "Round 2"], y=[oee1*100, oee2*100], color=["Round 1", "Round 2"],
                    color_discrete_map={"Round 1": "#86868b", "Round 2": "#0071e3"})
        st.plotly_chart(style_fig(f1, "OEE %"), use_container_width=True)

    with viz_col2:
        f2 = px.bar(x=["Round 1", "Round 2"], y=[fpy1*100, fpy2*100], color=["Round 1", "Round 2"],
                    color_discrete_map={"Round 1": "#86868b", "Round 2": "#ff3b30"})
        st.plotly_chart(style_fig(f2, "FPY (Qualité) %"), use_container_width=True)

    with viz_col3:
        f3 = px.bar(x=["Round 1", "Round 2"], y=[prod1, prod2], color=["Round 1", "Round 2"],
                    color_discrete_map={"Round 1": "#86868b", "Round 2": "#bf5af2"})
        st.plotly_chart(style_fig(f3, "Productivité"), use_container_width=True)

    # --- CONTROL CHARTS (X-BAR & R) ---
    st.markdown("<br><hr style='border: 0.5px solid rgba(128,128,128,0.2);'>", unsafe_allow_html=True)
    st.subheader("Suivi Statistique (X̄ & R) - Post-Optimisation")
    
    n_groups = 20
    x_bar_vals = [random.gauss(ct2, ct2*0.05) for _ in range(n_groups)]
    r_vals = [random.uniform(0, ct2*0.1) for _ in range(n_groups)]
    
    c_chart1, c_chart2 = st.columns(2)
    with c_chart1:
        fig_x = go.Figure()
        fig_x.add_trace(go.Scatter(y=x_bar_vals, mode='lines+markers', line_color='#0071e3'))
        fig_x.add_hline(y=sum(x_bar_vals)/n_groups, line_color="#34c759", annotation_text="X̄")
        st.plotly_chart(style_fig(fig_x, "Carte des Moyennes (X̄)"), use_container_width=True)
    with c_chart2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(y=r_vals, mode='lines+markers', line_color='#bf5af2'))
        fig_r.add_hline(y=sum(r_vals)/n_groups, line_color="#34c759", annotation_text="R̄")
        st.plotly_chart(style_fig(fig_r, "Carte des Étendues (R)"), use_container_width=True)
