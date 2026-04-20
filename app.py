import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# --- 5. TABS SETUP (Updated with 4th Tab) ---
tab1, tab2, tab3, tab4 = st.tabs(["Round 1", "Round 2", "Combined Analysis", "X & R Control"])

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
    
    st.markdown("### Measured Performance (Original)")
    k1, k2, k3 = st.columns(3)
    k1.metric("⏱️ Cycle Time", f"{res1['ct']:.1f}s")
    k2.metric("⚠️ Defect Rate", f"{res1['dr']:.1f}%")
    k3.metric("🛑 Temps mort", f"{res1['dt']:.1f}%")

    st.markdown("### Industrial Indicators (Added)")
    n1, n2, n3 = st.columns(3)
    n1.metric("OEE", f"{res1['oee']:.1f}%")
    n2.metric("First Pass Yield", f"{res1['fpy']:.1f}%")
    n3.metric("Productivité", f"{res1['prod']:.1f} u/min")

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
    
    st.markdown("### Measured Performance (Original)")
    k4, k5, k6 = st.columns(3)
    k4.metric("⏱️ Cycle Time", f"{res2['ct']:.1f}s")
    k5.metric("⚠️ Defect Rate", f"{res2['dr']:.1f}%")
    k6.metric("🛑 Temps mort", f"{res2['dt']:.1f}%")

    st.markdown("### Industrial Indicators (Added)")
    n4, n5, n6 = st.columns(3)
    n4.metric("OEE", f"{res2['oee']:.1f}%")
    n5.metric("First Pass Yield", f"{res2['fpy']:.1f}%")
    n6.metric("Productivité", f"{res2['prod']:.1f} u/min")

# ==========================================
# TAB 3: COMBINED & VISUALS (Random SPC Removed)
# ==========================================
with tab3:
    st.subheader("Comparison Analysis")
    
    c_col1, c_col2, c_col3 = st.columns(3)
    c_col1.metric("Cycle Time", f"{res2['ct']:.1f}s", delta=f"{res2['ct']-res1['ct']:.1f}s", delta_color="inverse")
    c_col2.metric("OEE", f"{res2['oee']:.1f}%", delta=f"{res2['oee']-res1['oee']:.1f}%")
    c_col3.metric("WIP", f"{res2['wip']:.2f}", delta=f"{res2['wip']-res1['wip']:.2f}", delta_color="inverse")

    st.divider()

    # --- FULL TABLE ---
    kpi_list = ["Cycle Time", "Defect Rate", "OEE", "FPY", "VA Rate", "Productivity"]
    r1_list = [res1['ct'], res1['dr'], res1['oee'], res1['fpy'], res1['va'], res1['prod']]
    r2_list = [res2['ct'], res2['dr'], res2['oee'], res2['fpy'], res2['va'], res2['prod']]
    
    df_table = pd.DataFrame({
        "Metric": kpi_list,
        "Before (R1)": [f"{v:.1f}" for v in r1_list],
        "After (R2)": [f"{v:.1f}" for v in r2_list],
        "Impact": [f"{((r2_list[i]-r1_list[i])/r1_list[i]*100):+.1f}%" if r1_list[i] != 0 else "0%" for i in range(len(kpi_list))]
    })
    st.dataframe(df_table, use_container_width=True, hide_index=True)

    # --- ORIGINAL CHARTS ---
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

# ==========================================
# TAB 4: X & R CONTROL (Real User Input)
# ==========================================
with tab4:
    st.subheader("📊 X̄ & R Control Charts (Real Data Entry)")

    st.markdown("### Configuration")

    colA, colB = st.columns(2)
    with colA:
        n_groups = st.number_input("Number of Posts", min_value=2, max_value=10, value=3)
    with colB:
        n_obs = st.number_input("Cycle Time Measurements", min_value=2, max_value=10, value=5)

    st.markdown("### Enter Cycle Time Data")

    data = []
    for i in range(n_groups):
        cols = st.columns(n_obs)
        row = []
        for j in range(n_obs):
            val = cols[j].number_input(
                f"Post {i+1} - Cycle {j+1}",
                value=10.0,
                key=f"{i}-{j}"
            )
            row.append(val)
        data.append(row)

    data = np.array(data)

    # --- CALCULATIONS ---
    means = data.mean(axis=1)
    ranges = data.max(axis=1) - data.min(axis=1)

    X_bar_bar = means.mean()
    R_bar = ranges.mean()

    # --- CONSTANTS (adapted for subgroup size) ---
    constants = {
        2: (1.88, 0, 3.267),
        3: (1.023, 0, 2.574),
        4: (0.729, 0, 2.282),
        5: (0.577, 0, 2.114),
        6: (0.483, 0, 2.004),
        7: (0.419, 0.076, 1.924),
        8: (0.373, 0.136, 1.864),
        9: (0.337, 0.184, 1.816),
        10: (0.308, 0.223, 1.777),
    }

    A2, D3, D4 = constants.get(n_obs, (0.577, 0, 2.114))

    # --- LIMITS ---
    UCL_x = X_bar_bar + A2 * R_bar
    LCL_x = X_bar_bar - A2 * R_bar

    UCL_r = D4 * R_bar
    LCL_r = D3 * R_bar

    st.markdown("### 📈 X̄ Chart")

    fig_x = go.Figure()
    fig_x.add_trace(go.Scatter(y=means, mode='lines+markers', name="Means"))

    fig_x.add_hline(y=X_bar_bar, line_color="green", annotation_text="Mean")
    fig_x.add_hline(y=UCL_x, line_color="red", line_dash="dash", annotation_text="UCL")
    fig_x.add_hline(y=LCL_x, line_color="red", line_dash="dash", annotation_text="LCL")

    st.plotly_chart(fig_x, use_container_width=True)

    st.markdown("### 📊 R Chart")

    fig_r = go.Figure()
    fig_r.add_trace(go.Scatter(y=ranges, mode='lines+markers', name="Range"))

    fig_r.add_hline(y=R_bar, line_color="green", annotation_text="Mean")
    fig_r.add_hline(y=UCL_r, line_color="red", line_dash="dash", annotation_text="UCL")
    fig_r.add_hline(y=LCL_r, line_color="red", line_dash="dash", annotation_text="LCL")

    st.plotly_chart(fig_r, use_container_width=True)
