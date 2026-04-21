# 🛡️ Firewall Review System

A collaborative project to analyze firewall configurations and detect security risks.

The Firewall Review System analyzes firewall rule configurations (CSV input) and identifies potential security risks such as open ports, overly permissive rules, and misconfigurations.

It is designed as a modular system with separate components for reading, analyzing, and reporting.

---

## 🚀 Team Onboarding & Setup

Follow these steps exactly to get your environment running.

1. Clone the Project

```powershell
git clone https://github.com/JanJanCpu/firewall-review-system.git
cd firewall-review-system
```

2. Set Up Virtual Environment (One-time)

```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## ⚠️ Troubleshooting

If you get an error saying "Running scripts is disabled on this system" when trying to activate:

1. Open PowerShell as Administrator.

2. Run this command:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

3. Type Y and press Enter.

4. Try activating the venv again.

---

## 🔄 System Flow

1. User uploads a firewall CSV file or inputs firewall rule into a premade input table
2. `reader.py` converts it into structured data
3. `analyzer.py` scans for security risks
4. `reporter.py` generates a summary
5. Results are displayed in the UI dashboard

## 🧪 Testing
Use the included `firewall-rules.csv` as your baseline for development. 
- **Reader Team:** Ensure your output matches the `id` and `port` data types.
- **Analyzer Team:** Your logic must catch the "Any-Any" rules in IDs #2 and #4.

## 📥 Sample Input & Output

### Sample Input (CSV)

id,source,destination,port,action  
1,Any,Any,80,ALLOW

### Sample Output (JSON)

{
"total_risks": 1,
"high_severity": 1,
"status": "DANGER"
}

---

## 📁 Project Structure
```text
firewall-review-system/
├── modules/              # Backend Logic
│   ├── reader.py         # CSV Parsing
│   ├── analyzer.py       # Security Logic
│   └── reporter.py       # Report Generation
├── static/               # CSS, Images, JS
├── templates/            # HTML Files (index.html)
├── venv/                 # Virtual Environment
├── app.py                # Main Flask Application
├── firewall-rules.csv    # Baseline Test Data
├── requirements.txt      # List of dependencies
└── README.md             # Project Documentation

## 🧩 Module Development Guide (Team Tasks)

To keep the system running, each team must follow these "Input/Output" rules. This ensures everyones code "plugs in" correctly to the main engine.

📥 1. File Reading (modules/reader.py)

Task: Create a function that opens the uploaded CSV and turns it into a list.

Function: def process_csv(file):

Target Output: A Python List of Dictionaries.

Example: [{'id': 1, 'port': 80, 'action': 'ALLOW'}, ...]

🔍 2. Security Analysis (modules/analyzer.py)

Task: Receive the list from reader and scan for risks.

Function: def analyze_rules(rules_list):

Risk Logic: \* Flag any port in [21, 23, 80, 445].

Flag any rule where source == "Any" and destination == "Any".

Target Output: A list of "Finding" dictionaries containing severity and messages.

📊 3. Result Reporting (modules/reporter.py)

Task: Summarize the findings for the user.

Function: def generate_summary(findings_list):

Target Output: A summary dictionary.

Example: {'total_risks': 5, 'high_severity': 2, 'status': 'DANGER'}

🎨 4. Frontend / UI (templates/)

Task: Build the user interface.

Files: index.html, style.css.

Required Features:

A file upload button.

A table or dashboard to display the JSON results returned by the backend.

## 🎨 UI/UX Design Requirement

### 1. The Main Dashboard

- **Navigation Sidebar:** Toggle between "New Scan", "Past Reports", and "Team Credits".
- **Dual-Input Area:** \* **Upload:** Drag-and-drop zone for CSV files.
  - **Manual Form:** Entry fields for Source, Destination, Port, and Action.

### 2. Processing & Results

- **Smart Table:** Highlight risky rules in **Red** with security icons (⚠️).
- **PDF Export:** A button to download the finalized security audit.

Any ideas kasi wala ako masyadong clue pagdating sa UI/UX :)

## 🤝 How to Contribute
1. **Pull the latest changes:** `git pull origin main`
2. **Create a branch:** `git checkout -b feature-yourname`
3. **Commit your work:** `git commit -m "Brief description of work"`
4. **Push your branch:** `git push origin feature-yourname`
5. **Open a Pull Request (PR)** on GitHub for Jan to review and merge.
