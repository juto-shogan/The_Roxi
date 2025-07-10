# The Roxi Project

## Overview

**Roxi** is an intelligent automated system designed to simulate reconnaissance, decision-making, weaponization, delivery, persistence, and feedback refinement. Built as a modular framework, Roxi adapts based on live results and grows smarter over time.

---

## **new File Structure**

```plaintext
The_Roxi/
│
├── interface/               # CLI or chat UI
│   └── roxi_cli.py
│
├── core/                    # Parser, task manager, rule engine
│   ├── parser.py
│   ├── task_runner.py
│   └── rules.py
│
├── modules/                 # Task modules (network-focused)
│   ├── recon/               # airodump, nmap, ping sweep
│   ├── exploit/             # WiFi cracking, router exploits
│   └── persistence/         # reverse shell, autorun, C2
│
├── memory/                  # Persistent data
│   └── memory.json
│
├── logs/                    # Full logs of every interaction and action
│   └── activity_logs/
│       └── 2025-07-08_roxi_log.json
│
├── tests/                   # Unit tests for modules
│
├── config.yaml              # Configuration file (tools, default ports, etc.)
└── main.py                  # Starts Roxi, loads modules

```

---


## 🔧 TO DO (BY PHASE)

### 📌 **Phase 1: MVP (This Week)**

* [ ] Build CLI interface to talk to Roxi
* [ ] Implement `parser.py` to turn text into intent
* [ ] Implement rule engine to match intent to toolchain
* [ ] Build a simple WiFi recon + crack module
* [ ] Log actions and memory

### 📌 **Phase 2: Expansion**

* [ ] Add persistence tools
* [ ] Add feedback on success/failure
* [ ] Start saving long-term memory (per user/task)
* [ ] Build simple test suite

### 📌 **Phase 3: Voice + Web (Optional)**

* [ ] Add microphone input and TTS with `speech_recognition` and `pyttsx3`
* [ ] Optional: Streamlit or Flask frontend for users
