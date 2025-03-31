import json
import matplotlib.pyplot as plt
import seaborn as sns

# Load delivery data from log file
def load_delivery_data(delivery_log_file):
    try:
        with open(delivery_log_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {delivery_log_file}. Please ensure deliveries are logged.")
        return []
    except json.JSONDecodeError:
        print(f"Error: JSON decoding failed for {delivery_log_file}. Check the file format.")
        return []

# Load refined decisions from log file
def load_decisions_data(decisions_log_file):
    try:
        with open(decisions_log_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {decisions_log_file}. Please ensure decisions are logged.")
        return []
    except json.JSONDecodeError:
        print(f"Error: JSON decoding failed for {decisions_log_file}. Check the file format.")
        return []

# Generate bar graph for delivery success rates
def visualize_delivery_rates(delivery_data):
    service_stats = {}
    for entry in delivery_data:
        for result in entry["results"]:
            service = result["task"]["service"]
            status = result["status"]
            service_stats.setdefault(service, {"success": 0, "failure": 0})
            if status == "success":
                service_stats[service]["success"] += 1
            elif status == "failure":
                service_stats[service]["failure"] += 1

    services = list(service_stats.keys())
    successes = [service_stats[service]["success"] for service in services]
    failures = [service_stats[service]["failure"] for service in services]

    plt.figure(figsize=(10, 6))
    x = range(len(services))
    plt.bar(x, successes, width=0.4, label="Success", color="green", align="center")
    plt.bar(x, failures, width=0.4, label="Failure", color="red", align="edge")
    plt.xticks(x, services)
    plt.xlabel("Service")
    plt.ylabel("Number of Deliveries")
    plt.title("Delivery Success vs Failure Rates by Service")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Generate pie chart for decision priority distribution
def visualize_decision_priorities(decision_data):
    priority_counts = {"high": 0, "low": 0}
    for decision in decision_data:
        priority = decision.get("priority", "low")
        priority_counts[priority] += 1

    labels = ["High Priority", "Low Priority"]
    values = [priority_counts["high"], priority_counts["low"]]

    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct="%1.1f%%", colors=["gold", "lightblue"], startangle=140)
    plt.title("Decision Priority Distribution")
    plt.tight_layout()
    plt.show()

# Entry point for visualization
if __name__ == "__main__":
    delivery_log_file = "logs/deliveryLogs/delivery_log.json"
    decisions_log_file = "logs/engineData/refined_decision_log.json"

    # Load data
    delivery_data = load_delivery_data(delivery_log_file)
    decision_data = load_decisions_data(decisions_log_file)

    # Generate visualizations if data exists
    if delivery_data:
        visualize_delivery_rates(delivery_data)
    else:
        print("Notice: No delivery data available for visualization.")
    if decision_data:
        visualize_decision_priorities(decision_data)
    else:
        print("Notice: No refined decisions available for visualization.")
