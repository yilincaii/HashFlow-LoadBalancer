import asyncio
import requests
import matplotlib.pyplot as plt

async def make_requests():
    responses = []
    print("Starting to make 10000 requests...")  # 添加提示
    for i in range(10000):
        if i % 1000 == 0:
            print(f"Progress: {i}/10000")  # 显示进度
        response = requests.get('http://127.0.0.1:5002/rep')
        responses.append(response.json()['message']['replicas'])
    print("Requests completed!")
    return responses

async def main():
    response = await make_requests()
    server_counts = {'Server 1': 0, 'Server 2': 0, 'Server 3': 0}
    
    for servers in response:
        for server in servers:
            server_counts[server] += 1
    
    print(f"\nServer request distribution:")
    for server, count in server_counts.items():
        print(f"  {server}: {count} requests")
    
    plt.bar(server_counts.keys(), server_counts.values())
    plt.xlabel('Server Instance')
    plt.ylabel('Request Count')
    plt.title('Request Distribution Among Server Instances (N=3)')
    plt.savefig('experiment_A1_results.png')
    print("\nGraph saved as: experiment_A1_results.png")
    plt.show()

if __name__ == '__main__':  # ✅ 修复！
    asyncio.run(main())