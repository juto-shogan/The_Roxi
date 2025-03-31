import json
import os
import sqlite3

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
        total_attempts = stats["success"] + stats["failure"]
        success_rate = stats["success"] / total_attempts if total_attempts > 0 else 0

        # Adjust priority based on success rate
        if success_rate > 0.7:
            rule["priority"] = "high"
        elif success_rate < 0.3:
            rule["priority"] = "low"
        else:
            rule["priority"] = "medium"

        # Mark rule as inactive if it consistently fails
        rule["active"] = stats["failure"] <= stats["success"]

        print(f"Updated rule: {rule['id']} with priority: {rule['priority']}")
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
        changes = [{"old": old_rule, "new": new_rule} for old_rule, new_rule in zip(original_rules, updated_rules) if old_rule != new_rule]

        with open(audit_log_file, "w") as file:
            json.dump({"rule_changes": changes}, file, indent=4)
        print(f"Success: Rule changes logged to {audit_log_file}")
    except Exception as e:
        print(f"Error: Failed to log rule changes. Reason: {e}")

# Integrate CVE data into rule automation
def update_rules_with_cve_data(rules, connection):
    try:
        cursor = connection.cursor()
        updated_rules = []

        for rule in rules:
            cve_id = rule.get("cve_id")
            if cve_id:
                # Fetch CVE details
                query = "SELECT description, problem_type FROM cve_data WHERE cve_id = ?"
                cursor.execute(query, (cve_id,))
                result = cursor.fetchone()

                if result:
                    description, problem_type = result
                    if "critical" in description.lower() or "high" in problem_type.lower():
                        rule["priority"] = "high"
                    else:
                        rule["priority"] = "medium"

            updated_rules.append(rule)
        return updated_rules
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return rules  # Return original rules if there was an error

# Entry point for rule automation
if __name__ == "__main__":
    rules_file = os.path.join("rules.json")
    delivery_log_file = os.path.join("logs", "deliveryLogs", "delivery_log.json")
    updated_rules_file = os.path.join("logs", "rulesData", "updated_rules.json")
    audit_log_file = os.path.join("logs", "rulesData", "rule_audit_log.json")

    rules = load_rules(rules_file)
    delivery_results = load_delivery_results(delivery_log_file)

    if rules and delivery_results:
        rule_stats = analyze_rule_performance(rules, delivery_results)
        updated_rules = update_rules(rules, rule_stats)
        save_updated_rules(updated_rules, updated_rules_file)
        log_rule_changes(rules, updated_rules, audit_log_file)
    else:
        print("Notice: Insufficient data for rule updates.")
