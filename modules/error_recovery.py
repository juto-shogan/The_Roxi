import json
import random

# Load tasks
def load_failed_tasks(delivery_log_file):
    try:
        with open(delivery_log_file, "r") as file:
            delivery_data = json.load(file)
            return [result for entry in delivery_data for result in entry["results"] if result["status"] == "failure"]
    except FileNotFoundError:
        print(f"Error: File not found - {delivery_log_file}.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in {delivery_log_file}.")
        return []

# Simulate retry logic
def retry_failed_tasks(failed_tasks):
    retry_results = []
    for task in failed_tasks:
        # Simulate retry with adjusted parameters
        retry_task = task.copy()
        retry_task["task"]["port"] = random.choice([22, 80, 443])  # Randomly select alternative port
        retry_task["status"] = random.choice(["success", "failure"])  # Simulate success or failure
        retry_results.append(retry_task)
    return retry_results

# Save retry results
def save_retry_results(results, output_file):
    try:
        with open(output_file, "w") as file:
            json.dump(results, file, indent=4)
        print(f"Retry results saved to {output_file}")
    except Exception as e:
        print(f"Error: Failed to save retry results. Reason: {e}")

# Entry point for error recovery module
if __name__ == "__main__":
    delivery_log_file = "logs/deliveryLogs/delivery_log.json"
    retry_results_file = "logs/deliveryLogs/retry_results.json"

    # Load failed tasks
    failed_tasks = load_failed_tasks(delivery_log_file)

    # Retry and save results
    if failed_tasks:
        retry_results = retry_failed_tasks(failed_tasks)
        save_retry_results(retry_results, retry_results_file)
    else:
        print("Notice: No failed tasks available for retry.")
