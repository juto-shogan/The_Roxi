import json
import sqlite3
import matplotlib.pyplot as plt
import os

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

# Visualize delivery success rates
def visualize_delivery_rates(delivery_data):
    if not delivery_data:
        print("No delivery data available for visualization.")
        return

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
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()

# Visualize decision priority distribution
def visualize_decision_priorities(decision_data):
    if not decision_data:
        print("No decision data available for visualization.")
        return

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

# Visualize CVE trends
def visualize_cve_trends(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT COUNT(*) AS total_cves, strftime('%Y', published_date) AS year
        FROM cve_data
        GROUP BY year
        """)
        cve_trends = cursor.fetchall()

        if not cve_trends:
            print("No CVE data available for visualization.")
            return

        years = [trend[1] for trend in cve_trends]
        totals = [trend[0] for trend in cve_trends]

        plt.figure(figsize=(10, 6))
        plt.bar(years, totals, color="skyblue")
        plt.xlabel("Year")
        plt.ylabel("Total CVEs Published")
        plt.title("CVE Trends Over Time")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Entry point for analytics
if __name__ == "__main__":
    delivery_log_file = os.path.join("logs", "deliveryLogs", "delivery_log.json")
    decisions_log_file = os.path.join("logs", "engineData", "refined_decision_log.json")
    db_file = "roxi_cve_database.db"

    # Ensure directories exist
    os.makedirs(os.path.dirname(delivery_log_file), exist_ok=True)
    os.makedirs(os.path.dirname(decisions_log_file), exist_ok=True)

    # Load data
    delivery_data = load_delivery_data(delivery_log_file)
    decision_data = load_decisions_data(decisions_log_file)

    # Generate visualizations
    if delivery_data:
        visualize_delivery_rates(delivery_data)
    if decision_data:
        visualize_decision_priorities(decision_data)
    try:
        connection = sqlite3.connect(db_file)
        visualize_cve_trends(connection)
        connection.close()
    except sqlite3.Error as e:
        print(f"Failed to connect to the database: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")