import json
import os
import sqlite3

# Ensure the log folder exists
def ensure_logs_folder():
    folder = "logs"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

# Load decisions from the JSON file
def load_decisions(decision_file):
    try:
        with open(decision_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {decision_file}. Please run the decision engine first.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {decision_file}. Check the file format.")
        return []

# Generate mock payloads based on detected services
def generate_payload(service, host, port):
    payloads = {
        "http": {
            "id": "http_payload_001",
            "action": "send GET request",
            "data": {
                "url": f"http://{host}:{port}",
                "headers": {
                    "User-Agent": "Roxi-Bot"
                }
            }
        },
        "ftp": {
            "id": "ftp_payload_001",
            "action": "open connection",
            "data": {
                "host": host,
                "port": port,
                "username": "anonymous",
                "password": ""
            }
        },
        "smtp": {
            "id": "smtp_payload_001",
            "action": "send email",
            "data": {
                "host": host,
                "port": port,
                "email": {
                    "from": "test@example.com",
                    "to": "target@example.com",
                    "subject": "Test Payload",
                    "body": "This is a mock SMTP payload."
                }
            }
        }
    }
    return payloads.get(service, None)

# Generate weaponization tasks
def generate_weaponization_tasks(decisions, output_file):
    tasks = []
    for decision in decisions:
        service = decision.get("service")
        host = decision.get("host")
        port = decision.get("port")
        payload = generate_payload(service, host, port)
        if payload:
            tasks.append(payload)

    if tasks:
        # Save weaponization tasks to JSON file
        with open(output_file, "w") as file:
            json.dump(tasks, file, indent=4)
        print(f"Weaponization tasks saved to {output_file}")
    else:
        print("No weaponization tasks were generated.")

# Connect to the database
def connect_to_database(db_file):
    connection = sqlite3.connect(db_file)
    return connection

# Fetch CVEs for weaponization
def fetch_cves_for_service(service_name, connection):
    cursor = connection.cursor()
    query = """
    SELECT cve_id, description, problem_type
    FROM cve_data
    WHERE description LIKE ? OR problem_type LIKE ?
    """
    cursor.execute(query, (f"%{service_name}%", f"%{service_name}%"))
    return cursor.fetchall()

# Generate weaponized payloads
def generate_payloads_for_cves(service_name, connection):
    cve_data = fetch_cves_for_service(service_name, connection)
    payloads = []

    for cve in cve_data:
        cve_id, description, problem_type = cve
        payload = {
            "service": service_name,
            "cve_id": cve_id,
            "description": description,
            "problem_type": problem_type,
            "payload": f"Mock exploit targeting {service_name} based on {cve_id}"
        }
        payloads.append(payload)

    if not payloads:
        print(f"No CVEs found for service: {service_name}")

    return payloads

# Save payloads for weaponization
def save_payloads(payloads, output_file):
    with open(output_file, "w") as file:
        json.dump(payloads, file, indent=4)
    print(f"Weaponized payloads saved to {output_file}")

# Entry point for weaponization module
if __name__ == "__main__":
    # Ensure logs folder exists
    ensure_logs_folder()

    # File paths
    db_file = "roxi_cve_database.db"
    input_decisions_file = os.path.join("logs", "engineData", "decision_log.json")
    output_tasks_file = os.path.join("logs", "weaponized_data", "weaponization_tasks.json")
    output_cves_file = os.path.join("logs", "weaponized_cves.json")
    service_name = "http"  # Replace with the service you want to target

    # Process CVEs and generate payloads
    try:
        connection = connect_to_database(db_file)
        try:
            payloads = generate_payloads_for_cves(service_name, connection)
            save_payloads(payloads, output_cves_file)
        finally:
            connection.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

    # Process decisions
    decisions = load_decisions(input_decisions_file)
    generate_weaponization_tasks(decisions, output_tasks_file)
