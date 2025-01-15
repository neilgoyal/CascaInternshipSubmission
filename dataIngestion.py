import os
import pandas as pd
from pdfminer.high_level import extract_text
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
   try:
       text = extract_text(file_path)
       return text
   except Exception as e:
       return str(e)

# Function to parse text into a structured DataFrame
def parse_transactions(text):
   transactions = []
   lines = text.split('\n')
   for line in lines:
       if any(char.isdigit() for char in line):
           parts = line.split()
           if len(parts) >= 5:
               date, description, debit, credit, balance = parts[:5]
               transactions.append({
                   'Date': date,
                   'Description': ' '.join(parts[1:-3]),
                   'Debit': float(debit) if debit.replace('.', '').isdigit() else 0.0,
                   'Credit': float(credit) if credit.replace('.', '').isdigit() else 0.0,
                   'Balance': float(balance) if balance.replace('.', '').isdigit() else 0.0
               })
   return pd.DataFrame(transactions)

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
   if 'file' not in request.files:
       return jsonify({'error': 'No file part'}), 400

   file = request.files['file']
   if file.filename == '':
       return jsonify({'error': 'No selected file'}), 400

   file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
   file.save(file_path)

   # Extract and process text
   text = extract_text_from_pdf(file_path)
   transactions_df = parse_transactions(text)

   # Return structured data as JSON
   return jsonify(transactions_df.to_dict(orient='records'))

# Run the Flask app
if __name__ == '__main__':
   app.run(port=3000, debug=True)
