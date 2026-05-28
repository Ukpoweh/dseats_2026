# =========================================================
# GEOTWIN-DC v11 — STREAMLIT PRODUCTION TWIN DASHBOARD
# SPE AFRICA GEOTHERMAL DATATHON 2026
# Upgraded: Dark cyberpunk theme, animations, improved charts
# =========================================================

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time

st.set_page_config(
    page_title="GEOTWIN-DC | SPE Africa 2026",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL THEME INJECTION
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

/* ── Root palette ── */
:root {
    --geo-bg:      #0a0f1a;
    --geo-panel:   #0e1624;
    --geo-border:  rgba(0,210,140,0.18);
    --geo-green:   #00d28c;
    --geo-teal:    #00b4d8;
    --geo-amber:   #f4a532;
    --geo-red:     #ff4d6d;
    --geo-purple:  #a78bfa;
    --geo-text:    rgba(255,255,255,0.88);
    --geo-muted:   rgba(255,255,255,0.42);
    --geo-mono:    'Space Mono', monospace;
    --geo-body:    'DM Sans', sans-serif;
}

/* ── App shell ── */
.stApp { background: var(--geo-bg) !important; color: var(--geo-text) !important; font-family: var(--geo-body); }
section[data-testid="stSidebar"] { background: var(--geo-panel) !important; border-right: 1px solid var(--geo-border); }
header[data-testid="stHeader"] { background: var(--geo-bg) !important; border-bottom: 1px solid var(--geo-border); }

/* ── Headings ── */
h1, h2, h3 { font-family: var(--geo-mono) !important; letter-spacing: 0.04em !important; }
h1 { color: var(--geo-green) !important; font-size: 1.5rem !important; }
h2 { color: var(--geo-text) !important; font-size: 1.1rem !important; }
h3 { color: var(--geo-teal) !important; font-size: 0.9rem !important; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--geo-panel) !important;
    border: 1px solid var(--geo-border) !important;
    border-radius: 8px !important;
    padding: 18px !important;
    position: relative !important;
    overflow: hidden !important;
    transition: border-color 0.25s, transform 0.2s !important;
}
[data-testid="metric-container"]:hover {
    border-color: rgba(0,210,140,0.45) !important;
    transform: translateY(-2px) !important;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--geo-green), transparent);
}
[data-testid="stMetricLabel"] > div {
    font-family: var(--geo-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    color: var(--geo-muted) !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--geo-mono) !important;
    color: var(--geo-green) !important;
    font-size: 1.7rem !important;
}
[data-testid="stMetricDelta"] { font-size: 0.68rem !important; font-family: var(--geo-mono) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--geo-panel) !important;
    border-bottom: 1px solid var(--geo-border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--geo-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    color: var(--geo-muted) !important;
    border-bottom: 2px solid transparent !important;
    padding: 12px 20px !important;
    background: transparent !important;
    transition: color 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--geo-green) !important;
    border-bottom: 2px solid var(--geo-green) !important;
    background: rgba(0,210,140,0.05) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--geo-panel) !important;
    border: 1px solid var(--geo-border) !important;
    border-radius: 0 8px 8px 8px !important;
    padding: 20px !important;
}

/* ── Sidebar sliders ── */
.stSlider > div > div > div { background: var(--geo-green) !important; }
.stSlider [data-testid="stThumbValue"] { 
    font-family: var(--geo-mono) !important;
    font-size: 0.7rem !important;
    color: var(--geo-green) !important;
}

