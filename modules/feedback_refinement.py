import json

# Load delivery results
def load_delivery_results(delivery_log_file):
    try:
        with open(delivery_log_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {delivery_log_file}. Please ensure deliveries have been logged.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in {delivery_log_file}. Check the file format.")
        return []

# Analyze delivery results
def analyze_delivery_results(delivery_results):
    service_metrics = {}
    for entry in delivery_results:
        for result in entry["results"]:
            service = result["task"]["service"]
            status = result["status"]
            service_metrics.setdefault(service, {"success": 0, "failure": 0})
            if status == "success":
                service_metrics[service]["success"] += 1
            elif status == "failure":
                service_metrics[service]["failure"] += 1
    return service_metrics

# Refine decisions based on delivery analysis
def refine_decisions(decisions, service_metrics):
    refined_decisions = []
    for decision in decisions:
        service = decision.get("service")
        metrics = service_metrics.get(service, {"success": 0, "failure": 0})
        if metrics["failure"] > metrics["success"]:
            decision["priority"] = "low"  # Lower priority for less reliable services
        else:
            decision["priority"] = "high"  # Boost priority for successful services
        refined_decisions.append(decision)
    return refined_decisions

# Save refined decisions to JSON file
def save_refined_decisions(refined_decisions, output_file):
    try:
        with open(output_file, "w") as file:
            json.dump(refined_decisions, file, indent=4)
        print(f"Success: Refined decisions saved to {output_file}")
    except Exception as e:
        print(f"Error: Failed to save refined decisions to {output_file}. Reason: {e}")

# Entry point for feedback refinement module
if __name__ == "__main__":
    delivery_log_file = "logs/deliveryLogs/delivery_log.json"
    decisions_file = "logs/engineData/decision_log.json"
    refined_decisions_file = "logs/engineData/refined_decision_log.json"

    # Load delivery results
    delivery_results = load_delivery_results(delivery_log_file)

    # Analyze delivery metrics
    service_metrics = analyze_delivery_results(delivery_results)

    # Load decisions
    try:
        with open(decisions_file, "r") as file:
            decisions = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {decisions_file}. Please ensure decisions are logged.")
        decisions = []

    # Refine decisions based on delivery metrics
    if decisions:
        refined_decisions = refine_decisions(decisions, service_metrics)
        save_refined_decisions(refined_decisions, refined_decisions_file)
    else:
        print("Notice: No decisions available for refinement.")
