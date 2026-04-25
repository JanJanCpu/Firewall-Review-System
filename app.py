from flask import Flask, render_template, render_template, request, jsonify, session
import csv
import io
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))
from analyzer import analyze_rules
from reporter import generate_summary
app = Flask(__name__)
app.secret_key = 'firewall-review-secret-key'

@app.route('/') 
def dashboard():
    csv_data = session.get('csv_data', [])
    report = session.get('report', None)
    return render_template('dashboard.html', csv_data=csv_data, report=report)

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']

        file_bytes = file.read()
        
        try:
            raw_content = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            raw_content = file_bytes.decode('latin-1')
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        csv_data = []
        reader = csv.reader(io.StringIO(raw_content))
        headers = next(reader, None)
        if headers:
            csv_data.append(headers)
            for row in reader:
                if row:
                    csv_data.append(row)
        
        # Convert CSV rows to dict format for analyzer
        rules_list = []
        for row in csv_data[1:]:
            if len(row) >= 5:
                rules_list.append({
                    "id": row[0],
                    "order": row[0],
                    "action": row[1],
                    "src_ip": row[2],
                    "dst_ip": row[3],
                    "port": int(row[4]) if row[4].isdigit() else None
                })
        
        # Run analysis
        findings = analyze_rules(rules_list)
        
        # Generate report
        report = generate_summary(findings)
        report['findings'] = findings
        
        session['csv_data'] = csv_data
        session['filename'] = file.filename
        session['report'] = report

        return jsonify({
            "status": "success",
            "message": f"File '{file.filename}' received and analyzed!",
            "raw_data": raw_content,
            "report": report
            })

    return render_template('upload.html')     

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

if __name__ == '__main__':    
    app.run(debug=True)   