import json
import requests
import os
from datetime import datetime

# Ensure the delivery logs folder exists
def ensure_delivery_logs_folder_exists():
    folder_name = "logs/deliveryLogs"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

# Log delivery results
def log_delivery_results(results, filename):
    filepath = os.path.join(ensure_delivery_logs_folder_exists(), filename)

    # Ensure the file exists
    if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            json.dump([], file)

    # Append new results with a timestamp
    with open(filepath, "r") as file:
        existing_data = json.load(file)
    results_with_timestamp = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }
    existing_data.append(results_with_timestamp)

    # Save updated results
    with open(filepath, "w") as file:
        json.dump(existing_data, file, indent=4)

# Simulate HTTP delivery
def deliver_http(task):
    try:
        url = f"http://{task['host']}:{task['port']}"
        response = requests.get(url, timeout=5)
        return {
            "task": task,
            "status": "success",
            "details": f"HTTP request successful. Status code: {response.status_code}"
        }
    except requests.exceptions.RequestException as e:
        return {
            "task": task,
            "status": "failure",
            "details": f"HTTP request failed. Error: {str(e)}"
        }

# Simulate FTP delivery
def deliver_ftp(task):
    try:
        return {
            "task": task,
            "status": "success",
            "details": f"FTP probe successful on {task['host']}:{task['port']}."
        }
    except Exception as e:
        return {
            "task": task,
            "status": "failure",
            "details": f"FTP probe failed. Error: {str(e)}"
        }

# Simulate SMTP delivery
def deliver_smtp(task):
    try:
        return {
            "task": task,
            "status": "success",
            "details": f"SMTP probe successful on {task['host']}:{task['port']}."
        }
    except Exception as e:
        return {
            "task": task,
            "status": "failure",
            "details": f"SMTP probe failed. Error: {str(e)}"
        }

# Simulate Telnet delivery
def deliver_telnet(task):
    try:
        return {
            "task": task,
            "status": "success",
            "details": f"Telnet probe successful on {task['host']}:{task['port']}."
        }
    except Exception as e:
        return {
            "task": task,
            "status": "failure",
            "details": f"Telnet probe failed. Error: {str(e)}"
        }

# Default mock delivery
def mock_delivery(task):
    return {
        "task": task,
        "status": "mock",
        "details": f"Mock delivery for service {task['service']} completed."
    }

# Execute delivery based on service type
def execute_delivery(task):
    service = task["service"]
    if service == "ftp":
        return deliver_ftp(task)
    elif service == "smtp":
        return deliver_smtp(task)
    elif service == "telnet":
        return deliver_telnet(task)
    elif service == "http":
        return deliver_http(task)
    else:
        return mock_delivery(task)

# Main execution for deliveries
def execute_deliveries(task_file):
    try:
        with open(task_file, "r") as file:
            tasks = json.load(file)

        results = [execute_delivery(task) for task in tasks]
        log_delivery_results(results, "delivery_log.json")
        print("Delivery results saved to logs/deliveryLogs/delivery_log.json")

    except FileNotFoundError:
        print(f"Task file {task_file} not found. Please run the weaponization module first.")

if __name__ == "__main__":
    task_file = "logs/weaponized_data/weaponization_tasks.json"  # Adjust path as needed
    execute_deliveries(task_file)
