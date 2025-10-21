import hashlib
import bisect
import requests
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

class ConsistentHashing:
    def __init__(self, replicas=3):
        self.replicas = replicas
        self.ring = []
        self.nodes = {}

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}-{i}")
            self.ring.append(key)
            self.nodes[key] = node
        self.ring.sort()

    def remove_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}-{i}")
            self.ring.remove(key)
            del self.nodes[key]

    def get_node(self, key):
        if not self.ring:
            return None
        hash_key = self._hash(key)
        idx = bisect.bisect(self.ring, hash_key)
        if idx == len(self.ring):
            idx = 0
        return self.nodes[self.ring[idx]]

class LoadBalancer:
    def __init__(self):
        self.servers = []
        self.consistent_hash = ConsistentHashing()

    def add_server(self, server):
        self.servers.append(server)
        self.consistent_hash.add_node(server)

    def remove_server(self, server):
        self.servers.remove(server)
        self.consistent_hash.remove_node(server)

    def get_server(self, key):
        return self.consistent_hash.get_node(key)

load_balancer = LoadBalancer()

@app.route('/add_server', methods=['POST'])
def add_server():
    server = request.json['server']
    load_balancer.add_server(server)
    return jsonify({'status': 'success', 'message': f'Server {server} added.'})

@app.route('/remove_server', methods=['POST'])
def remove_server():
    server = request.json['server']
    load_balancer.remove_server(server)
    return jsonify({'status': 'success', 'message': f'Server {server} removed.'})

@app.route('/get_server', methods=['GET'])
def get_server():
    key = request.args.get('key')
    server = load_balancer.get_server(key)
    return jsonify({'server': server})

@app.route('/request', methods=['POST'])
def handle_request():
    key = request.json['key']
    server = load_balancer.get_server(key)
    if server:
        try:
            response = requests.post(f"http://{server}/process", json=request.json)
            return jsonify(response.json())
        except requests.exceptions.RequestException:
            return jsonify({'status': 'error', 'message': f'Failed to connect to server {server}.'})
    return jsonify({'status': 'error', 'message': 'No available servers.'})

if __name__ == '__main__':
    # Adding some initial servers for demonstration
    initial_servers = ['127.0.0.1:5001', '127.0.0.1:5002', '127.0.0.1:5003']
    for server in initial_servers:
        load_balancer.add_server(server)
    
    app.run(port=5000)