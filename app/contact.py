from flask import Flask, request, jsonify, render_template
import csv
from datetime import datetime
import os

def create_app(testing=False):
    app = Flask(__name__, template_folder='../www')

    @app.route('/')
    def home():
        return render_template('contact.html')

    @app.route('/saveMessage', methods=['POST'])
    def save_message():
        data = request.get_json()

        if testing == True:
            csv_file = 'test_contacts.csv'
        else:
            csv_file = 'contacts.csv'

        file_exists = os.path.exists(csv_file)
        
        if file_exists:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                row_count = sum(1 for row in csv.reader(file))
                if row_count >= 1000:
                    print("overload")
                    return jsonify({'message': 'Contact list is full. Try again later.'}), 404
                
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(['NAME', 'EMAIL', 'MESSAGE', 'TIMESTAMP'])
            
            writer.writerow([
                data['name'],
                data['email'],
                data['message'],
                data.get('timestamp', datetime.now().isoformat())
            ])
        print("Stuff happened")
        return jsonify({'message': 'Contact saved successfully'}), 200
    return app