import json

# Function to load CVE data for weaponization (mock integration)
def load_cve_data(filepath):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"CVE data file not found at {filepath}")
        return []

# Function to generate weaponization tasks
def generate_tasks_from_decisions(decisions, cve_data):
    tasks = []
    for decision in decisions:
        service = decision.get("reason", "").split(":")[1].strip() if "reason" in decision else "Generic"
        host = decision["host"]
        port = decision["port"]

        # Match CVEs to detected services (mock logic)
        relevant_cves = [cve for cve in cve_data if service.lower() in cve["description"].lower()]
        for cve in relevant_cves:
            tasks.append({
                "host": host,
                "port": port,
                "service": service,
                "cve_id": cve["cve_id"],
                "description": cve["description"],
                "prepared_payload": f"Payload for {cve['cve_id']} targeting {service}"
            })
    return tasks

# Main function for weaponization
def weaponize(decision_file, cve_file):
    # Load decisions
    with open(decision_file, "r") as file:
        decisions = json.load(file)[-1]["decisions"]  # Use latest decisions

    # Load CVE data
    cve_data = load_cve_data(cve_file)

    # Generate tasks
    tasks = generate_tasks_from_decisions(decisions, cve_data)

    # Save weaponization tasks
    with open("weaponization_tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)
    print("Weaponization tasks saved to weaponization_tasks.json")

if __name__ == "__main__":
    decision_file = "../logs/decisionLogs/decision_log.json"  # Update path if needed
    cve_file = "../data/cve_data.json"  # Update path if needed
    weaponize(decision_file, cve_file)
