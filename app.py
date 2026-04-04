import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- CUSTOM CSS FOR ANIMATIONS & LOGO ---
st.markdown("""
    <style>
    /* Premium background gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
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
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 700;
        color: #1d1d1f;
        font-size: 3rem !important;
        margin-bottom: 0px !important;
    }
    
    h3 {
        font-weight: 600;
        color: #1d1d1f;
        margin-top: 1.5rem !important;
    }

    /* Glassmorphism KPI Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 18px;
        padding: 20px 25px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.1);
        background: rgba(255, 255, 255, 0.85);
    }
    
    .stDataFrame {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    }

    /* PURE CSS ANIMATED LOGO */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 15px;
    }
    .lss-logo {
        width: 65px;
        height: 65px;
        background: linear-gradient(135deg, #0071e3 0%, #bf5af2 100%);
        border-radius: 16px;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 32px;
        font-weight: bold;
        font-family: -apple-system, sans-serif;
        box-shadow: 0 10px 20px rgba(0, 113, 227, 0.2);
        animation: logoPulse 2.5s infinite alternate ease-in-out;
    }
    .logo-text {
        font-family: -apple-system, sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        color: #1d1d1f;
        line-height: 1.2;
    }
    @keyframes logoPulse {
        0% { transform: scale(1); box-shadow: 0 5px 15px rgba(0, 113, 227, 0.2); }
        100% { transform: scale(1.05); box-shadow: 0 15px 30px rgba(191, 90, 242, 0.4); }
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION WITH ANIMATED LOGO ---
col_title, col_logo = st.columns([3, 1])
with col_title:
    st.title("Lean Six Sigma")
    st.markdown("<p style='color: #86868b; font-size: 1.2rem; margin-top: -5px;'>Experience the power of efficiency.</p>", unsafe_allow_html=True)
with col_logo:
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text">LEAN<br>SIX SIGMA</div>
            <div class="lss-logo">Σ</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- CALCULATION FUNCTION ---
def calculate_kpis(production, lead_time, defects, downtime):
    cycle_time = lead_time / production if production > 0 else 0
    defect_rate = (defects / production) * 100 if production > 0 else 0
    downtime_rate = (downtime / lead_time) * 100 if lead_time > 0 else 0
    return cycle_time, defect_rate, downtime_rate

# --- TABS SETUP ---
tab1, tab2, tab3 = st.tabs(["Round 1", "Round 2", "Combined"])

# ==========================================
# TAB 1: ROUND 1
# ==========================================
with tab1:
    st.subheader("Initial Data Collection")
    col1, col2 = st.columns(2)
    
    with col1:
        prod1 = st.number_input("Production (Units) - R1", value=20, min_value=0, step=1)
        lead_time1 = st.number_input("Lead Time (sec) - R1", value=300, min_value=0, step=10)
    with col2:
        defects1 = st.number_input("Defects - R1", value=8, min_value=0, step=1)
        downtime1 = st.number_input("Temps mort (sec) - R1", value=60, min_value=0, step=5)

    ct1, dr1, dt1 = calculate_kpis(prod1, lead_time1, defects1, downtime1)
    
    st.markdown("### Measured Performance")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="⏱️ Cycle Time", value=f"{ct1:.1f}s")
    kpi2.metric(label="⚠️ Defect Rate", value=f"{dr1:.1f}%")
    kpi3.metric(label="🛑 Temps mort", value=f"{dt1:.1f}%")

# ==========================================
# TAB 2: ROUND 2
# ==========================================
with tab2:
    st.subheader("Post-Optimization Data")
    col1, col2 = st.columns(2)
    
    with col1:
        prod2 = st.number_input("Production (Units) - R2", value=35, min_value=0, step=1)
        lead_time2 = st.number_input("Lead Time (sec) - R2", value=300, min_value=0, step=10)
    with col2:
        defects2 = st.number_input("Defects - R2", value=2, min_value=0, step=1)
        downtime2 = st.number_input("Temps mort (sec) - R2", value=30, min_value=0, step=5)

    ct2, dr2, dt2 = calculate_kpis(prod2, lead_time2, defects2, downtime2)
    
    st.markdown("### Measured Performance")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="⏱️ Cycle Time", value=f"{ct2:.1f}s")
    kpi2.metric(label="⚠️ Defect Rate", value=f"{dr2:.1f}%")
    kpi3.metric(label="🛑 Temps mort", value=f"{dt2:.1f}%")

# ==========================================
# TAB 3: COMBINED
# ==========================================
with tab3:
    st.subheader("The Results Speak for Themselves")
    
    ct_diff = ct2 - ct1
    dr_diff = dr2 - dr1
    dt_diff = dt2 - dt1

    comp1, comp2, comp3 = st.columns(3)
    comp1.metric("Cycle Time", f"{ct2:.1f}s", delta=f"{ct_diff:.1f}s", delta_color="inverse")
    comp2.metric("Defect Rate", f"{dr2:.1f}%", delta=f"{dr_diff:.1f}%", delta_color="inverse")
    comp3.metric("Temps mort", f"{dt2:.1f}%", delta=f"{dt_diff:.1f}%", delta_color="inverse")
    
    st.markdown("<hr style='border: 0.5px solid rgba(0,0,0,0.05);'>", unsafe_allow_html=True)

    kpi_names = ["Cycle Time", "Defect Rate", "Temps mort"]
    r1_values = [ct1, dr1, dt1]
    r2_values = [ct2, dr2, dt2]
    
    imp_ct = ((ct1 - ct2) / ct1 * 100) if ct1 > 0 else 0
    imp_dr = ((dr1 - dr2) / dr1 * 100) if dr1 > 0 else 0
    imp_dt = ((dt1 - dt2) / dt1 * 100) if dt1 > 0 else 0
    improvements = [f"Reduced by {imp_ct:.1f}%", f"Reduced by {imp_dr:.1f}%", f"Reduced by {imp_dt:.1f}%"]

    # --- TABLE ---
    df_table = pd.DataFrame({
        "Metric": kpi_names,
        "Before (R1)": [f"{v:.1f}" for v in r1_values],
        "After (R2)": [f"{v:.1f}" for v in r2_values],
        "Result": improvements
    })
    st.dataframe(df_table, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- VISUALIZATIONS ---
    df_chart = pd.DataFrame({
        "KPI": kpi_names * 2,
        "Value": r1_values + r2_values,
        "Round": ["Round 1"] * 3 + ["Round 2"] * 3
    })

    chart_col1, chart_col2, chart_col3 = st.columns(3)

    def style_apple_chart(fig):
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_family="-apple-system, BlinkMacSystemFont",
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        return fig

    with chart_col1:
        fig_ct = px.bar(df_chart[df_chart["KPI"] == "Cycle Time"], 
                        x="Round", y="Value", color="Round", text_auto='.1f',
                        title="Cycle Time", 
                        color_discrete_map={"Round 1": "#86868b", "Round 2": "#0071e3"})
        st.plotly_chart(style_apple_chart(fig_ct), use_container_width=True)

    with chart_col2:
        fig_dr = px.bar(df_chart[df_chart["KPI"] == "Defect Rate"], 
                        x="Round", y="Value", color="Round", text_auto='.1f',
                        title="Defect Rate",
                        color_discrete_map={"Round 1": "#86868b", "Round 2": "#1d1d1f"})
        st.plotly_chart(style_apple_chart(fig_dr), use_container_width=True)

    with chart_col3:
        fig_dt = px.bar(df_chart[df_chart["KPI"] == "Temps mort"], 
                        x="Round", y="Value", color="Round", text_auto='.1f',
                        title="Temps mort",
                        color_discrete_map={"Round 1": "#86868b", "Round 2": "#bf5af2"})
        st.plotly_chart(style_apple_chart(fig_dt), use_container_width=True)
