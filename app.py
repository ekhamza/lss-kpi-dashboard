import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- STYLE FUNCTION (Defined early to avoid NameErrors) ---
def style_control_chart(fig, title_text, y_label):
    fig.update_layout(
        title=title_text,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="-apple-system, sans-serif",
        showlegend=False,
        margin=dict(l=60, r=40, t=50, b=60)
    )
    fig.update_xaxes(title_text="Sous-groupes (n=5)", showgrid=False)
    fig.update_yaxes(title_text=y_label, showgrid=True, gridcolor='rgba(128,128,128,0.2)')
    return fig

# --- CSS STYLING ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.1); 
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 15px;
        padding: 15px !important;
    }
    h1 { font-size: 3rem !important; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("Lean Six Sigma")
st.markdown("Experience the power of efficiency.")

# --- CALCULATION FUNCTION ---
def calculate_kpis(production, lead_time, defects, downtime):
    ct = lead_time / production if production > 0 else 0
    dr = (defects / production) * 100 if production > 0 else 0
    dt = (downtime / lead_time) * 100 if lead_time > 0 else 0
    return ct, dr, dt

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["Round 1", "Round 2", "Combined"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        prod1 = st.number_input("Production - R1", value=20)
        lt1 = st.number_input("Lead Time - R1", value=300)
    with col2:
        def1 = st.number_input("Defects - R1", value=8)
        dt_val1 = st.number_input("Temps mort - R1", value=60)
    ct1, dr1, dt1 = calculate_kpis(prod1, lt1, def1, dt_val1)
    
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        prod2 = st.number_input("Production - R2", value=35)
        lt2 = st.number_input("Lead Time - R2", value=300)
    with col2:
        def2 = st.number_input("Defects - R2", value=2)
        dt_val2 = st.number_input("Temps mort - R2", value=30)
    ct2, dr2, dt2 = calculate_kpis(prod2, lt2, def2, dt_val2)

with tab3:
    st.subheader("The Results Speak for Themselves")
    
    # FIX: Corrected the variable names here to match ct1, dr1, dt1
    c1, c2, c3 = st.columns(3)
    c1.metric("Cycle Time", f"{ct2:.1f}s", delta=f"{ct2-ct1:.1f}s", delta_color="inverse")
    c2.metric("Defect Rate", f"{dr2:.1f}%", delta=f"{dr2-dr1:.1f}%", delta_color="inverse")
    c3.metric("Temps mort", f"{dt2:.1f}%", delta=f"{dt2-dt1:.1f}%", delta_color="inverse")

    # --- CONTROL CHARTS ---
    st.markdown("---")
    st.subheader("Cartes de Contrôle (X̄ & R)")
    
    # Simulation
    n_subgroups = 20
    x_bar_vals, r_vals = [], []
    variation = ct2 * 0.05 if ct2 > 0 else 1
    
    for _ in range(n_subgroups):
        samples = [random.gauss(ct2, variation) for _ in range(5)]
        x_bar_vals.append(sum(samples)/5)
        r_vals.append(max(samples)-min(samples))
    
    x_double_bar = sum(x_bar_vals)/20
    r_bar = sum(r_vals)/20
    
    ucl_x, lcl_x = x_double_bar + (0.577 * r_bar), x_double_bar - (0.577 * r_bar)
    ucl_r, lcl_r = 2.114 * r_bar, 0
    
    cc1, cc2 = st.columns(2)
    
    with cc1:
        fig_x = go.Figure()
        fig_x.add_trace(go.Scatter(y=x_bar_vals, mode='lines+markers', line_color='#0071e3'))
        fig_x.add_hline(y=ucl_x, line_dash="dash", line_color="red")
        fig_x.add_hline(y=lcl_x, line_dash="dash", line_color="red")
        st.plotly_chart(style_control_chart(fig_x, "Carte des Moyennes (X̄)", "Secondes"), use_container_width=True)

    with cc2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(y=r_vals, mode='lines+markers', line_color='#bf5af2'))
        fig_r.add_hline(y=ucl_r, line_dash="dash", line_color="red")
        st.plotly_chart(style_control_chart(fig_r, "Carte des Étendues (R)", "Variation"), use_container_width=True)
