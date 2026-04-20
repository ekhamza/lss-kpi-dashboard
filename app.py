import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import numpy as np
# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- 2. ADAPTIVE CSS (Original Styling Preserved) ---
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

    h1 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 700;
        font-size: 3rem !important;
        margin-bottom: 0px !important;
    }
    
    h3 {
        font-weight: 600;
        margin-top: 1.5rem !important;
    }

    /* Glassmorphism KPI Cards */
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.1); 
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 18px;
        padding: 20px 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.4s ease-in-out;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        background: rgba(128, 128, 128, 0.15);
    }

    /* PURE CSS ANIMATED LOGO */
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
    # Integration of classmate's title concept with your styling
    st.title("Simulation Lean Six Sigma")
    st.markdown("<p style='color: #86868b; font-size: 1.2rem; margin-top: -5px;'>Approche DMAIC : Experience the power of efficiency.</p>", unsafe_allow_html=True)
with col_logo:
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text" style="font-family: -apple-system; font-weight: 600; text-align: right;">LEAN<br>SIX SIGMA</div>
            <div class="lss-logo">Σ</div>
        </div>
    """, unsafe_allow_html=True)

# --- CLASSMATE'S VISUALS & CONTEXT INTEGRATION ---
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

# --- 4. CALCULATION ENGINE (Old + New Combined) ---
def calculate_all_metrics(production, total_time, defects, downtime):
    # --- ORIGINAL METRICS ---
    cycle_time = total_time / production if production > 0 else 0
    defect_rate = (defects / production) * 100 if production > 0 else 0
    downtime_rate = (downtime / total_time) * 100 if total_time > 0 else 0
    
    # --- NEW ADDED METRICS ---
    lead_time_kpi = total_time / production if production > 0 else 0
    fpy = (production - defects) / production if production > 0 else 0
    va_rate = (total_time - downtime) / total_time if total_time > 0 else 0
    wip = (production * cycle_time) / total_time if total_time > 0 else 0
    productivity = production / (total_time / 60) if total_time > 0 else 0
    oee = va_rate * 1.0 * fpy # OEE = Disponibilité * Performance (1) * Qualité
    
    return {
        "ct": cycle_time, "dr": defect_rate, "dt": downtime_rate,
        "lt": lead_time_kpi, "fpy": fpy * 100, "va": va_rate * 100,
        "wip": wip, "prod": productivity, "oee": oee * 100
    }

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["Round 1", "Round 2", "Combined Analysis", "X & R Control"])

# ================= TAB 1 =================
with tab1:
    prod1 = st.number_input("Production R1", 20)
    time1 = st.number_input("Time R1", 300)
    defects1 = st.number_input("Defects R1", 8)
    downtime1 = st.number_input("Downtime R1", 60)

    res1 = calculate_all_metrics(prod1, time1, defects1, downtime1)

    st.metric("Cycle Time", f"{res1['ct']:.2f}")
    st.metric("OEE", f"{res1['oee']:.2f}%")

# ================= TAB 2 =================
with tab2:
    prod2 = st.number_input("Production R2", 35)
    time2 = st.number_input("Time R2", 300)
    defects2 = st.number_input("Defects R2", 2)
    downtime2 = st.number_input("Downtime R2", 30)

    res2 = calculate_all_metrics(prod2, time2, defects2, downtime2)

    st.metric("Cycle Time", f"{res2['ct']:.2f}")
    st.metric("OEE", f"{res2['oee']:.2f}%")

# ================= TAB 3 =================
with tab3:
    st.subheader("Comparison")

    df = pd.DataFrame({
        "Metric": ["Cycle Time", "OEE"],
        "R1": [res1["ct"], res1["oee"]],
        "R2": [res2["ct"], res2["oee"]]
    })

    st.dataframe(df)

    fig = px.bar(df, x="Metric", y=["R1", "R2"], barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# ================= TAB 4 =================
with tab4:
    st.subheader("📊 X̄ & R Control Charts (Real Data Entry)")

    st.markdown("Enter 5 subgroups (each 5 cycle times):")

    data = []
    for i in range(5):
        cols = st.columns(5)
        row = []
        for j in range(5):
            val = cols[j].number_input(f"G{i+1}V{j+1}", value=10.0, key=f"{i}-{j}")
            row.append(val)
        data.append(row)

    data = np.array(data)

    means = data.mean(axis=1)
    ranges = data.max(axis=1) - data.min(axis=1)

    X_bar_bar = means.mean()
    R_bar = ranges.mean()

    # Six Sigma constants (n=5)
    A2 = 0.577
    D3 = 0
    D4 = 2.114

    UCL_x = X_bar_bar + A2 * R_bar
    LCL_x = X_bar_bar - A2 * R_bar

    UCL_r = D4 * R_bar
    LCL_r = D3 * R_bar

    # --- X BAR ---
    fig_x = go.Figure()
    fig_x.add_trace(go.Scatter(y=means, mode='lines+markers', name="Means"))
    fig_x.add_hline(y=X_bar_bar, line_color="green", annotation_text="Mean")
    fig_x.add_hline(y=UCL_x, line_color="red", line_dash="dash", annotation_text="UCL")
    fig_x.add_hline(y=LCL_x, line_color="red", line_dash="dash", annotation_text="LCL")

    st.plotly_chart(fig_x, use_container_width=True)

    # --- R ---
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatter(y=ranges, mode='lines+markers', name="Range"))
    fig_r.add_hline(y=R_bar, line_color="green", annotation_text="Mean")
    fig_r.add_hline(y=UCL_r, line_color="red", line_dash="dash", annotation_text="UCL")
    fig_r.add_hline(y=LCL_r, line_color="red", line_dash="dash", annotation_text="LCL")

    st.plotly_chart(fig_r, use_container_width=True)

    # --- ORIGINAL CHARTS + NEW CHARTS ---
    st.markdown("### Performance Visualizations")
    v_col1, v_col2, v_col3 = st.columns(3)

    def style_fig(fig, title):
        fig.update_layout(title=title, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        return fig

    with v_col1:
        f1 = px.bar(x=["R1", "R2"], y=[res1['ct'], res2['ct']], color=["R1", "R2"], color_discrete_map={"R1": "#86868b", "R2": "#0071e3"})
        st.plotly_chart(style_fig(f1, "Cycle Time Evolution"), use_container_width=True)
    with v_col2:
        f2 = px.bar(x=["R1", "R2"], y=[res1['oee'], res2['oee']], color=["R1", "R2"], color_discrete_map={"R1": "#86868b", "R2": "#34c759"})
        st.plotly_chart(style_fig(f2, "OEE %"), use_container_width=True)
    with v_col3:
        f3 = px.bar(x=["R1", "R2"], y=[res1['prod'], res2['prod']], color=["R1", "R2"], color_discrete_map={"R1": "#86868b", "R2": "#bf5af2"})
        st.plotly_chart(style_fig(f3, "Productivity"), use_container_width=True)

