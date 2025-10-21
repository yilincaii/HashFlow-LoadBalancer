
import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/home')
def home():
    return jsonify({"message": "Hello from Server: {}".format(os.getenv('ID')), "status": "successful"})

@app.route('/heartbeat')
def heartbeat():
    return jsonify({"response": "[EMPTY]", "status": "successful"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)