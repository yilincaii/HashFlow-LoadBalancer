import asyncio
import requests
import matplotlib.pyplot as plt

async def make_requests():
    responses = []
    for _ in range(10000):
        response = requests.get('http://127.0.0.1:5000/rep')
        responses.append(response.json()['message']['replicas'])  # Access 'replicas' key
    return responses

async def main():
    response = await make_requests()
    server_counts = {'Server 1': 0, 'Server 2': 0, 'Server 3': 0}
    for servers in response:  # Iterate over each list of servers
        for server in servers:  # Iterate over each server in the list
            server_counts[server] += 1
    
    plt.bar(server_counts.keys(), server_counts.values())
    plt.xlabel('Server Instance')
    plt.ylabel('Request Count')
    plt.title('Request Distribution Among Server Instances (N=3)')
    plt.savefig('experiment_A1_results.png')  # Save the plot as an image file
    plt.show()

if __name__ == '_main_':
    asyncio.run(main())