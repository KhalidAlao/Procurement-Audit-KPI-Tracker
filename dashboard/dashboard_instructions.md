# Dashboard Instructions – Procurement Audit & KPI Tracker

This dashboard visualises the health of your marketing procurement pipeline. It is built with **Dash + Plotly** but can be easily recreated in **Power BI** or **Tableau** using the exported CSV files.

## Running the Python Dashboard

1. Make sure all dependencies are installed:  
   `pip install -r requirements.txt`

2. From the project root, run:  
   `python dashboard/app.py`

3. Open your browser to `http://127.0.0.1:8050`

## Understanding the KPIs

| KPI | What it measures | Why it matters |
|-----|----------------|----------------|
| **Burn Rate** | % of total marketing budget already spent (finished POs) | Tells you how fast the budget is being used – early warning for overspend. |
| **Compliance %** | % of finished POs that have a verified Proof‑of‑Execution (POE) uploaded | Measures partner discipline & internal process adherence. Low compliance = risk of unsubstantiated spend. |
| **Top Blockers** | Most frequent reasons delaying payment (e.g., Missing Invoice) | Directly shows where to intervene operationally. |
| **Exceptions** | POs that are 100% spent but have **0% POE** uploaded | Red flags for potential audit failures or missing documentation. |
| **Aging Analysis** | How many days POs remain open without any activity | Highlights stale POs that need chasing. |
| **Planned vs Actual** | Difference between budgeted amount and actual invoiced | Detects scope changes, amendments, or invoicing errors. |