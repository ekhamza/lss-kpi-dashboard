import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="LSS Dashboard Pro", page_icon="📈", layout="wide")

# --- ADAPTIVE CSS FOR LIGHT/DARK MODE ---
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
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 700;
        color: var(--text-color) !important; /* Automatically switches between black/white */
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
        background: rgba(128, 128, 128, 0.1); /* Semi-transparent grey works on light AND dark */
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
    
    .stDataFrame {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
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
        color: var(--text-color); /* Automatically switches between black/white */
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
