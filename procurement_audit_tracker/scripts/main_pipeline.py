import subprocess
import os

def run_script(script_name):
    result = subprocess.run(["python3", script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    print("=== Generating mock data ===")
    run_script("generate_mock_data.py")
    print("\n=== Running audit ===")
    run_script("audit_logic.py")
    print("\n=== Starting watcher (Ctrl+C to stop) ===")
    run_script("watcher_daemon.py")