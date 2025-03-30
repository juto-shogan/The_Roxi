import json
import os

# Ensure the log folder exists
def ensure_logs_folder():
    folder = "logs"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

# Load decisions from the decision log
def load_decisions(decision_log):
    try:
        with open(decision_log, "r") as file:
            return json.load(file)[-1]["decisions"]  # Extract the latest decisions
    except FileNotFoundError:
        print(f"Decision log file not found: {decision_log}")
        return []
    except IndexError:
        print(f"No valid decisions found in the decision log.")
        return []

# Mock CVE data (temporary until the database is functional)
mock_cve_database = {
    "http": [{"cve_id": "CVE-2023-12345", "description": "HTTP vulnerability"}],
    "ssh": [{"cve_id": "CVE-2019-14899", "description": "SSH session hijacking"}],
    "ftp": [{"cve_id": "CVE-2020-67890", "description": "FTP buffer overflow"}],
    "smtp": [{"cve_id": "CVE-2022-55555", "description": "SMTP relay vulnerability"}],
}

# Generate weaponization tasks
def generate_tasks(decisions):
    tasks = []
    for decision in decisions:
        service = decision["service"]
        host = decision["host"]
        port = decision["port"]

        # Match decisions to mock CVE data
        exploits = mock_cve_database.get(service, [{"cve_id": "N/A", "description": "No CVEs available"}])
        for exploit in exploits:
            tasks.append({
                "host": host,
                "port": port,
                "service": service,
                "cve_id": exploit["cve_id"],
                "description": exploit["description"],
                "prepared_payload": f"Payload for {exploit['cve_id']} targeting {service}"
            })
    return tasks

# Save tasks to the specified JSON file
def save_tasks(tasks, output_file):
    with open(output_file, "w") as file:
        json.dump(tasks, file, indent=4)
    print(f"Weaponization tasks saved to {output_file}")

# Main execution
if __name__ == "__main__":
    decision_file = "C:/Users/somto/OneDrive/Desktop/The_Roxi/logs/engineData/decision_log.json"  # Decision log input
    output_file = "C:/Users/somto/OneDrive/Desktop/The_Roxi/logs/weaponized_data/weaponization_tasks.json"  # Updated file path for weaponization tasks

    # Load decisions
    decisions = load_decisions(decision_file)

    # Generate tasks
    if decisions:
        weaponization_tasks = generate_tasks(decisions)
        save_tasks(weaponization_tasks, output_file)
    else:
        print("No decisions available for weaponization.")
