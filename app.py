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
    st.subheader("📊 X̄ & R Control Charts (Cycle Time per Operator)")
    st.markdown("""
    - Each post represents one operator station
    - Cycle time is entered manually per post (5 samples)
    - Control charts are computed automatically
    """)
    
    st.markdown("<br>### Input Operator Data", unsafe_allow_html=True)
    
    # Headers for grid
    h_cols = st.columns(6)
    h_cols[0].markdown("**Station**")
    for j in range(1, 6):
        h_cols[j].markdown(f"**Sample {j}**")
        
    # Input matrix configuration
    user_data = []
    for i in range(1, 7):
        cols = st.columns(6)
        cols[0].markdown(f"<div style='margin-top: 8px; font-weight: 600; color: #0071e3;'>Post {i}</div>", unsafe_allow_html=True)
        post_values = []
        for j in range(1, 6):
            val = cols[j].number_input(f"P{i}S{j}", value=10.0, step=0.1, key=f"post{i}_s{j}", label_visibility="collapsed")
            post_values.append(val)
        user_data.append(post_values)
        
    # Data transformation
    data_array = np.array(user_data)
    
    # Mathematical calculation exactly as requested
    means = data_array.mean(axis=1)
    ranges = data_array.max(axis=1) - data_array.min(axis=1)
    
    X_bar_bar = np.mean(means)
    R_bar = np.mean(ranges)
    
    # Constants for n=5
    A2 = 0.577
    D3 = 0
    D4 = 2.114
    
    # Limits calculations
    UCL_x = X_bar_bar + (A2 * R_bar)
    LCL_x = X_bar_bar - (A2 * R_bar)
    
    UCL_r = D4 * R_bar
    LCL_r = D3 * R_bar
    
    st.divider()
    st.markdown("### Process Stability Visualizations")
    
    post_labels = [f"Post {i}" for i in range(1, 7)]

    def style_control_fig(fig, title):
        fig.update_layout(title=title, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
        return fig

    c_chart1, c_chart2 = st.columns(2)
    
    # X-BAR CHART PLOTTING
    with c_chart1:
        fig_x_ctrl = go.Figure(go.Scatter(x=post_labels, y=means, mode='lines+markers', line_color='#0071e3'))
        fig_x_ctrl.add_hline(y=X_bar_bar, line_color="#34c759", annotation_text=f"Mean (X̄̄): {X_bar_bar:.2f}")
        fig_x_ctrl.add_hline(y=UCL_x, line_color="#ff3b30", line_dash="dash", annotation_text=f"UCL: {UCL_x:.2f}")
        fig_x_ctrl.add_hline(y=LCL_x, line_color="#ff3b30", line_dash="dash", annotation_text=f"LCL: {LCL_x:.2f}")
        st.plotly_chart(style_control_fig(fig_x_ctrl, "Carte X-Bar (Means per Post)"), use_container_width=True)
        
    # R CHART PLOTTING
    with c_chart2:
        fig_r_ctrl = go.Figure(go.Scatter(x=post_labels, y=ranges, mode='lines+markers', line_color='#bf5af2'))
        fig_r_ctrl.add_hline(y=R_bar, line_color="#34c759", annotation_text=f"R-bar: {R_bar:.2f}")
        fig_r_ctrl.add_hline(y=UCL_r, line_color="#ff3b30", line_dash="dash", annotation_text=f"UCL: {UCL_r:.2f}")
        fig_r_ctrl.add_hline(y=LCL_r, line_color="#ff3b30", line_dash="dash", annotation_text=f"LCL: {LCL_r:.2f}")
        st.plotly_chart(style_control_fig(fig_r_ctrl, "Carte R (Ranges per Post)"), use_container_width=True)
