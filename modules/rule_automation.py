import json

# Load existing rules
def load_rules(rules_file):
    try:
        with open(rules_file, "r") as file:
            return json.load(file)["rules"]
    except FileNotFoundError:
        print(f"Error: File not found - {rules_file}. Please provide a valid rules file.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in {rules_file}. Check the file format.")
        return []

# Load delivery results for rule evaluation
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

# Analyze rule performance
def analyze_rule_performance(rules, delivery_results):
    rule_stats = {rule["id"]: {"success": 0, "failure": 0} for rule in rules}

    for entry in delivery_results:
        for result in entry["results"]:
            rule_id = result["task"].get("rule_id")
            status = result["status"]
            if rule_id and rule_id in rule_stats:
                if status == "success":
                    rule_stats[rule_id]["success"] += 1
                elif status == "failure":
                    rule_stats[rule_id]["failure"] += 1

    return rule_stats

# Update rules based on performance
def update_rules(rules, rule_stats):
    updated_rules = []
    for rule in rules:
        stats = rule_stats.get(rule["id"], {"success": 0, "failure": 0})
        success_rate = stats["success"] / (stats["success"] + stats["failure"]) if (stats["success"] + stats["failure"]) > 0 else 0

        # Adjust priority based on success rate
        if success_rate > 0.7:
            rule["priority"] = "high"
        elif success_rate < 0.3:
            rule["priority"] = "low"
        else:
            rule["priority"] = "medium"

        # Example: Mark rule as inactive if it consistently fails
        if stats["failure"] > stats["success"]:
            rule["active"] = False
        else:
            rule["active"] = True

        updated_rules.append(rule)
    return updated_rules

# Save updated rules to a file
def save_updated_rules(updated_rules, output_file):
    try:
        with open(output_file, "w") as file:
            json.dump({"rules": updated_rules}, file, indent=4)
        print(f"Success: Updated rules saved to {output_file}")
    except Exception as e:
        print(f"Error: Failed to save updated rules. Reason: {e}")

# Save an audit trail of rule changes
def log_rule_changes(original_rules, updated_rules, audit_log_file):
    try:
        changes = []
        for old_rule, new_rule in zip(original_rules, updated_rules):
            if old_rule != new_rule:
                changes.append({"old": old_rule, "new": new_rule})

        with open(audit_log_file, "w") as file:
            json.dump({"rule_changes": changes}, file, indent=4)
        print(f"Success: Rule changes logged to {audit_log_file}")
    except Exception as e:
        print(f"Error: Failed to log rule changes. Reason: {e}")

# Entry point for rule automation
if __name__ == "__main__":
    rules_file = "rules.json"
    delivery_log_file = "logs/deliveryLogs/delivery_log.json"
    updated_rules_file = "logs/rulesData/updated_rules.json"
    audit_log_file = "logs/rulesData/rule_audit_log.json"

    # Load rules and delivery results
    rules = load_rules(rules_file)
    delivery_results = load_delivery_results(delivery_log_file)

    # Analyze performance and update rules
    if rules and delivery_results:
        rule_stats = analyze_rule_performance(rules, delivery_results)
        updated_rules = update_rules(rules, rule_stats)

        # Save updated rules and log changes
        save_updated_rules(updated_rules, updated_rules_file)
        log_rule_changes(rules, updated_rules, audit_log_file)
    else:
        print("Notice: Insufficient data for rule updates.")
