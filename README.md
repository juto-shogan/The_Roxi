


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

---

## **Modules Overview**

### **1. Decision Engine (`decision_engine.py`)**

- **Purpose**: Processes scan results, generates decisions based on open ports and services.
- **Key Outputs**:
  - `decision_log.json` contains generated decisions.
  - `refined_decision_log.json` contains dynamically adjusted priorities.

### **2. Weaponization (`weaponization.py`)**

- **Purpose**: Matches decisions with vulnerabilities (using mock CVE database) to generate actionable tasks.
- **Key Outputs**:
  - `weaponization_tasks.json` contains prepared payloads and target information.

### **3. Delivery Module (`delivery.py`)**

- **Purpose**: Executes delivery tasks like HTTP GET requests, FTP probing, SMTP testing, and Telnet connection.
- **Key Outputs**:
  - `delivery_log.json` contains results of delivery tasks.

### **4. Feedback Loop (`feedback.py`)**

- **Purpose**: Refines decisions based on success/failure of delivery tasks.
- **Key Outputs**:
  - `refined_decision_log.json` contains updated decisions.

### **5. Persistence Simulation (`persistence.py`)**

- **Purpose**: Simulates maintaining access via backdoors and session tracking.
- **Key Outputs**:
  - `persistence_log.json` contains persistence results.
  - `sessions.json` tracks simulated active sessions.

### **6. Monitoring (`monitor.py`)**

- **Purpose**: Real-time log monitoring for delivery tasks.
- **Key Outputs**:
  - Live streaming console output (tracked in `delivery_log.json`).

---

## **How to Run**

1. **Start the Decision Engine**:

   ```bash
   python modules/decision_engine.py
   ```
2. **Generate Weaponization Tasks**:

   ```bash
   python modules/weaponization.py
   ```
3. **Execute Delivery Tasks**:

   ```bash
   python modules/delivery.py
   ```
4. **Run Feedback Refinement**:

   ```bash
   python modules/feedback.py
   ```
5. **Simulate Persistence**:

   ```bash
   python modules/persistence/persistence.py
   ```
6. **Monitor Logs in Real-Time**:

   ```bash
   python modules/monitoring/monitor.py
   ```

---

## **Future Development**

- **Dynamic CVE Database Integration**:

  - Connect Roxi to a live CVE database for real-world weaponization tasks.
- **Enhanced Analytics**:

  - Expand analytics capabilities to visualize task performance and delivery trends.
- **Parallel Execution**:

  - Implement multi-threading to improve speed and scalability.

---


Certainly, Somto! Here's an update to the `README.md` file that reflects where the project stands, highlighting all the milestones we've achieved and the current state of Roxi:

---

### **README.md**

# **Roxi Project**

Roxi is an evolving intelligent system designed to analyze, process, and dynamically adapt to data-driven scenarios. This document tracks the development progress and outlines the current state of the project.

---

## **Project Overview**

Roxi is being developed to:

- Simulate workflows across services for reconnaissance, weaponization, and persistence.
- Dynamically adapt rules and tasks based on performance and feedback.
- Integrate with large-scale data like CVE records to enhance decision-making and execution.

The system is modular and scalable, designed for efficient data handling and complex coordination across multiple stages.

---

## **Current Progress**

### **1. Weaponization Module**

- **Functionality**: Generates payloads based on detected services and prepares tasks for execution.
- **Capabilities**:
  - Mock payload generation for HTTP, FTP, and SMTP services.
  - Saves weaponized tasks for further execution.
  - Provides a framework for dynamic payload creation, enabling future integration with vulnerability databases.

### **2. Feedback Refinement Module**

- **Functionality**: Refines decision-making based on delivery performance metrics.
- **Capabilities**:
  - Analyzes delivery logs to identify success and failure patterns.
  - Updates decision priorities dynamically based on historical success rates.
  - Outputs refined decision logs for Roxi’s next operations.

### **3. Visualization Module**

- **Functionality**: Provides insights into Roxi’s performance and decisions through visualizations.
- **Capabilities**:
  - Visualizes delivery success vs. failure rates.
  - Displays decision priority distributions using bar charts and pie charts.

### **4. Multi-Service Coordination Module**

- **Functionality**: Orchestrates workflows across multiple services.
- **Capabilities**:
  - Tracks dependencies between tasks (e.g., FTP credential retrieval for HTTP tasks).
  - Updates tasks dynamically based on upstream results.

### **5. Error and Recovery Module**

- **Functionality**: Handles task failures gracefully.
- **Capabilities**:
  - Implements retry mechanisms with adjusted parameters (e.g., alternate ports or payloads).
  - Saves retry outcomes for analysis and follow-up.

### **6. Simulated Persistence Module**

- **Functionality**: Simulates behaviors to maintain access and monitor changes in services.
- **Capabilities**:
  - Periodically scans previously targeted hosts for changes (new services, closed ports).
  - Flags critical updates for follow-up tasks.

### **7. CVE Data Integration (In Progress)**

- **Functionality**: Parses and processes CVE records for integration into Roxi’s decision-making.
- **Current Status**:
  - A script has been implemented to process over 150,000 CVE JSON files.
  - Extracts relevant fields (e.g., `cveId`, `description`, `problem type`, `affected products`).
  - Stores the data in an SQLite database with structured tables.
  - Progress is being tracked, with data processing currently underway.

---

## **Upcoming Tasks**

1. **CVE Data Utilization**:

   - Develop workflows to leverage CVE data for dynamic payload creation.
   - Integrate vulnerability-specific insights into Roxi’s weaponization module.
2. **Database Queries and Analysis**:

   - Implement scripts and tools to query and analyze CVE data for insights.
   - Integrate advanced reporting and analytics for Roxi’s decision-making.
3. **Advanced Feedback and Rule Automation**:

   - Expand rule automation with evolving patterns from CVE data and live feedback loops.

---

## **How to Run the Project**

1. **Database Initialization**:

   - Run the `setup_cve_database.py` script to create database tables and process CVE JSON files.

   ```bash
   python modules/database/setup_cve_database.py
   ```
2. **Modules**:

   - Weaponization: `weaponization.py`
   - Feedback Refinement: `feedback_refinement.py`
   - Multi-Service Coordination: `multi_service_coordination.py`
   - Error and Recovery: `error_recovery.py`
   - Simulated Persistence: `simulated_persistence.py`
   - Visualization: `visualization.py`
3. **Data Visualization**:

   - Use the `visualization.py` script to generate graphs and insights from logs.
4. **Database Inspection**:

   - Use SQLite or DB Browser for SQLite to explore the database (`roxi_cve_database.db`).
