from flask import Flask, request, jsonify, render_template
from web3 import Web3
import csv
import io

app = Flask(__name__)

# Assume token has 18 decimals
TOKEN_DECIMALS = 18

# Create a Web3 instance (no provider needed here for format conversion)
w3 = Web3()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Read file as text using io.StringIO
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    recipients = []
    amounts = []
    for row in csv_input:
        if len(row) < 2:
            continue
        addr = row[0].strip()
        amt_str = row[1].strip()
        # Validate Ethereum address using Web3.py
        if not w3.is_address(addr):
            print(f"Skipping invalid address: {addr}")
            continue

        recipients.append(addr)
        amounts.append(amt_str)  # Return as string for JSON compatibility
    return jsonify({"recipients": recipients, "amounts": amounts})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 