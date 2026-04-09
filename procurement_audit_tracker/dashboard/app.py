import os
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_processed_dir = os.path.join(project_root, "data", "processed")
data_raw_dir = os.path.join(project_root, "data", "raw")

exceptions = pd.read_csv(os.path.join(data_processed_dir, "exceptions.csv"))
aging = pd.read_csv(os.path.join(data_processed_dir, "aging_report.csv"))
efficiency = pd.read_csv(os.path.join(data_processed_dir, "efficiency_check.csv"))
blocker = pd.read_csv(os.path.join(data_raw_dir, "blocker_log.csv"))
po_master = pd.read_csv(os.path.join(data_raw_dir, "po_master.csv"))

total_budget = po_master["Total_Value"].sum()
spent = po_master[po_master["Status"] == "Finished"]["Total_Value"].sum()
burn_rate = spent / total_budget if total_budget > 0 else 0
compliance = (len(po_master[po_master["Status"] == "Finished"]) / len(po_master)) * 100 if len(po_master) > 0 else 0
bottleneck_counts = blocker["Blocker_Reason"].value_counts().reset_index()
bottleneck_counts.columns = ["Blocker", "Count"]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Procurement Audit & KPI Tracker", style={"textAlign": "center"}),
    html.Div([
        html.Div([html.H3(f"Burn Rate: {burn_rate:.1%}"), html.P("Marketing budget usage")]),
        html.Div([html.H3(f"Compliance: {compliance:.1f}%"), html.P("POEs submitted on time")]),
    ], style={"display": "flex", "gap": "20px", "justifyContent": "center"}),
    dcc.Graph(figure=px.bar(bottleneck_counts, x="Blocker", y="Count", title="Top Blockers")),
    dcc.Graph(figure=px.bar(exceptions, x="Partner_Name", y="Total_Value", color="Region", title="Exceptions")),
    dcc.Graph(figure=px.histogram(aging, x="Days_Open", color="Aging_Flag", title="Aging Analysis")),
    dcc.Graph(figure=px.scatter(efficiency, x="Total_Value", y="Actual_Invoiced", trendline="ols", title="Planned vs Actual"))
])

if __name__ == "__main__":
    app.run(debug=True)