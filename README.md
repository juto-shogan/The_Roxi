
# The Roxi Project

## Overview

**Roxi** is an intelligent automated system designed to simulate reconnaissance, decision-making, weaponization, delivery, persistence, and feedback refinement. Built as a modular framework, Roxi adapts based on live results and grows smarter over time.

---

## **Features**

1. **Reconnaissance and Decision Engine**:

   - Scans targets for open ports and services.
   - Generates decisions based on detected services (e.g., HTTP, SSH, FTP, etc.).
   - Outputs decisions to `decision_log.json` for further processing.
2. **Weaponization Module**:

   - Matches decisions with vulnerabilities or exploits (mock data used for now).
   - Generates weaponization tasks, including prepared payloads, and saves them to `weaponization_tasks.json`.
3. **Delivery Module**:

   - Executes delivery tasks such as HTTP, FTP, Telnet, SMTP probes, or mock payload delivery.
   - Logs delivery results in `delivery_log.json`.
4. **Feedback Loop**:

   - Refines decisions based on delivery outcomes (success/failure).
   - Updates decision priorities dynamically and saves refined decisions in `refined_decision_log.json`.
5. **Persistence Simulation**:

   - Simulates maintaining access via mock backdoors and session tracking.
   - Saves persistence results in `persistence_log.json`.

---

## **File Structure**

```plaintext
The_Roxi/
│
├── data/                     # Data storage for CVE files (future)
│
├── logs/                     # Log storage
│   ├── engineData/           # Decision engine logs
│   │   ├── decision_log.json
│   │   └── refined_decision_log.json
│   ├── weaponized_data/      # Weaponization task logs
│   │   ├── weaponization_tasks.json
│   ├── deliveryLogs/         # Delivery task logs
│   │   ├── delivery_log.json
│   └── persistence/          # Persistence simulation logs
│       ├── sessions.json
│       └── persistence_log.json
│
├── modules/                  # Modular components of Roxi
│   ├── analytics/            # Analytics tools (to be integrated)
│   │   └── delivery_analytics.py
│   ├── database/             # Database setup scripts (future integration)
│   │   ├── setup_cve_database.py
│   │   └── query_cve.py
│   ├── monitoring/           # Real-time monitoring tools
│   │   └── monitor.py
│   ├── persistence/          # Persistence simulation tools
│   │   └── persistence.py
│   ├── weaponization.py      # Generates weaponization tasks
│   ├── decision_engine.py    # Processes scanned data and makes decisions
│   └── delivery.py           # Handles task delivery for various protocols
│
└── README.md                 # Project documentation
```
