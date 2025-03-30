import json
import requests
import os
from datetime import datetime

# Function to ensure the delivery logs folder exists
def ensure_delivery_logs_folder_exists():
    folder_name = "logs/deliveryLogs"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

# Function to log delivery results
def log_delivery_results(results, filename):
    filepath = os.path.join(ensure_delivery_logs_folder_exists(), filename)

    # If the file doesn't exist, create it
    if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            json.dump([], file)

    # Read existing data and append new results
    with open(filepath, "r") as file:
        existing_data = json.load(file)

    # Add a timestamp to the results
    results_with_timestamp = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }
    existing_data.append(results_with_timestamp)

    # Write updated data back to the file
    with open(filepath, "w") as file:
        json.dump(existing_data, file, indent=4)

# Function to simulate HTTP delivery
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

# Function to simulate other deliveries
def mock_delivery(task):
    return {
        "task": task,
        "status": "mock",
        "details": f"Mock delivery for service {task['service']} completed."
    }

# Main function to execute deliveries
def execute_deliveries(task_file):
    try:
        # Load weaponization tasks
        with open(task_file, "r") as file:
            tasks = json.load(file)

        results = []
        for task in tasks:
            if task["service"] == "http":
                result = deliver_http(task)
            else:
                result = mock_delivery(task)  # Generic mock action for non-HTTP services
            results.append(result)

        # Log results
        log_delivery_results(results, "delivery_log.json")
        print("Delivery results saved to logs/deliveryLogs/delivery_log.json")

    except FileNotFoundError:
        print(f"Task file {task_file} not found. Please run the weaponization module first.")

if __name__ == "__main__":
    task_file = "logs/weaponized_data/weaponization_tasks.json"  # Replace with the actual path to weaponization tasks
    execute_deliveries(task_file)
