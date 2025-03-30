import json
import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from datetime import datetime
from modules.rules_engine import load_rules, process_rules

# This module is responsible for making decisions based on scan results and logging them.
# Function to ensure the decision logs folder exists
def ensure_logs_folder_exists():
    folder_name = "logs/engineData"
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

# Ensure the directory for the file exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Log decisions to a JSON file
def log_decisions_to_json(decisions, filename):
    # Ensure directory exists before writing
    directory = os.path.dirname(filename)
    ensure_directory_exists(directory)

    # Write decisions to the file
    with open(filename, "w") as file:
        json.dump(decisions, file, indent=4)

# Process decisions with rules
def refine_decisions_with_rules(decisions, rules_file):
    rules = load_rules(rules_file)
    for decision in decisions:
        decision = process_rules(rules, decision)
    return decisions

# Main function for decision refinement
def refine_decisions(decisions_file, rules_file):
    try:
        with open(decisions_file, "r") as file:
            decisions = json.load(file)

        refined_decisions = refine_decisions_with_rules(decisions, rules_file)

        # Save refined decisions to file
        with open("logs/engineData/refined_decision_log.json", "w") as file:
            json.dump(refined_decisions, file, indent=4)

        print("Decisions refined and saved to logs/engineData/refined_decision_log.json")

    except FileNotFoundError:
        print(f"Decisions file {decisions_file} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {decisions_file}.")
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
    # Define paths for scan results and rules
    scan_results_file = "logs/scanData/scan_results.json"
    rules_file = "rules.json"

    try:
        # Load the latest scan results
        with open(scan_results_file, "r") as file:
            scan_results = json.load(file)[-1]["data"]
    except FileNotFoundError:
        print(f"File not found: {scan_results_file}. Please run the scanner first.")
        scan_results = []
    except (IndexError, KeyError, json.JSONDecodeError):
        print("Error reading scan results. Please check the scanner output format.")
        scan_results = []

    # Step 1: Generate basic decisions based on scan results
    decisions = make_decisions(scan_results)

    # Step 2: Apply rules to prioritize decisions
    if decisions:
        # Load rules and apply them to the decisions
        rules = load_rules(rules_file)
        prioritized_decisions = []
        for decision in decisions:
            decision = process_rules(rules, decision)  # Apply rules
            prioritized_decisions.append(decision)

        # Step 3: Save the prioritized decisions to a JSON log file
        log_decisions_to_json(prioritized_decisions, "logs/engineData/decision_log.json")
        print("Prioritized decisions saved to logs/engineData/decision_log.json")
    else:
        print("No open ports found in the scan results. No decisions were made.")