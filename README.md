# Automated Procurement Audit & KPI Tracker

**Simulates a real‑world “data supply chain” for Purchase Orders (POs) and Proof‑of‑Execution (POE) documents – built for the Ipsos Data Labs role.**

This project automates the lifecycle of marketing POs from creation to payment, identifies operational blockers, and delivers a live dashboard for stakeholders. It mirrors the EMEA partner ecosystem and demonstrates skills in data operations, business intelligence, and client‑facing automation.

## Key Features

- **Data Modeling** – SQLite + CSV mock data with three linked tables (PO Master, POE Storage, Blocker Log).
- **Audit Logic (Python/Pandas)** – Flags exceptions (100% spent, 0% POE), aging analysis, planned vs actual spend.
- **File‑Watching Automation** – Uses `watchdog` to monitor a folder (simulating an email alias); auto‑updates tracker when a POE file arrives.
- **Interactive Dashboard** – Built with Dash + Plotly; shows burn rate, compliance %, bottleneck tracker, and regional exceptions.
- **End‑to‑End Pipeline** – One script generates data, runs audit, and starts the watcher.

## Tech Stack

- Python (Pandas, SQLAlchemy, Watchdog, Dash, Plotly)
- SQLite / CSV
- Power BI / Tableau ready (exported CSVs)

## Project Structure
procurement_audit_tracker/

├── data/ # raw, processed, verified folders

├── watcher/ # incoming & verified (POE drops)

├── scripts/ # mock data, audit logic, watcher daemon, main pipeline

├── dashboard/ # Dash app

└── requirements.txt

## Quick Start

```bash
git clone https://github.com/KhalidAlao/Procurement-Audit-KPI-Tracker
cd procurement-audit-kpi-tracker
python3 setup_project.py          # creates folders & installs deps
cd procurement_audit_tracker
python scripts/main_pipeline.py  # generates data, runs audit, starts watcher
# In another terminal:
python dashboard/app.py          # open http://127.0.0.1:8050
