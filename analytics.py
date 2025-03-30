import json 
import os 
from datetime import datetime
import requests

def analyze_delivery_logs(log_file):
    with open(log_file, "r") as file:
        logs = json.load(file)
    
    total_tasks = 0
    successes = 0
    failures = 0
    service_count = {}

    for entry in logs:
        results = entry["results"]
        for result in results:
            total_tasks += 1
            service = result["task"]["service"]
            status = result["status"]

            # Count service occurrences
            service_count[service] = service_count.get(service, 0) + 1

            # Track success and failure
            if status == "success":
                successes += 1
            elif status == "failure":
                failures += 1

    success_rate = (successes / total_tasks) * 100 if total_tasks > 0 else 0
    return {"success_rate": success_rate, "service_count": service_count, "failures": failures}

if __name__ == "__main__":
    log_file = "C:/Users/somto/OneDrive/Desktop/The_Roxi/logs/deliveryLogs/delivery_log.json"
    analysis_results = analyze_delivery_logs(log_file)
    
    print("Delivery Log Analysis:")
    print(f"Success Rate: {analysis_results['success_rate']}%")
    print(f"Service Count: {analysis_results['service_count']}")
    print(f"Total Failures: {analysis_results['failures']}")
    print(f"Analysis Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# import json
# import plotly.graph_objects as go

# # Load delivery log data
# def load_delivery_data(file_path):
#     try:
#         with open(file_path, "r") as file:
#             logs = json.load(file)
#         return logs
#     except FileNotFoundError:
#         print(f"File not found: {file_path}")
#         return []

# # Analyze the data
# def analyze_delivery_data(logs):
#     service_count = {}
#     successes = 0
#     total_tasks = 0

#     for log in logs:
#         for result in log["results"]:
#             service = result["task"]["service"]
#             status = result["status"]

#             service_count[service] = service_count.get(service, 0) + 1
#             total_tasks += 1
#             if status == "success":
#                 successes += 1

#     success_rate = (successes / total_tasks) * 100 if total_tasks > 0 else 0
#     return service_count, success_rate

# # Create a bar chart
# def create_bar_chart(service_count):
#     services = list(service_count.keys())
#     counts = list(service_count.values())

#     fig = go.Figure(data=[
#         go.Bar(x=services, y=counts, marker_color='blue', text=counts, textposition="auto")
#     ])
#     fig.update_layout(title="Service Usage in Deliveries",
#                       xaxis_title="Services",
#                       yaxis_title="Number of Delivery Attempts")
#     fig.show()

# # Main
# if __name__ == "__main__":
#     log_file = "C:/Users/somto/OneDrive/Desktop/The_Roxi/logs/deliveryLogs/delivery_log.json"
#     logs = load_delivery_data(log_file)
#     if logs:
#         service_count, success_rate = analyze_delivery_data(logs)
#         print(f"Success Rate: {success_rate}%")
#         create_bar_chart(service_count)
#     else:
#         print("No logs available for analytics.")
# #     print(f"Service Count: {service_count}")