import os
import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

# Get the project root (procurement_audit_tracker folder)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_raw_dir = os.path.join(project_root, "data", "raw")
os.makedirs(data_raw_dir, exist_ok=True)

DB_PATH = os.path.join(data_raw_dir, "procurement.db")

# PO Master Data 
po_data = []
partners = ["Partner A", "Partner B", "Partner C", "Partner D"]
regions = ["EMEA-North", "EMEA-South", "EMEA-Central"]
statuses = ["Open", "Finished", "In Audit"]
for i in range(1, 101):
    po_data.append({
        "PO_Number": f"PO-{i:04d}",
        "Partner_Name": random.choice(partners),
        "Region": random.choice(regions),
        "Total_Value": round(random.uniform(5000, 500000), 2),
        "Creation_Date": datetime.now() - timedelta(days=random.randint(0, 90)),
        "Status": random.choices(statuses, weights=[0.4, 0.4, 0.2])[0]
    })
df_po = pd.DataFrame(po_data)

# POE Storage Log 
poe_data = []
for _, row in df_po.iterrows():
    if row["Status"] in ["Finished", "In Audit"]:
        received = row["Creation_Date"] + timedelta(days=random.randint(10, 60))
        poe_data.append({
            "PO_Number": row["PO_Number"],
            "Date_Received": received,
            "Document_Type": random.choice(["Invoice", "Proof_of_Execution"]),
            "Status": random.choices(["Verified", "Rejected"], weights=[0.7, 0.3])[0]
        })
    else:
        poe_data.append({
            "PO_Number": row["PO_Number"],
            "Date_Received": None,
            "Document_Type": None,
            "Status": "Missing"
        })
df_poe = pd.DataFrame(poe_data)

# Blocker Log 
blocker_data = []
finished_pos = df_po[df_po["Status"] == "Finished"]
for _, row in finished_pos.iterrows():
    finished_date = row["Creation_Date"] + timedelta(days=random.randint(30, 70))
    paid_date = finished_date + timedelta(days=random.randint(5, 30))
    blocker_data.append({
        "PO_Number": row["PO_Number"],
        "Finished_Date": finished_date,
        "Paid_Date": paid_date,
        "Blocker_Days": (paid_date - finished_date).days,
        "Blocker_Reason": random.choice(["Missing Invoice", "Internal Approval", "POE Rejected"])
    })
df_blocker = pd.DataFrame(blocker_data)

# Save
conn = sqlite3.connect(DB_PATH)
df_po.to_sql("po_master", conn, if_exists="replace", index=False)
df_poe.to_sql("poe_storage", conn, if_exists="replace", index=False)
df_blocker.to_sql("blocker_log", conn, if_exists="replace", index=False)
conn.close()

df_po.to_csv(os.path.join(data_raw_dir, "po_master.csv"), index=False)
df_poe.to_csv(os.path.join(data_raw_dir, "poe_log.csv"), index=False)
df_blocker.to_csv(os.path.join(data_raw_dir, "blocker_log.csv"), index=False)

print(f"Mock data generated in {data_raw_dir}")