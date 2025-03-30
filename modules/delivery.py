import json
import sys
import requests
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from modules.rules_engine import load_rules, process_rules

# Ensure the delivery logs folder exists
def ensure_delivery_logs_folder_exists():
    folder_name = "logs/deliveryLogs"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name
# Ensure the delivery logs folder exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Log delivery results
def log_delivery_results(results, filename):
    # Ensure directory exists before writing
    directory = os.path.dirname(filename)
    ensure_directory_exists(directory)

    # Write delivery results
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            json.dump([], file)

    with open(filename, "r") as file:
        existing_data = json.load(file)

    results_with_timestamp = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }
    existing_data.append(results_with_timestamp)

    with open(filename, "w") as file:
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


# Execute delivery with rules
def execute_delivery_with_rules(task, rules_file):
    rules = load_rules(rules_file)
    task = process_rules(rules, task)
    return execute_delivery(task)

# Main execution for deliveries
def execute_deliveries_with_rules(task_file, rules_file):
    try:
        with open(task_file, "r") as file:
            tasks = json.load(file)

        results = []
        for task in tasks:
            result = execute_delivery_with_rules(task, rules_file)
            results.append(result)

        log_delivery_results(results, "delivery_log.json")
        print("Delivery results saved to logs/deliveryLogs/delivery_log.json")

    except FileNotFoundError:
        print(f"Task file {task_file} not found. Please run the weaponization module first.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {task_file}.")
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

# Entry point for the script
if __name__ == "__main__":
    # Define paths for weaponized tasks and rules
    task_file = "logs/weaponized_data/weaponization_tasks.json"
    rules_file = "rules.json"

    try:
        # Load tasks from the weaponization log
        with open(task_file, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        print(f"Task file {task_file} not found. Please run the weaponization module first.")
        tasks = []
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {task_file}.")
        tasks = []

    if tasks:
        # Load rules and apply them during delivery
        rules = load_rules(rules_file)
        results = []
        for task in tasks:
            task = process_rules(rules, task)  # Apply rules to task
            result = execute_delivery(task)  # Standard delivery logic
            results.append(result)

        # Log the delivery results to the logs folder
        log_delivery_results(results, "logs/deliveryLogs/delivery_log.json")
        print("Delivery results saved to logs/deliveryLogs/delivery_log.json")
    else:
        print("No tasks found. Please check the weaponization output.")