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

# Function to process scan results and make port-specific decisions
def make_decisions(scan_results):
    decisions = []
    for result in scan_results:
        host = result["host"]
        port = result["port"]
        status = result["status"]
        service = result["service"]
        
        # Decision logic based on ports
        if status == "open":
            if port == 80:  # HTTP
                decisions.append({
                    "host": host,
                    "port": port,
                    "action": "probe_http",
                    "reason": f"HTTP detected on port {port}. Potential for web-based vulnerability testing."
                })
            elif port == 22:  # SSH
                decisions.append({
                    "host": host,
                    "port": port,
                    "action": "check_ssh_security",
                    "reason": f"SSH detected on port {port}. Consider checking authentication methods."
                })
            elif port == 443:  # HTTPS
                decisions.append({
                    "host": host,
                    "port": port,
                    "action": "probe_https",
                    "reason": f"Secure HTTPS service detected on port {port}. Verify SSL/TLS configurations."
                })
            elif port == 21:  # FTP
                decisions.append({
                    "host": host,
                    "port": port,
                    "action": "probe_ftp",
                    "reason": f"FTP detected on port {port}. Investigate file transfer vulnerabilities."
                })
            elif port == 25:  # SMTP
                decisions.append({
                    "host": host,
                    "port": port,
                    "action": "probe_smtp",
                    "reason": f"SMTP detected on port {port}. Evaluate mail server security."
                })
            else:
                decisions.append({
                    "host": host,
                    "port": port,
                    "action": "log_unknown_port",
                    "reason": f"Open port {port} detected with service '{service}'. Requires further analysis."
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
