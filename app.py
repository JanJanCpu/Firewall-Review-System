from flask import Flask, render_template, render_template, request, jsonify
app = Flask(__name__)

@app.route('/dashboard') #uses index.html as the dashboard page
def home():
    return render_template('index.html')

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

        return jsonify({
            "status": "success",
            "message": f"File '{file.filename}' received and analyzed!",
            "raw_data": raw_content 
            })

    return render_template('upload.html')     

if __name__ == '__main__':    
    app.run(debug=True)   