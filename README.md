Here is the fully formatted, copy-paste ready version of your `README.md`. I have fixed the code blocks, added the JSON syntax highlighting, and ensured the structure looks professional on GitHub.

***

```markdown
# 🛡️ Firewall Review System

A collaborative project to analyze firewall configurations and detect security risks.

The Firewall Review System analyzes firewall rule configurations (CSV input) and identifies potential security risks such as open ports, overly permissive rules, and misconfigurations.

It is designed as a modular system with separate components for reading, analyzing, and reporting.

---

## 🚀 Team Onboarding & Setup

Follow these steps exactly to get your environment running.

1. **Clone the Project**
```powershell
git clone [https://github.com/JanJanCpu/firewall-review-system.git](https://github.com/JanJanCpu/firewall-review-system.git)
cd firewall-review-system
```

2. **Set Up Virtual Environment (One-time)**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. **Install Dependencies**
```powershell
pip install -r requirements.txt
```

---

## ⚠️ Troubleshooting

If you get an error saying *"Running scripts is disabled on this system"* when trying to activate:

1. Open PowerShell as **Administrator**.
2. Run this command:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Type **Y** and press **Enter**.
4. Try activating the `venv` again.

---

## 🔄 System Flow

1. User uploads a firewall CSV file or inputs firewall rules into a manual form.
2. `reader.py` converts the raw data into structured Python dictionaries.
3. `analyzer.py` scans the rules for security vulnerabilities.
4. `reporter.py` generates a summary and prepares data for export.
5. Results are displayed on the UI dashboard and available for PDF download.

---

## 🧪 Testing Baseline
Use the included `firewall-rules.csv` as your baseline for development. 
- **Reader Team:** Ensure your output matches the `id` and `port` data types (Integers).
- **Analyzer Team:** Your logic must catch the "Any-Any" rules in IDs #2 and #4.

### Sample Input (CSV)
```csv
id,source,destination,port,action
1,Any,Any,80,ALLOW
```

### Sample Output (JSON)
```json
{
  "total_risks": 1,
  "high_severity": 1,
  "status": "DANGER"
}
```

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
```

---

## 🧩 Module Development Guide (Team Tasks)

To keep the system running, each team must follow these **"Input/Output"** rules.

### 📥 1. File Reading (`modules/reader.py`)
- **Lead:** MauRys
- **Task:** Create a function that opens the uploaded CSV and turns it into a list.
- **Function:** `def process_csv(file):`
- **Target Output:** `[{'id': 1, 'source': 'Any', 'port': 80, 'action': 'ALLOW'}, ...]`

### 🔍 2. Security Analysis (`modules/analyzer.py`)
- **Leads:** Tine & Pesa
- **Task:** Receive the list from reader and scan for risks.
- **Function:** `def analyze_rules(rules_list):`
- **Risk Logic:** Flag ports [21, 23, 80, 445] and "Any-Any" source/destination combinations.
- **Target Output:** List of dictionaries containing `severity` and `message`.

### 📊 3. Result Reporting (`modules/reporter.py`)
- **Leads:** Dar & Nate
- **Task:** Summarize the findings for the user and handle PDF generation.
- **Function:** `def generate_summary(findings_list):`
- **Target Output:** `{'total_risks': 5, 'high_severity': 2, 'status': 'DANGER'}`

### 🎨 4. Frontend / UI (`templates/` & `static/`)
- **Leads:** Bel, Gab, Neil
- **Task:** Build the user interface and dashboard.
- **Required Features:** - Navigation Sidebar (New Scan, History, Credits).
    - Dual-Input System (File Upload + Manual Entry Form).
    - High-visibility "Security Score" gauge.
    - Result table with row-highlighting for risks.

Any ideas kasi wala ako masyadong clue pagdating sa UI/UX :)

---

## 🤝 How to Contribute
1. **Pull the latest changes:** `git pull origin main`
2. **Create a branch:** `git checkout -b feature-yourname`
3. **Commit your work:** `git commit -m "Brief description of work"`
4. **Push your branch:** `git push origin feature-yourname`
5. **Open a Pull Request (PR)** on GitHub for Jan to review and merge.
```
