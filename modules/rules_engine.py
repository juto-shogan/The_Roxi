import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


# Function to load rules from the JSON file
def load_rules(rules_file):
    try:
        with open(rules_file, "r") as file:
            return json.load(file)["rules"]
    except FileNotFoundError:
        print(f"Rules file '{rules_file}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON in '{rules_file}'. Please check the file format.")
        return []

# Function to evaluate a rule's condition against a given task
def evaluate_condition(condition, task):
    return all(task.get(key) == value for key, value in condition.items())

# Function to apply actions from a matched rule to a task
def apply_action(action, task):
    if "priority" in action:
        task["priority"] = action["priority"]
    if "retry" in action:
        task["retry"] = action["retry"]
    return task

# Function to process all rules for a given task
def process_rules(rules, task):
    for rule in rules:
        if evaluate_condition(rule["condition"], task):
            task = apply_action(rule["action"], task)
    return task


# Watchdog event handler for monitoring rule file changes
class RulesUpdateHandler(FileSystemEventHandler):
    def __init__(self, rules_file):
        self.rules_file = rules_file
        self.updated_rules = load_rules(rules_file)

    def on_modified(self, event):
        if event.src_path.endswith(self.rules_file):
            print(f"Rules file '{self.rules_file}' has been updated. Reloading rules...")
            self.updated_rules = load_rules(self.rules_file)


# Function to start watching the rules file for changes
def start_rules_watching(rules_file):
    event_handler = RulesUpdateHandler(rules_file)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    print(f"Started watching '{rules_file}' for updates.")
    return observer


# Keep the observer running (to be used where necessary)
if __name__ == "__main__":
    rules_file = "rules.json"  # Specify the rules file
    observer = start_rules_watching(rules_file)
    try:
        while True:
            time.sleep(1)  # Keeps the script running to monitor file changes
    except KeyboardInterrupt:
        observer.stop()
        print("Stopped watching rules file.")
        observer.join()
