from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/get_data')
def get_data():
    with open("app/files/data.json", "r") as json_file:
        data = json.load(json_file)
    print(jsonify(data))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)