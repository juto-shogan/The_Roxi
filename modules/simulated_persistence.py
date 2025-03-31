import json
import time

# Load previous scan results
def load_previous_results(previous_results_file):
    try:
        with open(previous_results_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Notice: No previous results found. Starting fresh.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in {previous_results_file}. Check the file format.")
        return {}

# Save updated results
def save_updated_results(results, results_file):
    try:
        with open(results_file, "w") as file:
            json.dump(results, file, indent=4)
        print(f"Updated scan results saved to {results_file}")
    except Exception as e:
        print(f"Error: Failed to save updated results. Reason: {e}")

# Simulate a scan and compare with previous results
def simulate_scan(previous_results):
    # Mock new scan results
    new_results = {
        "192.168.1.1": ["http", "ssh"],
        "192.168.1.2": ["ftp"],
        "192.168.1.3": ["http", "smtp"],
        "192.168.1.4": ["http"]  # Example of a service update (added http)
    }

    # Compare with previous results
    changes = {}
    for host, services in new_results.items():
        if host not in previous_results:
            changes[host] = {"status": "new_host", "services": services}
        elif set(services) != set(previous_results[host]):
            changes[host] = {
                "status": "updated_services",
                "old": previous_results[host],
                "new": services
            }

    return new_results, changes

# Notify changes
def notify_changes(changes):
    if not changes:
        print("No changes detected during the scan.")
    else:
        print("Changes detected:")
        for host, details in changes.items():
            if details["status"] == "new_host":
                print(f"- New host discovered: {host} with services {details['services']}")
            elif details["status"] == "updated_services":
                print(f"- Service update on {host}: {details['old']} -> {details['new']}")

# Entry point for simulated persistence module
if __name__ == "__main__":
    previous_results_file = "logs/persistence/previous_scan_results.json"

    # Load previous results
    previous_results = load_previous_results(previous_results_file)

    # Simulate scan and check for changes
    new_results, changes = simulate_scan(previous_results)

    # Notify changes
    notify_changes(changes)

    # Save updated results
    save_updated_results(new_results, previous_results_file)
#     delivery_results = load_delivery_results(delivery_log_file)
#     rule_stats = analyze_delivery_results(delivery_results)