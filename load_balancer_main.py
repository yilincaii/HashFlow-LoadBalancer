from flask import Flask, request, jsonify





app = Flask(__name__)

# Placeholder for the replicas
replicas = ["Server 1", "Server 2", "Server 3"]

@app.route('/rep', methods=['GET'])
def get_replicas():
    response = {
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.get_json()
    n = data.get('n')
    hostnames = data.get('hostnames', [])
    
    if len(hostnames) > n:
        response = {
            "message": "<Error> Length of hostname list is more than newly added instances",
            "status": "failure"
        }
        return jsonify(response), 400

    new_replicas = hostnames[:n]
    replicas.extend(new_replicas)
    
    response = {
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.get_json()
    n = data.get('n')
    hostnames = data.get('hostnames', [])
    
    if len(hostnames) > n:
        response = {
            "message": "<Error> Length of hostname list is more than removable instances",
            "status": "failure"
        }
        return jsonify(response), 400

    for hostname in hostnames:
        if hostname in replicas:
            replicas.remove(hostname)
    
    while len(hostnames) < n and replicas:
        replicas.pop()

    response = {
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200

@app.route('/<path>', methods=['GET'])
def get_path(path):
    if path != "home":
        response = {
            "message": f"<Error> '/{path}' endpoint does not exist in server replicas",
            "status": "failure"
        }
        return jsonify(response), 400
    
    # Here you should have the logic to forward the request to one of the replicas
    response = {
        "message": "Request forwarded to one of the replicas",
        "status": "successful"
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


