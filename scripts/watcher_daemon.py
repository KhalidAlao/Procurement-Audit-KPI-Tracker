import time
import shutil
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

INCOMING_DIR = "../watcher/incoming"
VERIFIED_DIR = "../watcher/verified"
PO_MASTER_PATH = "../data/raw/po_master.csv"
POE_LOG_PATH = "../data/raw/poe_log.csv"

class POEHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and (event.src_path.endswith(".csv") or event.src_path.endswith(".pdf")):
            print(f"New POE detected: {event.src_path}")
            # Simulate parsing filename to extract PO number
            filename = event.src_path.split("/")[-1]
            po_number = filename.split("_")[0]  # e.g., "PO-0123_invoice.csv"

            # Update POE log
            poe_log = pd.read_csv(POE_LOG_PATH)
            if po_number in poe_log["PO_Number"].values:
                poe_log.loc[poe_log["PO_Number"] == po_number, "Status"] = "Verified"
                poe_log.loc[poe_log["PO_Number"] == po_number, "Date_Received"] = pd.Timestamp.now()
                poe_log.to_csv(POE_LOG_PATH, index=False)
                print(f"Updated POE log for {po_number}")

            # Move file to verified folder
            shutil.move(event.src_path, f"{VERIFIED_DIR}/{filename}")
            print(f"Moved to {VERIFIED_DIR}")

if __name__ == "__main__":
    event_handler = POEHandler()
    observer = Observer()
    observer.schedule(event_handler, INCOMING_DIR, recursive=False)
    observer.start()
    print(f"Watching {INCOMING_DIR} for new POE files...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()