import json
import os
from datetime import datetime

# Function to ensure the decision logs folder exists
def ensure_logs_folder_exists():
    folder_name = "decisionLogs"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

# Function to log decisions to a JSON file
def log_decisions_to_json(decisions, filename):
    filepath = os.path.join(ensure_logs_folder_exists(), filename)
    
    # If the file doesn't exist, create it
    if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            json.dump([], file)
    
    # Read existing data and append new decisions
    with open(filepath, "r") as file:
        existing_data = json.load(file)
    
    # Add a timestamp to the decisions
    decisions_with_timestamp = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "decisions": decisions
    }
    existing_data.append(decisions_with_timestamp)
    
    # Write updated data back to the file
    with open(filepath, "w") as file:
        json.dump(existing_data, file, indent=4)

# Function to process scan results and log open ports
def make_decisions(scan_results):
    decisions = []
    for result in scan_results:
        host = result["host"]
        port = result["port"]
        status = result["status"]
        
        # Log only open ports
        if status == "open":
            decisions.append({
                "host": host,
                "port": port,
                "action": "log_open_port",
                "reason": f"Port {port} is open"
            })
    return decisions

# Main execution block
if __name__ == "__main__":
    # Load the scanner results from a JSON file
    scan_results_file = "dataGathered/scan_results.json"
    
    try:
        with open(scan_results_file, "r") as file:
            scan_results = json.load(file)[-1]["data"]  # Load the latest scan results
    except (FileNotFoundError, IndexError, KeyError):
        print("No scan results found. Please run the scanner first.")
        scan_results = []

    # Make decisions based on the scan results
    decisions = make_decisions(scan_results)
    
    # Save the decisions to a JSON log
    if decisions:
        log_decisions_to_json(decisions, "decision_log.json")
        print("Decisions made and saved to decisionLogs/decision_log.json")
    else:
        print("No open ports found. No decisions were made.")
