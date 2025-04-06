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
DEFAULT_TOKEN_ADDRESS = os.getenv('TOKEN_ADDRESS', '0xdAC17F958D2ee523a2206206994597C13D831ec7')
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/upload', methods=['POST'])
def upload():
    # Redirect to upload_csv function to handle both endpoint URLs
    return upload_csv()

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        try:
            # Read the CSV file correctly
            content = file.read()
            stream = io.StringIO(content.decode("UTF-8", errors='replace'))
            csv_data = list(csv.reader(stream))
            
            # Process the CSV data
            recipients = []
            amounts = []
            
            for row in csv_data:
                if len(row) >= 2:
                    address = row[0].strip()
                    amount = row[1].strip()
                    
                    # Basic validation
                    if address.startswith('0x') and len(address) == 42:
                        recipients.append(address)
                        amounts.append(amount)
            
            return jsonify({
                'recipients': recipients,
                'amounts': amounts
            })
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file format. Please upload a CSV file.'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 