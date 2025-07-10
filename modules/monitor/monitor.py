import time

def monitor_logs(log_file):
    print("Monitoring logs in real-time...")
    with open(log_file, "r") as file:
        while True:
            where = file.tell()
            line = file.readline()
            if not line:
                time.sleep(1)
                file.seek(where)
            else:
                print(line.strip())

if __name__ == "__main__":
    log_file = r"/deliveryLogs/delivery_log.json"
    monitor_logs(log_file)
