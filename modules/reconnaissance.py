import socket
import ipaddress
import json
import os
from datetime import datetime
from time import time

# Function to ensure the dataGathered folder exists
def ensure_data_folder_exists():
    folder_name = "dataGathered"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

# Function to log results into a JSON file
def log_results_to_json(results, filename):
    filepath = os.path.join(ensure_data_folder_exists(), filename)
    
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
        "data": results
    }
    existing_data.append(results_with_timestamp)
    
    # Write updated data back to the file
    with open(filepath, "w") as file:
        json.dump(existing_data, file, indent=4)

# Function to grab the banner (service information) from an open port
def grab_banner(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)  # Adjust timeout as needed
            s.connect((ip, port))
            s.send(b"Hello\r\n")  # Basic message to elicit a response
            banner = s.recv(1024).decode().strip()
            return banner
    except Exception as e:
        return "Unknown Service"

# Function to scan the network
def scan_network(ip_range, port_range):
    print(f"Starting network scan on range {ip_range} for ports {port_range}")
    active_hosts = []

    for ip in ipaddress.IPv4Network(ip_range, strict=False):
        for port in range(port_range[0], port_range[1] + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)  # Adjust timeout as needed
                start_time = time()  # Record the start time
                result = s.connect_ex((str(ip), port))
                end_time = time()  # Record the end time
                
                latency = round((end_time - start_time) * 1000, 2)  # Calculate latency in ms
                protocol = "TCP"  # Currently, this is hardcoded for simplicity

                if result == 0:  # Port is open
                    banner = grab_banner(str(ip), port)  # Get the banner (service info)
                    print(f"[+] Host: {ip} | Port: {port} is open | Service: {banner}")
                    active_hosts.append({
                        "host": str(ip),
                        "port": port,
                        "protocol": protocol,
                        "service": banner,
                        "latency_ms": latency,
                        "status": "open"
                    })
                else:
                    active_hosts.append({
                        "host": str(ip),
                        "port": port,
                        "protocol": protocol,
                        "service": "Unknown",
                        "latency_ms": latency,
                        "status": "closed"
                    })
    return active_hosts

# Main execution block
if __name__ == "__main__":
    # Define the IP range and port range
    ip_range = "192.168.1.0/28"
    port_range = (20, 25)
    
    # Perform the scan
    results = scan_network(ip_range, port_range)
    
    # Save the results to a JSON file
    log_results_to_json(results, "scan_results.json")
    print("Scan completed and results saved to dataGathered/scan_results.json")
