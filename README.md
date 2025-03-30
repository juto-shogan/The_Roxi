# Roxi Project

## **Overview**

Welcome to the Roxi project—an ambitious journey to develop a modular, intelligent system designed for advanced network operations and learning capabilities. Roxi aims to evolve into a robust tool that seamlessly integrates reconnaissance, decision-making, exploitation, and persistence functions.

---

## **What We’ve Done So Far**

### **1. Project Structure**

We’ve laid out a well-defined and scalable project directory structure for Roxi to ensure clear organization and modularity. The structure includes folders for `config`, `modules`, `utils`, `dataGathered`, and more, setting the foundation for efficient development and future expansion.

### **2. Reconnaissance Module**

The reconnaissance module serves as Roxi’s gateway to the network. It scans an IP range and port range, detects open ports, and logs results. Key features include:

- **Banner Grabbing**: Retrieves basic service information for detected open ports.
- **JSON Logging**: Logs scan results with detailed metadata (host, port, protocol, latency, status, and service info) into a JSON file within the `dataGathered` folder.
- **Dynamic Folder Creation**: Ensures a dedicated folder (`dataGathered`) is created to store scan logs systematically.

### **3. Decision Engine**

While the decision engine is in the planning stage, we’ve defined its scope and capabilities to ensure it will seamlessly integrate with other modules. The decision engine will act as Roxi’s “brain,” making intelligent decisions based on the reconnaissance results, predefined rules, and dynamic learning in future iterations.

#### **Scope and Goals for the Decision Engine**

- **Input Handling**: Process structured data from modules like reconnaissance and exploitation.
- **Rule-Based Logic**: Make initial decisions using simple `if-else` conditions.
- **Task Sequencing**: Prioritize actions and coordinate steps based on risk and impact.
- **Learning and Feedback**: Integrate reinforcement learning for dynamic improvements in decision-making.
- **Modular Interaction**: Act as a middle layer connecting reconnaissance, exploitation, persistence, and logging.

---

## **Next Steps**

### **1. Build the Decision Engine**

- Implement a rule-based framework for immediate decision-making based on scan results.
- Gradually expand with scoring systems and feedback loops for smarter decisions.

### **2. Refine the Reconnaissance Module**

- Introduce multithreading for faster scans.
- Expand service detection capabilities and integrate deeper analyses.

### **3. Modular Development**

- Lay the groundwork for exploitation and persistence modules that interact seamlessly with the decision engine.

---

## **How to Run the Project**

To set up and run the current modules:

1. Clone this repository.
2. Navigate to the project directory.
3. Run the `reconnaissance.py` module:
   ```bash
   python modules/reconnaissance.py
   ```
