# 🌍 GEOTWIN-DC — Integrated Geothermal Digital Twin
### SPE Africa Geothermal Datathon 2026 · Team: Data Drillers

> **An AI-assisted geothermal reservoir assessment and district heating & cooling optimisation framework for the Utrecht neighbourhood energy system.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://geotwin-dc.streamlit.app/)

🚀 **Live Dashboard:** [geotwin-dc.streamlit.app](https://geotwin-dc.streamlit.app/)

---

## Overview

GEOTWIN-DC (Geothermal Twin — District Cooling) is a full-stack geothermal engineering workflow that combines subsurface reservoir analysis, machine learning, physics-informed modelling, economic evaluation, and Bayesian optimisation into a single integrated pipeline.

The system assesses the geothermal potential of four wells in the Utrecht area, confirms the resource can sustainably meet district heating and cooling demand, and recommends the optimal hybrid energy system configuration — all surfaced through a live Streamlit digital twin dashboard.

---

## Repository Structure

```
dseats_2026/
│
├── stage_1_2_documented.ipynb     # Stage 1 & 2: Subsurface assessment + surface design
├── AI_documented.ipynb            # Stages 3–8: ML pipeline + Bayesian optimisation
├── app.py                         # Streamlit digital twin dashboard
├── requirements.txt               # Python dependencies
│
├── stage1_stage2_results.xlsx     # Intermediate output: petrophysical results (Stage 1→2)
├── final_geotwin_results.xlsx     # Final output: AI-ranked well results (Stage 8 export)
├── LCoE.xlsx                      # TNO/ECN LCoE template — all 4 scenario runs completed
│
└── data_AGD_2026/data/            # Raw input data
    ├── raw/                       # LAS well-log files (BLT-01, JUT-01, EVD-01, PKP-01)
    ├── Lithostratigraphic Data.xlsx
    ├── ThermoGIS Data.xlsx
    ├── Well Path Data.xlsx
    └── target_lithologies.csv
```

---

## Pipeline Architecture

```
Raw LAS + Excel Data
        │
        ▼
┌─────────────────────────────────────────────────┐
│  stage_1_2_documented.ipynb                     │
│                                                 │
│  Stage 1 · LAS ingestion & log standardisation  │
│  Stage 2 · Reservoir interval extraction        │
│  Stage 3 · Petrophysical analysis (PHI, NTG)   │
│  Stage 4 · Reservoir Quality Index (RQI)        │
│  Stage 5 · Surface system design & sizing       │
│  Stage 6 · Seasonal operational strategy        │
│  Stage 7 · Risk & sustainability assessment     │
└────────────────┬────────────────────────────────┘
                 │  stage1_stage2_results.xlsx
                 ▼
┌─────────────────────────────────────────────────┐
│  AI_documented.ipynb                            │
│                                                 │
│  Stage 1 · Dataset integration & cleaning       │
│  Stage 2 · ML porosity reconstruction (RF)     │
│  Stage 3 · Physics-informed permeability        │
│  Stage 4 · Reservoir Flow Potential Index       │
│  Stage 5 · AI-RQI v3 composite ranking         │
│  Stage 6 · Uncertainty quantification          │
│  Stage 7 · Final geothermal ranking index      │
│  Stage 7B· Thermal sustainability check        │
│  Stage 7C· Temperature–depth profile           │
│  Stage 8 · Bayesian optimisation (Optuna TPE)  │
│  Stage 9 · Scenario analysis & LCoE (A–D)     │
└────────────────┬────────────────────────────────┘
                 │  final_geotwin_results.xlsx
                 ▼
        ┌────────────────┐
        │    app.py      │
        │  Streamlit     │
        │  Dashboard     │
        └────────────────┘
```

---

## Key Results

### Well Ranking (AI-RQI v3)

| Rank | Well | PHI_ML | RFPI | Final Index | Decision |
|------|------|--------|------|-------------|----------|
| 1 | **BLT-01** | 12.65% | 0.04320 | 0.8825 | ✅ Production Anchor |
| 2 | **JUT-01** | 9.33% | 0.01177 | 0.4296 | ✅ Injection Anchor |
| 3 | EVD-01 | 8.72% | 0.00540 | 0.3261 | ⚠️ Marginal Standby |
| 4 | PKP-01 | 6.88% | 0.00188 | −0.0045 | ❌ Excluded — CAPEX Risk |

### Thermal Sustainability
- **Geothermal supply:** 17.71 MWth at 70 L/s (satisfies ≥10 MWth heating + ≥5 MWth cooling)
- **Thermal breakthrough:** 29.8 years (14.8-year margin beyond the 15-year project life)
- **Geothermal gradient:** 42.0 °C/km | Reservoir interval: 1,924–2,053 m TVD

### Scenario Comparison

| Scenario | CAPEX | Reliability | LCoE | Decision |
|----------|-------|-------------|------|----------|
| A — Geothermal Only | €9.73M | 97.76% | €14.96/MWh | Rejected — no cooling |
| B — Geo + Heat Pump | €15.73M | 100.00% | €19.47/MWh | Review |
| **C — Geo + HP + Storage** | **€27.73M** | **100.00%** | **€28.91/MWh** | ✅ **Optimal** |
| D — Geo + HP + Storage + Solar | €30.23M | 100.00% | €30.88/MWh | Rejected — over-capitalised |

### Bayesian Optimisation Result
```
Optimal Flow Rate:   63.77 L/s
Thermal Power:       16.13 MWth  (incl. 0.93 system efficiency)
Heat Pump COP:       5.0
Thermal Storage:     2 hours
Status:              SAFE OPERATION ZONE
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Ukpoweh/dseats_2026.git
cd dseats_2026
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the notebooks in order
Open and run `stage_1_2_documented.ipynb` first — it generates `stage1_stage2_results.xlsx` which is required by `AI_documented.ipynb`.

```
stage_1_2_documented.ipynb  →  stage1_stage2_results.xlsx
AI_documented.ipynb         →  final_geotwin_results.xlsx
```

### 4. Launch the dashboard
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`. Use the sidebar sliders to adjust flow rate, demand, storage capacity, and heat pump boost in real time.

---

## Dependencies

```
streamlit>=1.35.0
numpy>=1.26.0
pandas>=2.2.0
matplotlib>=3.8.0
plotly>=5.22.0
scikit-learn>=1.4.0
xgboost>=2.0.0
optuna>=3.5.0
lasio>=0.31
openpyxl>=3.1.0
```

Full list in `requirements.txt`.

---

## Methodology

### Subsurface Assessment (Challenge 1)
- **LAS log processing:** GR, RHOB, DT, NPHI curves standardised across 4 wells
- **Petrophysics:** Density porosity (Archie/bulk-density crossplot), net sand (GR cutoff 75 API), NTG
- **ML Porosity Reconstruction:** Random Forest (300 trees) trained on wireline features — fills missing data while quantifying model uncertainty
- **Physics-informed permeability:** Kozeny–Carman dimensionless proxy ($k_{phy} = \phi^3 / (1-\phi)^2$)
- **AI-RQI v3:** Weighted composite — 40% RFPI + 25% porosity + 20% GR cleanliness + 15% thickness
- **Thermal sustainability:** 1-D retardation model confirms 29.8-year thermal breakthrough (R=5.39)

### Surface System Design (Challenge 2)
- **District energy architecture:** Geothermal doublet → heat exchanger → HP → TES → district loop
- **Scenario simulation:** 180 monthly timesteps, dispatch-priority logic (geo → HP → storage → shortage)
- **LCoE:** Discounted cash-flow model (WACC 6.6%, 15-year horizon, scheduled workovers)
- **Sensitivity analysis:** Tornado chart — ±20% parametric sweep on 5 key variables

### LCoE Economic Template (Challenge 3)
- **File:** `LCoE.xlsx` — TNO/ECN standard discounted cash-flow model
- **All four scenarios pre-run:** Scenario A–D results filled in with values from the Python simulation
- **Hybrid system inputs** added in rows 75–103 of `Input_Output` sheet: heat pump CAPEX, thermal storage capacity, solar/waste heat CAPEX, flow rate, COP, demand
- **GeoTwin-DC Scenarios** sheet provides side-by-side comparison matrix linked to all inputs
- **Sensitivity sheet** contains tornado chart data (±20% on 5 key variables)

### AI-Assisted Optimisation (Bonus)
- **Framework:** Optuna TPE sampler, 100 trials, `seed=42`
- **Constraints:** Hard geological flow ceiling (70 L/s), thermal power window (16–22 MWth)
- **Variables:** Flow rate (50–70 L/s), COP (3.5–5.0), storage duration (2–6 hrs)

---

## Dashboard Features

The Streamlit dashboard (`app.py`) provides a live digital twin interface:

- **Real-time simulation** — sliders update the full 15-year simulation on every interaction
- **KPI cards** — Grid reliability, LCOE, total CAPEX, lifetime CO₂ offset
- **Tab 1 — Dynamic Performance:** Demand vs supply time series, annual energy production, shortage analysis
- **Tab 2 — Subsurface Analytics:** AI-RQI v3 well ranking table, feature weight chart, BLT-01 vs JUT-01 radar
- **Tab 3 — Techno-Economic Reports:** Scenario comparison chart, CAPEX waterfall, CSV export

---

## Team

**Data Drillers** — SPE Africa Geothermal Datathon 2026

| | |
|---|---|
| 🏆 **Team Name** | Data Drillers |
| 📦 **Repository** | [github.com/Ukpoweh/dseats_2026](https://github.com/Ukpoweh/dseats_2026) |
| 🚀 **Live App** | [geotwin-dc.streamlit.app](https://geotwin-dc.streamlit.app/) |
| 🎯 **Competition** | SPE Africa Geothermal Datathon 2026 |

---

