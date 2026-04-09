import pandas as pd
import numpy as np

def run_audit(po_path="../data/raw/po_master.csv",
              poe_path="../data/raw/poe_log.csv",
              blocker_path="../data/raw/blocker_log.csv"):

    po = pd.read_csv(po_path, parse_dates=["Creation_Date"])
    poe = pd.read_csv(poe_path, parse_dates=["Date_Received"])
    blocker = pd.read_csv(blocker_path, parse_dates=["Finished_Date", "Paid_Date"])

    # Exceptions: 100% spent but 0% POE uploaded
    # Assume "spent" = finished status. For demo, we treat "Finished" as fully spent.
    finished_pos = po[po["Status"] == "Finished"]["PO_Number"]
    poe_submitted = poe[poe["Status"] != "Missing"]["PO_Number"]
    exceptions = set(finished_pos) - set(poe_submitted)
    df_exceptions = po[po["PO_Number"].isin(exceptions)].copy()
    df_exceptions["Exception_Reason"] = "100% spent, 0% POE uploaded"

    # Aging: days open without activity (Status = Open and no POE)
    open_pos = po[po["Status"] == "Open"]["PO_Number"]
    aging = []
    for po_num in open_pos:
        creation = po.loc[po["PO_Number"] == po_num, "Creation_Date"].iloc[0]
        days_open = (pd.Timestamp.now() - creation).days
        poe_entry = poe[poe["PO_Number"] == po_num]
        has_activity = not poe_entry["Date_Received"].isna().all()
        aging.append({
            "PO_Number": po_num,
            "Days_Open": days_open,
            "Has_Activity": has_activity,
            "Aging_Flag": "Stale" if (days_open > 30 and not has_activity) else "Active"
        })
    df_aging = pd.DataFrame(aging)

    # Efficiency: Planned vs Actual Invoiced
    # We simulate actual invoiced as Total_Value +/- random discrepancy
    np.random.seed(42)
    po["Actual_Invoiced"] = po["Total_Value"] * np.random.uniform(0.8, 1.2, len(po))
    po["Discrepancy"] = po["Actual_Invoiced"] - po["Total_Value"]
    po["Discrepancy_Pct"] = (po["Discrepancy"] / po["Total_Value"]) * 100

    # Save audit outputs
    df_exceptions.to_csv("../data/processed/exceptions.csv", index=False)
    df_aging.to_csv("../data/processed/aging_report.csv", index=False)
    po[["PO_Number", "Total_Value", "Actual_Invoiced", "Discrepancy", "Discrepancy_Pct"]].to_csv("../data/processed/efficiency_check.csv", index=False)

    print("Audit complete. Outputs saved to /data/processed/")
    return df_exceptions, df_aging, po

if __name__ == "__main__":
    run_audit()