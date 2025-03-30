import json
import os
from datetime import datetime

# Function to ensure the decision logs folder exists
def ensure_logs_folder_exists():
    folder_name = "logs/engineData"
    # Check if the folder exists, if not, create it
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
# Function to process scan results and make port-specific decisions
def make_decisions(scan_results):
    decisions = []
    for result in scan_results:
        host = result["host"]
        port = result["port"]
        status = result["status"]
        service = result["service"]  # Service type detected

        # Decision logic based on ports and services
        if status == "open":
            if port == 80:  # HTTP
                decisions.append({
                    "host": host,
                    "port": port,
                    "service": "http",
                    "action": "probe_http",
                    "reason": f"HTTP detected on port {port}. Potential for web-based vulnerability testing."
                })
            elif port == 22:  # SSH
                decisions.append({
                    "host": host,
                    "port": port,
                    "service": "ssh",
                    "action": "check_ssh_security",
                    "reason": f"SSH detected on port {port}. Consider checking authentication methods."
                })
            elif port == 443:  # HTTPS
                decisions.append({
                    "host": host,
                    "port": port,
                    "service": "https",
                    "action": "probe_https",
                    "reason": f"Secure HTTPS service detected on port {port}. Verify SSL/TLS configurations."
                })
            elif port == 21:  # FTP
                decisions.append({
                    "host": host,
                    "port": port,
                    "service": "ftp",
                    "action": "probe_ftp",
                    "reason": f"FTP detected on port {port}. Investigate file transfer vulnerabilities."
                })
            elif port == 25:  # SMTP
                decisions.append({
                    "host": host,
                    "port": port,
                    "service": "smtp",
                    "action": "probe_smtp",
                    "reason": f"SMTP detected on port {port}. Evaluate mail server security."
                })
            else:
                decisions.append({
                    "host": host,
                    "port": port,
                    "service": "unknown",
                    "action": "log_unknown_port",
                    "reason": f"Open port {port} detected with service '{service}'. Requires further analysis."
                })
    return decisions

def prioritize_decisions(decisions):
    prioritized_decisions = []
    for decision in decisions:
        service = decision["service"]
        priority = 5  # Default priority for unknown or generic services

        # Assign priorities based on service type
        if service == "http":
            priority = 10
        elif service == "ssh":
            priority = 9
        elif service == "https":
            priority = 8
        elif service == "ftp":
            priority = 6
        elif service == "smtp":
            priority = 7

        # Add the priority to the decision
        decision["priority"] = priority
        prioritized_decisions.append(decision)

    # Sort decisions by priority (highest first)
    return sorted(prioritized_decisions, key=lambda d: d["priority"], reverse=True)


# Main execution block
if __name__ == "__main__":
    # Load the scanner results from a JSON file
    scan_results_file = "logs/scanData/scan_results.json"  # Update the path as needed

    try:
        with open(scan_results_file, "r") as file:
            scan_results = json.load(file)[-1]["data"]  # Load the latest scan results
    except (FileNotFoundError, IndexError, KeyError):
        print("No scan results found. Please run the scanner first.")
        scan_results = []

    # Step 1: Generate basic decisions
    decisions = make_decisions(scan_results)

    # Step 2: Prioritize decisions
    if decisions:
        prioritized_decisions = prioritize_decisions(decisions)

        # Step 3: Save the prioritized decisions to a JSON log
        log_decisions_to_json(prioritized_decisions, "decision_log.json")
        print("Prioritized decisions saved to logs/engineData/decision_log.json")
    else:
        print("No open ports found. No decisions were made.")
