import requests

def test_endpoints():
    # GET /rep
    response = requests.get('http://localhost:5000/rep')
    print(response.json())

    # POST /add
    response = requests.post('http://localhost:5000/add', json={"n": 2, "hostnames": ["S5", "S4"]})
    print(response.json())

    # DELETE /rm
    response = requests.delete('http://localhost:5000/rm', json={"n": 1, "hostnames": ["S5"]})
    print(response.json())

def simulate_server_failure():
    # Simulate server failure (implementation depends on your environment)
    print("Simulating server failure...")
    # Example command to stop a server container (adjust based on your setup)
    # os.system("docker stop server_container_name")
    
    # Observe how the load balancer spawns a new instance (depends on your setup)
    print("Observing load balancer response to failure...")

if __name__ == '_main_':
    test_endpoints()
    simulate_server_failure()