/* ── Sidebar labels ── */
.stSidebar label {
    font-family: var(--geo-mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.06em !important;
    color: var(--geo-muted) !important;
    text-transform: uppercase !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--geo-green) !important;
    color: var(--geo-green) !important;
    font-family: var(--geo-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 4px !important;
    padding: 8px 16px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(0,210,140,0.12) !important;
    box-shadow: 0 0 14px rgba(0,210,140,0.25) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: rgba(0,210,140,0.1) !important;
    border: 1px solid var(--geo-green) !important;
    color: var(--geo-green) !important;
    font-family: var(--geo-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    border-radius: 4px !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border: 1px solid var(--geo-border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrameResizable"] { background: var(--geo-panel) !important; }

/* ── Dividers ── */
hr { border-color: var(--geo-border) !important; }

/* ── Caption / footer ── */
.stCaption, .caption {
    font-family: var(--geo-mono) !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.08em !important;
    color: var(--geo-muted) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--geo-panel); }
::-webkit-scrollbar-thumb { background: rgba(0,210,140,0.35); border-radius: 2px; }

/* ── Animated scan line on load ── */
@keyframes scan-load {
    0%   { transform: translateY(-100%); opacity: 0; }
    10%  { opacity: 0.6; }
    90%  { opacity: 0.6; }
    100% { transform: translateY(200vh); opacity: 0; }
}
.scan-overlay {
    position: fixed; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, transparent, #00d28c 40%, transparent);
    animation: scan-load 1.8s ease-out forwards;
    pointer-events: none; z-index: 9999;
}

/* ── KPI pulse for reliability ── */
@keyframes kpi-pulse {
    0%, 100% { text-shadow: 0 0 8px rgba(0,210,140,0.4); }
    50%       { text-shadow: 0 0 18px rgba(0,210,140,0.85), 0 0 30px rgba(0,210,140,0.3); }
}
.kpi-pulse { animation: kpi-pulse 2.5s ease-in-out infinite; }

/* ── Status tags in table ── */
.tag-sel  { background: rgba(0,210,140,0.12); color: #00d28c; border: 1px solid rgba(0,210,140,0.4); padding: 2px 8px; border-radius: 3px; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.06em; }
.tag-ret  { background: rgba(0,180,216,0.12); color: #00b4d8; border: 1px solid rgba(0,180,216,0.4); padding: 2px 8px; border-radius: 3px; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.06em; }
.tag-std  { background: rgba(244,165,50,0.12); color: #f4a532; border: 1px solid rgba(244,165,50,0.4); padding: 2px 8px; border-radius: 3px; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.06em; }
.tag-exc  { background: rgba(255,77,109,0.10); color: #ff4d6d; border: 1px solid rgba(255,77,109,0.3); padding: 2px 8px; border-radius: 3px; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.06em; }

/* ── Sidebar section dividers ── */
.sidebar-section-title {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.14em !important;
    color: rgba(0,210,140,0.6) !important;
    text-transform: uppercase !important;
    margin: 12px 0 6px 0 !important;
}
</style>

<!-- Scan-line animation on first render -->
<div class="scan-overlay"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
SEED = 42
np.random.seed(SEED)

years = 15
total_months = years * 12
hours_per_month = 730
discount_rate = 0.066

cp = 4250
T_reservoir = 94
T_reinject = 30
delta_T = T_reservoir - T_reinject

surface_cost_per_MW     = 150_000
storage_cost_per_MWh    = 100_000
fixed_om_rate_per_mw    = 8_791.01
variable_om_rate_per_mwh = 5.55556

monthly_demand_factor = np.array([
    1.28, 1.24, 1.15, 1.05, 0.95, 0.85,
    0.75, 0.78, 0.90, 1.02, 1.15, 1.30
])

# ─────────────────────────────────────────────
# PLOTLY DARK THEME DEFAULTS
# ─────────────────────────────────────────────
GEO_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(14,22,36,0.7)",
    font=dict(family="Space Mono, monospace", color="rgba(255,255,255,0.7)", size=10),
    margin=dict(l=50, r=30, t=40, b=40),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)",
        tickfont=dict(size=9), showgrid=True,
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)",
        tickfont=dict(size=9), showgrid=True,
    ),
    legend=dict(
        bgcolor="rgba(14,22,36,0.7)", bordercolor="rgba(0,210,140,0.2)",
        borderwidth=1, font=dict(size=9, family="Space Mono, monospace"),
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
    ),
)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="width:46px;height:46px;border-radius:8px;background:rgba(0,210,140,0.12);
         border:1px solid rgba(0,210,140,0.4);display:flex;align-items:center;justify-content:center;
         font-size:1.4rem;">🌍</div>
    """, unsafe_allow_html=True)
with col_title:
    st.markdown("""
    <div style="padding-top:4px">
      <div style="font-family:'Space Mono',monospace;font-size:1.6rem;font-weight:700;
           color:#00d28c;letter-spacing:0.05em">GEOTWIN-DC</div>
      <div style="font-family:'DM Sans',sans-serif;font-size:0.8rem;
           color:rgba(255,255,255,0.45);margin-top:2px">
        SPE Africa Geothermal Datathon 2026 &nbsp;·&nbsp; Integrated Asset Management Portal
        &nbsp;&nbsp;<span style="background:rgba(0,210,140,0.12);border:1px solid rgba(0,210,140,0.35);
        color:#00d28c;font-family:'Space Mono',monospace;font-size:0.6rem;
        padding:2px 8px;border-radius:3px;letter-spacing:0.1em">● LIVE SIM</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align:center;padding:12px 0 8px">
  <div style="font-family:'Space Mono',monospace;font-size:0.75rem;
       color:#00d28c;letter-spacing:0.1em">🕹 SURFACE LOOP CONTROLLER</div>
  <div style="font-size:0.65rem;color:rgba(255,255,255,0.35);margin-top:4px">
    Real-time parameter adjustment
  </div>
</div>
""", unsafe_allow_html=True)

OPTIMAL_DEFAULTS = {"flow": 80, "demand": 18, "storage": 160, "hp": 2.50}
for key, val in OPTIMAL_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

def reset_to_optimal():
    for key, val in OPTIMAL_DEFAULTS.items():
        st.session_state[key] = val

st.sidebar.button("↺  Reset to Optimal Targets", on_click=reset_to_optimal, use_container_width=True)
st.sidebar.divider()

st.sidebar.markdown('<div class="sidebar-section-title">Reservoir Parameters</div>', unsafe_allow_html=True)
slider_flow = st.sidebar.slider("Flow Ceiling (L/s)", 40, 90, key="flow", step=5)

st.sidebar.markdown('<div class="sidebar-section-title">Demand & Grid</div>', unsafe_allow_html=True)
slider_demand = st.sidebar.slider("Community Demand (MW)", 10, 22, key="demand", step=1)

st.sidebar.markdown('<div class="sidebar-section-title">Storage & Backup</div>', unsafe_allow_html=True)
slider_storage = st.sidebar.slider("Thermal Storage (MWh)", 0, 200, key="storage", step=10)
slider_hp = st.sidebar.slider("Heat Pump Boost (MW)", 0.0, 6.0, key="hp", step=0.5)

# Live supply readout in sidebar
thermal_supply_MW = (slider_flow * cp * delta_T) / 1e6 * 0.93
st.sidebar.divider()
st.sidebar.markdown(f"""
<div style="background:rgba(0,210,140,0.06);border:1px solid rgba(0,210,140,0.2);
     border-radius:6px;padding:12px;text-align:center">
  <div style="font-family:'Space Mono',monospace;font-size:0.62rem;
       color:rgba(0,210,140,0.6);letter-spacing:0.1em;margin-bottom:4px">
    COMPUTED THERMAL SUPPLY
  </div>
  <div style="font-family:'Space Mono',monospace;font-size:1.4rem;
       font-weight:700;color:#00d28c">{thermal_supply_MW:.2f} <span style="font-size:0.8rem">MW</span></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIMULATION ENGINE
# ─────────────────────────────────────────────
storage_state = 0.5 * slider_storage if slider_storage > 0 else 0.0
charge_eff, discharge_eff = 0.92, 0.90

monthly_supply, monthly_storage_history = [], []
annual_energy_produced_mwh = np.zeros(years)
annual_shortage_mwh = np.zeros(years)

for m in range(total_months):
    idx = m % 12
    current_year = m // 12
    demand = slider_demand * monthly_demand_factor[idx]
    flow = slider_flow * np.random.normal(1.0, 0.01)
    supply_MW = thermal_supply_MW * (flow / slider_flow)
    net_power = supply_MW - demand

    if net_power > 0:
        if slider_storage > 0:
            potential_charge_energy = net_power * hours_per_month * charge_eff
            storage_state = min(slider_storage, storage_state + potential_charge_energy)
        delivered_power = demand
    else:
        deficit_power = abs(net_power)
        hp_power_delivered = storage_power_delivered = 0.0
        if slider_hp > 0:
            hp_power_delivered = min(deficit_power, slider_hp)
            deficit_power -= hp_power_delivered
        if slider_storage > 0 and deficit_power > 0:
            max_storage_power = (storage_state * discharge_eff) / hours_per_month
            storage_power_delivered = min(deficit_power, max_storage_power)
            storage_energy_used = (storage_power_delivered * hours_per_month) / discharge_eff
            storage_state -= storage_energy_used
            deficit_power -= storage_power_delivered
        delivered_power = supply_MW + hp_power_delivered + storage_power_delivered
        annual_shortage_mwh[current_year] += deficit_power * hours_per_month

    monthly_supply.append(delivered_power)
    monthly_storage_history.append(storage_state)
    annual_energy_produced_mwh[current_year] += delivered_power * hours_per_month

monthly_supply_arr = np.array(monthly_supply)
monthly_demand_arr = np.array([slider_demand * monthly_demand_factor[m % 12] for m in range(total_months)])
reliability = 1 - (np.sum(annual_shortage_mwh) / np.sum(annual_energy_produced_mwh + annual_shortage_mwh))
supply_variance = np.std(monthly_supply_arr) / np.mean(monthly_supply_arr)

# Economics
n_wells = 2
subsurface_CAPEX = n_wells * (3.237e6 + 0.3e6)
surface_CAPEX    = thermal_supply_MW * surface_cost_per_MW
storage_CAPEX    = slider_storage * storage_cost_per_MWh
heat_pump_CAPEX  = (slider_hp / 4.0) * 6_000_000 if slider_hp > 0 else 0.0
total_CAPEX      = subsurface_CAPEX + surface_CAPEX + storage_CAPEX + heat_pump_CAPEX

annual_fixed_OPEX = fixed_om_rate_per_mw * thermal_supply_MW
discounted_costs = total_CAPEX
discounted_energy = 0.0
total_co2_offset = 0.0

for y in range(years):
    t = y + 1
    yr_opex = annual_fixed_OPEX + (variable_om_rate_per_mwh * annual_energy_produced_mwh[y])
    if t in [5, 10, 15]:
        yr_opex += 300_000
    discounted_costs  += yr_opex / ((1 + discount_rate) ** t)
    discounted_energy += annual_energy_produced_mwh[y] / ((1 + discount_rate) ** t)
    total_co2_offset  += annual_energy_produced_mwh[y] * 0.24

LCOE = discounted_costs / discounted_energy

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

with k1:
    delta_str = "▲ PASS — TARGET MET" if reliability >= 0.95 else "▼ CRITICAL — BELOW THRESHOLD"
    delta_col = "normal" if reliability >= 0.95 else "inverse"
    st.metric("Grid Supply Reliability", f"{reliability*100:.2f}%", delta_str, delta_color=delta_col)

with k2:
    lcoe_str = "▼ OPTIMAL — Sub-€30/MWh" if LCOE <= 30 else "▲ REVIEW — High CAPEX Regime"
    lcoe_col = "normal" if LCOE <= 30 else "inverse"
    st.metric("Levelized Cost (LCOE)", f"€{LCOE:.2f} / MWh", lcoe_str, delta_color=lcoe_col)

with k3:
    st.metric("Total Network CAPEX", f"€{total_CAPEX/1e6:.2f} M", "Lifecycle Budget")

with k4:
    st.metric("Lifecycle CO₂ Prevented", f"{total_co2_offset:,.0f} t", "Tons offset vs grid baseline")

st.write("---")

# ─────────────────────────────────────────────
# TAB INTERFACE
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📊  Dynamic Performance",
    "🧬  Subsurface Analytics",
    "💼  Techno-Economic Reports",
])

# ══════════════════════════════════════════════
# TAB 1 — PERFORMANCE CHARTS (all Plotly)
# ══════════════════════════════════════════════
with tab1:
    st.markdown("#### Real-Time Grid Telemetry · Last 36 Months")

    plot_slice = 36
    x_months = list(range(plot_slice))

    # ── Chart A: Demand vs Supply ──
    fig_grid = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("Grid Load Matching Profile", "Thermal Energy Storage — State of Charge"),
    )
    fig_grid.update_annotations(font=dict(family="Space Mono, monospace", size=10, color="rgba(255,255,255,0.55)"))

    # Supply fill area
    fig_grid.add_trace(go.Scatter(
        x=x_months, y=list(monthly_supply_arr[-plot_slice:]),
        name="Twin Supply", mode="lines",
        line=dict(color="#00d28c", width=2.5),
        fill="tozeroy", fillcolor="rgba(0,210,140,0.07)",
    ), row=1, col=1)

    # Demand dashed
    fig_grid.add_trace(go.Scatter(
        x=x_months, y=list(monthly_demand_arr[-plot_slice:]),
        name="Community Demand", mode="lines",
        line=dict(color="#ff4d6d", width=1.8, dash="dot"),
    ), row=1, col=1)

    # Storage state
    storage_hist = monthly_storage_history[-plot_slice:]
    fig_grid.add_trace(go.Scatter(
        x=x_months, y=storage_hist,
        name="Storage Level", mode="lines",
        line=dict(color="#00b4d8", width=2),
        fill="tozeroy", fillcolor="rgba(0,180,216,0.09)",
    ), row=2, col=1)

    fig_grid.update_layout(
        **GEO_LAYOUT,
        height=420,
        showlegend=True,
    )
    fig_grid.update_yaxes(title_text="Power (MWth)", row=1, col=1, title_font=dict(size=9))
    fig_grid.update_yaxes(title_text="Energy (MWh)", row=2, col=1, title_font=dict(size=9))
    fig_grid.update_xaxes(title_text="Timeline (months)", row=2, col=1, title_font=dict(size=9))

    st.plotly_chart(fig_grid, use_container_width=True, config={"displayModeBar": False})

    st.write("")
    col_var1, col_var2 = st.columns(2)

    # ── Chart B: Annual Energy Production ──
    with col_var1:
        st.markdown("##### Annual Energy Produced (MWh)")
        fig_ann = go.Figure()
        fig_ann.add_trace(go.Bar(
            x=[f"Y{y+1}" for y in range(years)],
            y=annual_energy_produced_mwh,
            marker=dict(
                color=annual_energy_produced_mwh,
                colorscale=[[0,"#0e4a35"],[0.5,"#00955e"],[1,"#00d28c"]],
                line=dict(color="rgba(0,210,140,0.5)", width=0.5),
            ),
            hovertemplate="Year %{x}<br>%{y:,.0f} MWh<extra></extra>",
        ))
        fig_ann.update_layout(**GEO_LAYOUT, height=260, showlegend=False)
        st.plotly_chart(fig_ann, use_container_width=True, config={"displayModeBar": False})

    # ── Chart C: Annual Shortage Heatmap ──
    with col_var2:
        st.markdown("##### Annual Shortage vs Production (MWh)")
        fig_short = go.Figure()
        fig_short.add_trace(go.Bar(
            x=[f"Y{y+1}" for y in range(years)],
            y=annual_energy_produced_mwh,
            name="Produced", marker_color="rgba(0,210,140,0.6)",
        ))
        fig_short.add_trace(go.Bar(
            x=[f"Y{y+1}" for y in range(years)],
            y=annual_shortage_mwh,
            name="Shortage", marker_color="rgba(255,77,109,0.75)",
        ))
        fig_short.update_layout(
            **GEO_LAYOUT, barmode="stack", height=260,
        )
        st.plotly_chart(fig_short, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════
# TAB 2 — SUBSURFACE ANALYTICS
# ══════════════════════════════════════════════
with tab2:
    st.markdown("#### AI-RQI v3 — Subsurface Well Characterization Engine")

    # Styled well table with HTML badges
    well_html = """
    <table style="width:100%;border-collapse:collapse;font-family:'DM Sans',sans-serif;font-size:0.82rem">
      <thead>
        <tr style="border-bottom:1px solid rgba(0,210,140,0.2)">
          <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;font-size:0.62rem;letter-spacing:0.1em;color:rgba(255,255,255,0.4);text-transform:uppercase">Rank</th>
          <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;font-size:0.62rem;letter-spacing:0.1em;color:rgba(255,255,255,0.4);text-transform:uppercase">Well ID</th>
          <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;font-size:0.62rem;letter-spacing:0.1em;color:rgba(255,255,255,0.4);text-transform:uppercase">PHI_ML</th>
          <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;font-size:0.62rem;letter-spacing:0.1em;color:rgba(255,255,255,0.4);text-transform:uppercase">PERM_PHY</th>
          <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;font-size:0.62rem;letter-spacing:0.1em;color:rgba(255,255,255,0.4);text-transform:uppercase">RFPI</th>
          <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;font-size:0.62rem;letter-spacing:0.1em;color:rgba(255,255,255,0.4);text-transform:uppercase">GRI</th>
          <th style="padding:10px 14px;text-align:left;font-family:'Space Mono',monospace;font-size:0.62rem;letter-spacing:0.1em;color:rgba(255,255,255,0.4);text-transform:uppercase">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.04)">
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#00d28c;font-weight:700">01</td>
          <td style="padding:12px 14px;font-weight:600">BLT-01</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace">12.65%</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace">0.002654</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#00d28c">0.043196</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#00d28c">0.8825</td>
          <td style="padding:12px 14px"><span class="tag-sel">PRODUCTION ANCHOR</span></td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.04)">
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#00b4d8;font-weight:700">02</td>
          <td style="padding:12px 14px;font-weight:600">JUT-01</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace">9.33%</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace">0.000989</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#00b4d8">0.011767</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#00b4d8">0.4296</td>
          <td style="padding:12px 14px"><span class="tag-ret">INJECTION ANCHOR</span></td>
        </tr>
        <tr style="border-bottom:1px solid rgba(255,255,255,0.04)">
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#f4a532;font-weight:700">03</td>
          <td style="padding:12px 14px;font-weight:600">EVD-01</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace">8.72%</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace">0.000795</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#f4a532">0.005399</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#f4a532">0.3261</td>
          <td style="padding:12px 14px"><span class="tag-std">MARGINAL STANDBY</span></td>
        </tr>
        <tr>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#ff4d6d;font-weight:700">04</td>
          <td style="padding:12px 14px;font-weight:600">PKP-01</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace">6.88%</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace">0.000375</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#ff4d6d">0.001882</td>
          <td style="padding:12px 14px;font-family:'Space Mono',monospace;color:#ff4d6d">-0.0045</td>
          <td style="padding:12px 14px"><span class="tag-exc">EXCLUDED — CAPEX RISK</span></td>
        </tr>
      </tbody>
    </table>
    """
    st.markdown(well_html, unsafe_allow_html=True)
    st.write("")

    col_feat, col_radar = st.columns([1, 1])

    # ── Feature importance horizontal bar ──
    with col_feat:
        st.markdown("##### AI-RQI Engine — Feature Weights")
        features = ["Flow Potential (RFPI)", "ML Matrix Porosity", "Gamma Ray Cleanliness", "Formation Thickness"]
        weights  = [0.40, 0.25, 0.20, 0.15]
        colors   = ["#00d28c", "#00b4d8", "#a78bfa", "rgba(255,255,255,0.3)"]

        fig_feat = go.Figure(go.Bar(
            x=weights, y=features,
            orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{w*100:.0f}%" for w in weights],
            textfont=dict(family="Space Mono, monospace", size=10, color="rgba(255,255,255,0.8)"),
            textposition="outside",
            hovertemplate="%{y}<br>Weight: %{x:.0%}<extra></extra>",
        ))
        fig_feat.update_layout(**GEO_LAYOUT, height=220, showlegend=False)
        fig_feat.update_xaxes(tickformat=".0%", range=[0, 0.52])
        st.plotly_chart(fig_feat, use_container_width=True, config={"displayModeBar": False})

    # ── Radar chart for top 2 wells ──
    with col_radar:
        st.markdown("##### BLT-01 vs JUT-01 — Attribute Profile")
        cats = ["Porosity", "Permeability", "RFPI", "GRI Score", "Certainty"]
        blt  = [1.00, 1.00, 1.00, 0.88, 0.60]
        jut  = [0.43, 0.37, 0.24, 0.43, 0.99]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=blt + [blt[0]], theta=cats + [cats[0]],
            fill="toself", fillcolor="rgba(0,210,140,0.12)",
            line=dict(color="#00d28c", width=2),
            name="BLT-01",
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=jut + [jut[0]], theta=cats + [cats[0]],
            fill="toself", fillcolor="rgba(0,180,216,0.10)",
            line=dict(color="#00b4d8", width=2, dash="dot"),
            name="JUT-01",
        ))
        fig_radar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            polar=dict(
                bgcolor="rgba(14,22,36,0.5)",
                radialaxis=dict(
                    visible=True, range=[0,1],
                    gridcolor="rgba(255,255,255,0.08)",
                    tickfont=dict(size=8, color="rgba(255,255,255,0.3)"),
                    tickvals=[0.25,0.5,0.75,1.0],
                ),
                angularaxis=dict(
                    gridcolor="rgba(255,255,255,0.08)",
                    tickfont=dict(size=9, family="Space Mono, monospace", color="rgba(255,255,255,0.6)"),
                ),
            ),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9, family="Space Mono, monospace", color="rgba(255,255,255,0.6)")),
            height=260,
            margin=dict(l=40, r=40, t=20, b=20),
            font=dict(family="Space Mono, monospace", color="rgba(255,255,255,0.6)"),
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════
# TAB 3 — TECHNO-ECONOMIC REPORTS
# ══════════════════════════════════════════════
with tab3:
    st.markdown("#### Strategic Scenario Comparison Matrix")

    scenario_data = {
        "Scenario": [
            "A · Geothermal Only",
            "B · Geothermal + HP",
            "C · Geo + HP + Storage",
            "D · Hybrid Solar/Waste",
        ],
        "CAPEX (€M)": [9.73, 15.73, 27.73, 30.23],
        "OPEX/yr (€k)": [894, 911, 911, 911],
        "Reliability (%)": [97.76, 100.00, 100.00, 100.00],
        "LCOE (€/MWh)": [14.96, 19.47, 28.91, 30.88],
        "Decision": ["REJECTED", "REVIEW", "OPTIMAL", "REJECTED"],
    }
    df_scenarios = pd.DataFrame(scenario_data)

    # ── Grouped bar chart ──
    fig_scen = go.Figure()
    bar_colors = ["#ff4d6d", "#f4a532", "#00d28c", "#a78bfa"]

    fig_scen.add_trace(go.Bar(
        name="Reliability (%)",
        x=df_scenarios["Scenario"],
        y=df_scenarios["Reliability (%)"],
        marker_color=[
            "rgba(255,77,109,0.73)", "rgba(244,165,50,0.73)",
            "rgba(0,210,140,0.73)",  "rgba(167,139,250,0.73)",
        ],
        marker_line=dict(color=bar_colors, width=1.5),
        yaxis="y",
        offsetgroup=1,
        hovertemplate="%{x}<br>Reliability: %{y:.2f}%<extra></extra>",
    ))
    fig_scen.add_trace(go.Scatter(
        name="LCOE (€/MWh)",
        x=df_scenarios["Scenario"],
        y=df_scenarios["LCOE (€/MWh)"],
        mode="lines+markers",
        line=dict(color="#00b4d8", width=2.5, dash="dot"),
        marker=dict(size=9, symbol="diamond", color="#00b4d8"),
        yaxis="y2",
        hovertemplate="%{x}<br>LCOE: €%{y:.2f}/MWh<extra></extra>",
    ))
    # Target line at 95%
    fig_scen.add_hline(
        y=95, line_dash="dash", line_color="rgba(255,255,255,0.2)", line_width=1,
        annotation_text="95% reliability threshold",
        annotation_font=dict(size=9, color="rgba(255,255,255,0.35)", family="Space Mono, monospace"),
    )

    fig_scen.update_layout(**GEO_LAYOUT, height=300)
    fig_scen.update_yaxes(title_text="Reliability (%)", range=[0, 115])
    fig_scen.update_layout(yaxis2=dict(
        title="LCOE (€/MWh)", overlaying="y", side="right",
        range=[10, 38], showgrid=False,
        tickfont=dict(size=9, color="#00b4d8"),
        title_font=dict(size=9, color="#00b4d8"),
    ))
    st.plotly_chart(fig_scen, use_container_width=True, config={"displayModeBar": False})

    # ── CAPEX waterfall ──
    st.markdown("#### CAPEX Decomposition — Scenario C (Active)")
    capex_labels = ["Subsurface Wells", "Surface Infrastructure", "Thermal Storage", "Heat Pump Units", "TOTAL"]
    capex_vals   = [
        subsurface_CAPEX/1e6,
        surface_CAPEX/1e6,
        storage_CAPEX/1e6,
        heat_pump_CAPEX/1e6,
        total_CAPEX/1e6,
    ]
    capex_measures = ["relative","relative","relative","relative","total"]
    capex_colors   = ["#00b4d8","#00d28c","#a78bfa","#f4a532","rgba(255,255,255,0.8)"]

    fig_wf = go.Figure(go.Waterfall(
        name="CAPEX", orientation="v",
        measure=capex_measures,
        x=capex_labels, y=capex_vals,
        text=[f"€{v:.2f}M" for v in capex_vals],
        textfont=dict(family="Space Mono, monospace", size=9),
        textposition="outside",
        connector=dict(line=dict(color="rgba(255,255,255,0.1)", width=1, dash="dot")),
        increasing=dict(marker=dict(color="#00d28c", line=dict(color="#00d28c", width=1))),
        totals=dict(marker=dict(color="rgba(0,210,140,0.25)", line=dict(color="#00d28c", width=1.5))),
        hovertemplate="%{x}<br>€%{y:.3f}M<extra></extra>",
    ))
    fig_wf.update_layout(**GEO_LAYOUT, height=280, showlegend=False)
    st.plotly_chart(fig_wf, use_container_width=True, config={"displayModeBar": False})

    st.write("---")
    st.markdown("#### 💾 Export Submission Assets")
    
    reporting_matrix = pd.DataFrame({
        "Scenario Pipeline Pathway": [
            "Scenario A: Geothermal Only Baseline",
            "Scenario B: Geothermal + Heat Pump Support",
            "Scenario C: Geothermal + HP + Thermal Storage",
            "Scenario D: Hybrid Solar/Industrial Waste Heat",
        ],
        "Capital CAPEX Outlay":    ["€9,730,080", "€15,730,080", "€27,730,080", "€30,230,080"],
        "Annual OPEX Overhead":    ["€894,297/yr", "€911,215/yr", "€911,215/yr", "€911,215/yr"],
        "Grid System Reliability": ["97.76%", "100.00%", "100.00%", "100.00%"],
        "Levelized Lifecycle LCOE":["€14.96/MWh", "€19.47/MWh", "€28.91/MWh", "€30.88/MWh"],
        "Project Status":          ["REJECTED (FAIL)", "REVIEW (BUFFER RISK)", "OPTIMIZED TARGET", "REJECTED (OVER-CAP)"],
    })
    csv_bytes = reporting_matrix.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇  Download Master Economic Report (.csv)",
        data=csv_bytes,
        file_name="GEOTWIN_DC_Master_Report.csv",
        mime="text/csv",
    )

st.write("---")
st.caption("💻 GEOTWIN-DC · Data Drillers · SPE Africa Geothermal Datathon 2026")