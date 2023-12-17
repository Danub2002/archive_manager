import socket
import threading
import random
import time

CENTRAL_SERVER_ADDRESS = ('localhost', 9000)

class CentralServer:
    def __init__(self):
        self.storage_servers = []
        self.file_replication_map = {}
        self.lock = threading.Lock()

    def handle_client(self, client_socket):
        while True:
            request = client_socket.recv(1024).decode()
            if not request:
                break

            if request.startswith('DEPOSIT'):
                self.handle_deposit(request, client_socket)
            elif request.startswith('RECOVERY'):
                self.handle_recovery(request, client_socket)
            elif request.startswith('SET_REPLICAS'):
                self.handle_set_replicas(request, client_socket)

        client_socket.close()

    def handle_deposit(self, request, client_socket):
        _, filename, tolerance = request.split()
        tolerance = int(tolerance)

        with self.lock:
            # Servidores disponíveis são todos os servidores
            available_servers = list(self.storage_servers)
            
            if not available_servers:
                response = "No storage servers available."
                client_socket.send(response.encode())
                return
    
            # Escolhe um servidor aleatório entre todos os servidores disponíveis
            selected_server = random.choice(available_servers)
            # Garante que todas as réplicas são armazenadas no mesmo servidor
            self.file_replication_map[filename] = [selected_server] * tolerance

        response = f"File {filename} deposited successfully on server {selected_server}"
        client_socket.send(response.encode())

    def handle_recovery(self, request, client_socket):
        _, filename = request.split()

        with self.lock:
            server_with_replica = self.file_replication_map.get(filename, [])

        if server_with_replica:
            response = f"File {filename} found on server {server_with_replica}"
        else:
            response = f"File {filename} not found on any server"

        client_socket.send(response.encode())

    def handle_set_replicas(self, request, client_socket):
        _, filename, new_replicas = request.split()
        new_replicas = int(new_replicas)

        with self.lock:
            if filename in self.file_replication_map:
                current_replicas = len(self.file_replication_map[filename])

                if new_replicas > current_replicas:
                    # Adiciona réplicas
                    available_servers = [server for server in self.storage_servers if server not in self.file_replication_map[filename]]
                    additional_servers = random.sample(available_servers, new_replicas - current_replicas)
                    self.file_replication_map[filename].extend(additional_servers)
                elif new_replicas < current_replicas:
                    # Remove réplicas
                    self.file_replication_map[filename] = self.file_replication_map[filename][:new_replicas]

                response = f"Number of replicas for {filename} updated to {new_replicas}"
            else:
                response = f"File {filename} not found"

        client_socket.send(response.encode())

    def run(self):
        central_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        central_server_socket.bind(CENTRAL_SERVER_ADDRESS)
        central_server_socket.listen(5)
        print(f"Central Server listening on {CENTRAL_SERVER_ADDRESS}")

        while True:
            client_socket, addr = central_server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

class StorageServer:
    def __init__(self, address):
        self.address = address
        self.stored_files = {}
        self.lock = threading.Lock()

    def handle_client(self, client_socket):
        while True:
            request = client_socket.recv(1024).decode()
            if not request:
                break

            if request.startswith('REPLICATE'):
                self.handle_replication(request, client_socket)
            elif request.startswith('GET'):
                self.handle_get(request, client_socket)

        client_socket.close()

    def handle_replication(self, request, client_socket):
        _, filename = request.split()
        with self.lock:
            self.stored_files[filename] = True

    def handle_get(self, request, client_socket):
        _, filename = request.split()

        with self.lock:
            if filename in self.stored_files:
                response = f"File {filename} retrieved from {self.address}"
            else:
                response = f"File {filename} not found on {self.address}"

        client_socket.send(response.encode())

    def run(self):
        storage_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        storage_server_socket.bind(self.address)
        storage_server_socket.listen(5)
        print(f"Storage Server {self.address} listening")

        while True:
            client_socket, addr = storage_server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

class Proxy:
    def __init__(self, storage_servers):
        self.central_server_address = CENTRAL_SERVER_ADDRESS
        self.proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.proxy_socket.bind(('localhost', 9102))
        self.proxy_socket.listen(5)
        self.storage_servers = storage_servers
        print(f"Proxy listening on ('localhost', 9102)")

    def create_storage_servers(self):
        server_count = int(input("Enter the number of storage servers to create: "))
        for i in range(server_count):
            address = input(f"Enter address for storage server {i + 1} (e.g., 'localhost:9100'): ")
            self.storage_servers.append(tuple(address.split(':')))
            
    def run(self):
        while True:
            client_socket, addr = self.proxy_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        request = client_socket.recv(1024).decode()
        if request.startswith('DEPOSIT') or request.startswith('RECOVERY') or request.startswith('SET_REPLICAS'):
            self.forward_to_central_server(request, client_socket)

    def forward_to_central_server(self, request, client_socket):
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.connect(self.central_server_address)
        proxy_socket.send(request.encode())
        response = proxy_socket.recv(1024).decode()
        client_socket.send(response.encode())
        proxy_socket.close()

class Client:
    def __init__(self, address):
        self.address = address
        self.stored_files = {}
        self.lock = threading.Lock()
        self.proxy_address = ('localhost', 9000)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.proxy_address)

    def deposit(self, filename, tolerance):
        request = f"DEPOSIT {filename} {tolerance}"
        self.client_socket.send(request.encode())
        response = self.client_socket.recv(1024).decode()
        print(response)

    def recover(self, filename):
        request = f"RECOVERY {filename}"
        self.client_socket.send(request.encode())
        response = self.client_socket.recv(1024).decode()
        print(response)

    def set_replicas(self, filename, new_replicas):
        request = f"SET_REPLICAS {filename} {new_replicas}"
        self.client_socket.send(request.encode())
        response = self.client_socket.recv(1024).decode()
        print(response)

    def close(self):
        self.client_socket.close()

if __name__ == "__main__":
    central_server = CentralServer()
    central_server_thread = threading.Thread(target=central_server.run)

    proxy = Proxy(central_server.storage_servers)
    proxy.create_storage_servers()
    proxy_thread = threading.Thread(target=proxy.run)

    central_server_thread.start()
    proxy_thread.start()

    number_clients = int(input("Enter the number of clients: "))
    clients = []
    for i in range(number_clients):
        address = input(f"Enter address for client {i + 1} (e.g., 'localhost:9100'): ")
        client = Client(address)
        clients.append(client)

    time.sleep(2)  # Wait for servers and proxy to start

    for client in clients:
        while True:
            command = input(f"Enter command for {client.address} (e.g., deposit, recover, set_replicas, sair): ").lower()

            if command == 'sair':
                break
            elif command == 'deposit':
                filename = input("Enter filename: ")
                tolerance = int(input("Enter tolerance: "))
                client.deposit(filename, tolerance)
            elif command == 'recover':
                filename = input("Enter filename: ")
                client.recover(filename)
            elif command == 'set_replicas':
                filename = input("Enter filename: ")
                new_replicas = int(input("Enter new replicas count: "))
                client.set_replicas(filename, new_replicas)
            else:
                print("Invalid command. Try again.")

    for client in clients:
        client.close()

    central_server_thread.join()
    proxy_thread.join()