import subprocess
import os

def run_script(script_name):
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error in {script_name}: {result.stderr}")

if __name__ == "__main__":
    os.chdir("scripts")  # ensure relative paths work
    print("=== Generating mock data ===")
    run_script("generate_mock_data.py")
    print("\n=== Running audit logic ===")
    run_script("audit_logic.py")
    print("\n=== Starting file watcher (daemon) ===")
    run_script("watcher_daemon.py")  # must be stopped manually 