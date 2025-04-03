from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import csv
import io
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')

# Get default addresses from environment variables
DEFAULT_TOKEN_ADDRESS = os.getenv('TOKEN_ADDRESS', '0xb7109df1a93f8fe2B8162c6207C9B846C1C68090')
DEFAULT_BULK_CONTRACT_ADDRESS = os.getenv('BULK_CONTRACT_ADDRESS', '0xBbFe81A1B144a33d30d4D871b9737D3b7Be8F7de')

# Create a Web3 instance (no provider needed here for format conversion)
w3 = Web3()

@app.route('/')
def index():
    return render_template('index.html', 
                          token_address=DEFAULT_TOKEN_ADDRESS,
                          bulk_contract_address=DEFAULT_BULK_CONTRACT_ADDRESS)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        try:
            # Read the CSV file
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_data = list(csv.reader(stream))
            
            # Process the CSV data
            recipients = []
            for row in csv_data:
                if len(row) >= 2:
                    address = row[0].strip()
                    amount = row[1].strip()
                    
                    # Basic validation
                    if address.startswith('0x') and len(address) == 42:
                        recipients.append({
                            'address': address,
                            'amount': amount
                        })
            
            return jsonify({'recipients': recipients})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file format. Please upload a CSV file.'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 