import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load data from processed files
exceptions = pd.read_csv("../data/processed/exceptions.csv")
aging = pd.read_csv("../data/processed/aging_report.csv")
efficiency = pd.read_csv("../data/processed/efficiency_check.csv")
blocker = pd.read_csv("../data/raw/blocker_log.csv")
po_master = pd.read_csv("../data/raw/po_master.csv")

# Precompute KPIs
total_budget = po_master["Total_Value"].sum()
spent = po_master[po_master["Status"] == "Finished"]["Total_Value"].sum()
burn_rate = spent / total_budget  # simplified
compliance = (len(po_master[po_master["Status"] == "Finished"]) / len(po_master)) * 100
bottleneck_counts = blocker["Blocker_Reason"].value_counts().reset_index()
bottleneck_counts.columns = ["Blocker", "Count"]

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Procurement Audit & KPI Tracker", style={"textAlign": "center"}),
    html.Div([
        html.Div([html.H3(f"Burn Rate: {burn_rate:.1%}"), html.P("Marketing budget usage")], className="card"),
        html.Div([html.H3(f"Compliance: {compliance:.1f}%"), html.P("POEs submitted on time")], className="card"),
    ], style={"display": "flex", "gap": "20px", "justifyContent": "center", "marginBottom": "30px"}),
    dcc.Graph(
        id="bottleneck-chart",
        figure=px.bar(bottleneck_counts, x="Blocker", y="Count", title="Top Blockers (Days between finished & paid)")
    ),
    dcc.Graph(
        id="exceptions-map",
        figure=px.bar(exceptions, x="Partner_Name", y="Total_Value", color="Region",
                      title="Exceptions: Spent but No POE Uploaded")
    ),
    dcc.Graph(
        id="aging-gauge",
        figure=px.histogram(aging, x="Days_Open", color="Aging_Flag", title="Aging Analysis: Open POs")
    ),
    dcc.Graph(
        id="efficiency-scatter",
        figure=px.scatter(efficiency, x="Total_Value", y="Actual_Invoiced", trendline="ols",
                          title="Planned vs Actual Invoiced (Discrepancy)")
    )
], style={"fontFamily": "Arial", "padding": "20px"})

if __name__ == "__main__":
    app.run(debug=True)