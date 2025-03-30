import json
import os

# Function to load delivery results
def load_delivery_results(filepath):
    try:
        with open(filepath, "r") as file:
            delivery_logs = json.load(file)
            return delivery_logs[-1]["results"]  # Use the latest results
    except FileNotFoundError:
        print(f"Delivery log file not found: {filepath}")
        return []
    except IndexError:
        print(f"No valid delivery results found in the log.")
        return []

# Function to refine decision priorities based on feedback
def refine_decisions(delivery_results, decisions):
    for result in delivery_results:
        status = result["status"]
        task = result["task"]

        # Lower priority for failed deliveries
        if status == "failure":
            for decision in decisions:
                if decision["host"] == task["host"] and decision["port"] == task["port"]:
                    decision["priority"] = max(1, decision["priority"] - 2)  # Reduce priority, minimum 1

        # Raise priority for successful deliveries
        if status == "success":
            for decision in decisions:
                if decision["host"] == task["host"] and decision["port"] == task["port"]:
                    decision["priority"] = min(10, decision["priority"] + 2)  # Increase priority, maximum 10

    return decisions

# Save refined decisions to a new JSON file
def save_refined_decisions(decisions, output_file):
    with open(output_file, "w") as file:
        json.dump(decisions, file, indent=4)
    print(f"Refined decisions saved to {output_file}")

# Main execution
if __name__ == "__main__":
    delivery_log_file = "C:/Users/somto/OneDrive/Desktop/The_Roxi/logs/deliveryLogs/delivery_log.json"
    decision_file = "C:/Users/somto/OneDrive/Desktop/The_Roxi/logs/engineData/decision_log.json"
    refined_decision_file = "C:/Users/somto/OneDrive/Desktop/The_Roxi/logs/engineData/refined_decision_log.json"

    # Step 1: Load delivery results and decisions
    delivery_results = load_delivery_results(delivery_log_file)
    try:
        with open(decision_file, "r") as file:
            decisions = json.load(file)[-1]["decisions"]  # Load the latest decisions
    except FileNotFoundError:
        print(f"Decision log file not found: {decision_file}")
        decisions = []

    # Step 2: Refine decisions based on feedback
    if delivery_results and decisions:
        refined_decisions = refine_decisions(delivery_results, decisions)

        # Step 3: Save refined decisions
        save_refined_decisions(refined_decisions, refined_decision_file)
    else:
        print("No valid data available for feedback refinement.")
