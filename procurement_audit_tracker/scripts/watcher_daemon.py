import os
import time
import shutil
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
incoming_dir = os.path.join(project_root, "watcher", "incoming")
verified_dir = os.path.join(project_root, "watcher", "verified")
poe_log_path = os.path.join(project_root, "data", "raw", "poe_log.csv")

os.makedirs(incoming_dir, exist_ok=True)
os.makedirs(verified_dir, exist_ok=True)

class POEHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and (event.src_path.endswith(".csv") or event.src_path.endswith(".pdf")):
            print(f"New POE detected: {event.src_path}")
            filename = os.path.basename(event.src_path)
            po_number = filename.split("_")[0]
            if os.path.exists(poe_log_path):
                poe_log = pd.read_csv(poe_log_path)
                if po_number in poe_log["PO_Number"].values:
                    poe_log.loc[poe_log["PO_Number"] == po_number, "Status"] = "Verified"
                    poe_log.loc[poe_log["PO_Number"] == po_number, "Date_Received"] = pd.Timestamp.now()
                    poe_log.to_csv(poe_log_path, index=False)
                    print(f"Updated POE log for {po_number}")
                else:
                    print(f"PO number {po_number} not found")
            shutil.move(event.src_path, os.path.join(verified_dir, filename))
            print(f"Moved to {verified_dir}")

if __name__ == "__main__":
    event_handler = POEHandler()
    observer = Observer()
    observer.schedule(event_handler, incoming_dir, recursive=False)
    observer.start()
    print(f"Watching {incoming_dir}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()