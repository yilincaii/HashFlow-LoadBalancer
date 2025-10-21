class ConsistentHashMap:
    def __init__(self, N, M, K):
        self.N = N  # Number of server containers managed by the load balancer
        self.M = M  # Total number of slots in the consistent hash map
        self.K = K  # Number of virtual servers for each server container

        self.server_containers = [f'S{i}' for i in range(1, N + 1)]
        self.virtual_servers = self.generate_virtual_servers()

        # Initialize the hash map
        self.hash_map = {slot: None for slot in range(M)}

    def generate_virtual_servers(self):
        virtual_servers = []
        for i in range(1, self.N + 1):
            for j in range(self.K):
                virtual_servers.append(f'S{i}_{j}')
        return virtual_servers

    def h(self, Rid):
        return (Rid + 2 * Rid + 17) % self.M

    def phi(self, Sid, j):
        return (Sid + j + 2 * j + 25) % self.M

    def add_server(self, Sid):
        for j in range(self.K):
            slot = self.phi(Sid, j)
            while self.hash_map[slot] is not None:
                slot = (slot + 1) % self.M
            self.hash_map[slot] = f'S{Sid}_{j}'

    def remove_server(self, Sid):
        for j in range(self.K):
            virtual_server = f'S{Sid}_{j}'
            for slot, value in self.hash_map.items():
                if value == virtual_server:
                    self.hash_map[slot] = None
                    break

    def map_request(self, Rid):
        slot = self.h(Rid)
        while self.hash_map[slot] is None:
            slot = (slot + 1) % self.M
        return self.hash_map[slot]


def main():
    # Initialize Consistent Hash Map
    N = 3  # Number of server containers managed by the load balancer
    M = 512  # Total number of slots in the consistent hash map
    K = 9  # Number of virtual servers for each server container
    chm = ConsistentHashMap(N, M, K)

    # Add servers to the hash map
    for i in range(1, N + 1):
        chm.add_server(i)

    # Map requests to servers
    requests = [132574, 237891, 982345, 674512, 876234, 543289]
    for Rid in requests:
        server = chm.map_request(Rid)
        print(f"Request {Rid} mapped to server {server}")

    # Simulate server failure
    failed_server = 1
    chm.remove_server(failed_server)
    print(f"Server {failed_server} failed")

    # Map requests again after server failure
    for Rid in requests:
        server = chm.map_request(Rid)
        print(f"Request {Rid} mapped to server {server}")


if __name__ == "__main__":
    main()