from flask import Flask, jsonify, request
import random
import json
from consistent_hash_map import ConsistentHashMap

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Default values for the load balancer
N = 3  # Number of server containers managed by the load balancer
M = 512  # Total number of slots in the consistent hash map
K = 9  # Number of virtual servers for each server container

# Initialize Consistent Hash Map
chm = ConsistentHashMap(N, M, K)

# List to store the server replicas managed by the load balancer
server_replicas = [f'S{i}' for i in range(1, N + 1)]


@app.route('/rep', methods=['GET'])
def get_replicas():
    response = {
        "message": {
            "N": N,
            "replicas": server_replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200


@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.get_json()
    n = data.get('n')
    hostnames = data.get('hostnames')

    if len(hostnames) > n:
        response = {
            "message": "<Error> Length of hostname list is more than newly added instances",
            "status": "failure"
        }
        return jsonify(response), 400

    for i in range(n):
        if i < len(hostnames):
            server_replicas.append(hostnames[i])
        else:
            server_replicas.append(f'S{random.randint(1, 100)}')

    chm.add_server(n + 3)  # Update Consistent Hash Map

    response = {
        "message": {
            "N": len(server_replicas),
            "replicas": server_replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200


@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.get_json()
    n = data.get('n')
    hostnames = data.get('hostnames')

    if len(hostnames) > n:
        response = {
            "message": "<Error> Length of hostname list is more than removable instances",
            "status": "failure"
        }
        return jsonify(response), 400

    for hostname in hostnames:
        if hostname in server_replicas:
            server_replicas.remove(hostname)

    chm.remove_server(n)

    response = {
        "message": {
            "N": len(server_replicas),
            "replicas": server_replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200


@app.route('/<path>', methods=['GET'])
def route_request(path):
    replica = chm.map_request(int(path))
    if replica not in server_replicas:
        response = {
            "message": f"<Error> '/{path}' endpoint does not exist in server replicas",
            "status": "failure"
        }
        return jsonify(response), 400

    # You may replace the logic below with your actual routing logic to the server replica
    response = {
        "message": f"Request routed to server {replica}",
        "status": "successful"
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)