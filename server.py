from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def handle_request():
    return jsonify({"message": "Handled by server"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)  # Change the port if necessary for different servers