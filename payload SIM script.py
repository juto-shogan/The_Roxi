import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def simulate_payload():
    logging.info("Starting simulated payload execution...")
    try:
        message = "Payload executed successfully!"
        file_path = "/tmp/payload_simulation.txt"
        with open(file_path, "w") as f:
            f.write(message)
        logging.info(f"Simulated payload written to: {file_path}")
    except Exception as e:
        logging.error(f"Failed to simulate payload: {e}")

if __name__ == "__main__":
    simulate_payload()