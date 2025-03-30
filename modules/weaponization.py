import json
import os


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
            decisions = json.load(file)
            return decisions
    except FileNotFoundError:
        print(f"File not found: {decision_file}. Please run the decision engine first.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {decision_file}. Check the file format.")
        return []

# Generate mock payloads based on detected services
import json

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

    # Save weaponization tasks to JSON file
    with open(output_file, "w") as file:
        json.dump(tasks, file, indent=4)
    print(f"Weaponization tasks saved to {output_file}")

# Entry point for weaponization module
if __name__ == "__main__":
    input_decisions_file = "logs/engineData/decision_log.json"  # Input decisions
    output_tasks_file = "logs/weaponized_data/weaponization_tasks.json"  # Output weaponization tasks

    try:
        with open(input_decisions_file, "r") as file:
            decisions = json.load(file)
            generate_weaponization_tasks(decisions, output_tasks_file)
    except FileNotFoundError:
        print(f"File not found: {input_decisions_file}. Please run the decision engine first.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {input_decisions_file}.")
