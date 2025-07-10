# dummy.py
import os
import platform

def execute_payload():
    print("Dummy script executed!")
    # Create a test file in a platform-independent way
    if platform.system() == "Windows":
        test_file_path = os.path.join(os.environ["TEMP"], "payload_success.txt") # Use temp directory
    else:  # Linux/macOS
        test_file_path = "/tmp/payload_success.txt"

    try:
        with open(test_file_path, "w") as f:
            f.write("Payload executed successfully!")
        print(f"Test file created at: {test_file_path}") # Print for debugging
    except Exception as e:
        print(f"Error creating test file: {e}")

if __name__ == "__main__":
    execute_payload()