import os
import platform
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def execute_test_payload():
    logging.info("Executing test payload script...")
    if platform.system() == "Windows":
        test_file_path = os.path.join(os.environ.get("TEMP", "."), "test_payload_success.txt")
    else:
        test_file_path = "/tmp/test_payload_success.txt"

    try:
        with open(test_file_path, "w") as f:
            f.write("Test payload executed successfully!")
        logging.info(f"Test file created at: {test_file_path}")
    except Exception as e:
        logging.error(f"Error creating test file: {e}")

if __name__ == "__main__":
    execute_test_payload()