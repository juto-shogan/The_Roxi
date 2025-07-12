# The Roxi Project – Reboot Plan

## Vision

Roxi is a rule-based, modular, conversational AI hacker simulator that performs network attacks such as WiFi cracking and recon. It should be beginner-friendly, log every step it performs, and grow smarter by remembering past tasks and users. Roxi is designed to be controlled via human-like conversation and built collaboratively by a team of seven.

---

## Final Project Structure

```
The_Roxi/
├── main.py                        # Entry point for Roxi
├── config.yaml                    # Tool and settings config

├── interface/                     # Handles user interaction
│   └── roxi_cli.py                # Text-based interface (Phase 1)

├── core/                          # Logic and parsing engine
│   ├── parser.py                  # Converts human input into intent
│   ├── task_runner.py             # Executes tasks via rules
│   └── rules.py                   # Mapping of intents to modules

├── modules/                       # Actual attack modules
│   ├── recon/                     # Ping, port scan, WiFi scan
│   ├── exploit/                   # WiFi cracking, router exploits
│   └── persistence/               # Reverse shell, autorun, etc.

├── memory/                        # Persistent user/task memory
│   └── memory.json                # Stores all user history

├── logs/                          # Per-session execution logs
│   └── activity_logs/
│       └── 2025-07-08_roxi_log.json

├── tests/                         # Future test files
└── README.md                      # Project documentation
```

---

## System Architecture Overview

```
             ┌─────────────────────────────┐
             │         User                │
             └────────────┬────────────────┘
                          │
                (Natural language input)
                          │
                          ▼
             ┌─────────────────────────────┐
             │      Interface Layer        │
             │       (roxi_cli.py)         │
             └────────────┬────────────────┘
                          ▼
             ┌─────────────────────────────┐
             │        Parser Engine        │
             │       (parser.py)           │
             └────────────┬────────────────┘
                          ▼
             ┌─────────────────────────────┐
             │      Rule Engine (rules)    │
             └────────────┬────────────────┘
                          ▼
             ┌─────────────────────────────┐
             │   Task Executor (runner)    │
             └────────────┬────────────────┘
                          ▼
             ┌─────────────────────────────┐
             │     Modules (recon, etc)    │
             └────────────┬────────────────┘
                          ▼
             ┌─────────────────────────────┐
             │ Memory & Logs (JSON files)  │
             └─────────────────────────────┘
```

---

## Roadmap and To-Do List

### Phase 1: MVP (Command Line Interface + Core System)

* [ ] Build CLI interface to talk to Roxi
* [ ] Implement parser.py to convert text to intent
* [ ] Implement rule engine to match intent to toolchain
* [ ] Build a simple WiFi recon and crack module
* [ ] Log actions and memory to JSON

### Phase 2: Expansion

* [ ] Add persistence tools (reverse shell, autorun)
* [ ] Add feedback handling based on delivery results
* [ ] Enhance long-term memory (users and tasks)
* [ ] Add testing suite

### Phase 3: Voice and Web Interface (Optional)

* [ ] Add microphone input and speech synthesis (using Python libraries)
* [ ] Add Streamlit or Flask interface for non-terminal use

---

## Memory File Design (Example)

```json
{
  "users": {
    "Somto": {
      "history": [
        {
          "task": "WiFi crack",
          "input": "Please hack John's WiFi",
          "steps": ["scanned", "captured", "cracked"],
          "output": "Password: johns_wifi123",
          "timestamp": "2025-07-12T19:10:00"
        }
      ]
    }
  }
}
```

---

## Rules File Example

```python
rules = {
    "wifi_attack": {
        "tools": ["airmon-ng", "airodump-ng", "aircrack-ng"],
        "workflow": ["monitor_mode", "capture_handshake", "crack"]
    },
    "network_scan": {
        "tools": ["nmap"],
        "workflow": ["ping_sweep", "port_scan"]
    }
}
```

---

## Next Step

If you'd like, I can now:

* Generate the starter codebase with this exact structure
* Package it into a ZIP file
* Assign a file/module to each of your 7 team members with estimated work time

Would you like me to generate the starter project ZIP for you now?
