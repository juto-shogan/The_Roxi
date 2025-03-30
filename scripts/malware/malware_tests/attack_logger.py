import logging
import os
from datetime import datetime

class AttackLogger:
    def __init__(self, log_dir="attack_logs"):  # Default log directory
        self.log_dir = log_dir
        self.log_file = None  # Will be set dynamically

        # Create log directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def start_new_log(self, attack_name="malware_attack"):  # Start a new log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"{attack_name}_{timestamp}.log")

        # Set up the logger
        logging.basicConfig(filename=self.log_file, level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")
        logging.info(f"Starting new log for {attack_name}...")  # Initial log message

    def log(self, level, message):  # Log a message with a specific level
        if self.log_file:  # Check if a log file is started
            if level == "info":
                logging.info(message)
            elif level == "warning":
                logging.warning(message)
            elif level == "error":
                logging.error(message)
            elif level == "debug":
                logging.debug(message)
            else:
                logging.info(message) # Default to info if the level is not valid
        else:
            print("No log file started. Call start_new_log() first.")  # Handle if no log file is started

    def log_recon(self, target_ip, os_type=None):
        message = f"Reconnaissance on {target_ip}"
        if os_type:
            message += f" - Detected OS: {os_type}"
        self.log("info", message)

    def log_weaponization(self, attack_type, target_ip):
        self.log("info", f"Weaponizing {attack_type} on {target_ip}...")

    def log_delivery(self, delivery_method, target_ip):
        self.log("info", f"Delivering payload via {delivery_method} to {target_ip}...")

    def log_exploitation(self, target_ip, exploit_type):
        self.log("info", f"Exploiting {exploit_type} on {target_ip}...")

    def log_post_exploitation(self, target_ip, action):
        self.log("info", f"Post-exploitation: {action} on {target_ip}...")

    def log_c2(self, target_ip, action):
        self.log("info", f"C2 operation: {action} on {target_ip}...")

    def log_evasion(self, technique):
        self.log("info", f"Evasion technique used: {technique}...")

    def log_exfiltration(self, target_ip, method, destination):
        self.log("info", f"Exfiltrating data from {target_ip} to {destination} via {method}...")

    # Add other logging methods as needed (e.g., for lateral movement, persistence, impact)
    def log_lateral_movement(self, target_ip, method):
        self.log("info", f"Lateral movement to {target_ip} via {method}...")

    def log_persistence(self, target_ip, method):
        self.log("info", f"Establishing persistence on {target_ip} via {method}...")

    def log_impact(self, target_ip, action):
        self.log("info", f"Impact: {action} on {target_ip}...")

    def log_error(self, message):  # Dedicated error logging
        self.log("error", message)