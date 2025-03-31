import json

# Load tasks from delivery log
def load_tasks(delivery_log_file):
    try:
        with open(delivery_log_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {delivery_log_file}.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in {delivery_log_file}.")
        return []

# Simulate dependency handling
def handle_service_dependencies(tasks):
    coordinated_tasks = []
    ftp_credentials = None

    for task in tasks:
        service = task["task"]["service"]
        if service == "ftp" and task["status"] == "success":
            ftp_credentials = {
                "username": "retrieved_user",
                "password": "retrieved_pass"
            }
        elif service == "http" and ftp_credentials:
            task["task"]["action"] = "send POST request"
            task["task"]["data"]["credentials"] = ftp_credentials
        coordinated_tasks.append(task)

    return coordinated_tasks

# Save coordinated tasks
def save_coordinated_tasks(tasks, output_file):
    try:
        with open(output_file, "w") as file:
            json.dump(tasks, file, indent=4)
        print(f"Coordinated tasks saved to {output_file}")
    except Exception as e:
        print(f"Error: Failed to save coordinated tasks. Reason: {e}")

# Entry point for multi-service coordination module
if __name__ == "__main__":
    delivery_log_file = "logs/deliveryLogs/delivery_log.json"
    coordinated_tasks_file = "logs/engineData/coordinated_tasks.json"

    # Load tasks
    tasks = load_tasks(delivery_log_file)

    # Handle dependencies and save coordinated tasks
    if tasks:
        coordinated_tasks = handle_service_dependencies(tasks)
        save_coordinated_tasks(coordinated_tasks, coordinated_tasks_file)
    else:
        print("Notice: No tasks available for coordination.")
