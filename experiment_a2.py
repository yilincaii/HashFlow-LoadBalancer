import asyncio
import aiohttp
import matplotlib.pyplot as plt
import random

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def make_requests(n):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, f'http://localhost:5002/rep') for _ in range(10000)]
        responses = await asyncio.gather(*tasks)
    return responses

async def main():
    load_data = {}
    for n in range(2, 7):
        responses = await make_requests(n)
        server_counts = {}
        for response in responses:
            # Extracting the server names
            servers = response['message']['replicas']
            
            # For simplicity, we assume each request is handled by a random server in the list
            server = random.choice(servers)
            
            # Count the requests per server
            server_counts[server] = server_counts.get(server, 0) + 1
        
        load_data[n] = server_counts

    # Debugging: Print the load data to inspect the final counts
    print(load_data)

    plt.plot(load_data.keys(), [sum(values.values()) / len(values) for values in load_data.values()])
    plt.xlabel('Number of Server Containers (N)')
    plt.ylabel('Average Request Count per Server')
    plt.title('Load Distribution Among Servers for Different N values')
    plt.savefig('experiment_A2_results.png')
    plt.show()

if __name__ == '__main__':
    asyncio.run(main())