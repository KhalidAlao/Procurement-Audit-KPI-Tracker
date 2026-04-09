import os
import subprocess
import sys

PROJECT_NAME = "procurement_audit_tracker"
FOLDERS = [
    "data/raw",
    "data/processed",
    "data/verified",
    "scripts",
    "dashboard",
    "watcher/incoming",
    "watcher/verified"
]
FILES = {
    "scripts/generate_mock_data.py": "",
    "scripts/audit_logic.py": "",
    "scripts/watcher_daemon.py": "",
    "scripts/main_pipeline.py": "",
    "dashboard/dashboard_instructions.md": "",
    "requirements.txt": "pandas\nsqlalchemy\nwatchdog\nopenpyxl\nplotly\ndash\n",
}

def create_project():
    # Create folders
    for folder in FOLDERS:
        os.makedirs(f"{PROJECT_NAME}/{folder}", exist_ok=True)
    # Create files
    for filepath, content in FILES.items():
        full_path = f"{PROJECT_NAME}/{filepath}"
        with open(full_path, "w") as f:
            f.write(content)
    # Install dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", f"{PROJECT_NAME}/requirements.txt"])
    print(f"Project '{PROJECT_NAME}' created. Navigate into it and continue.")

if __name__ == "__main__":
    create_project()