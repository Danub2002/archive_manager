import socket
import threading
import os
from dotenv import load_dotenv

load_dotenv()
class LoadBalancer:
    def __init__(self, host, port):
        self.file_table = {}
        self.server_list = [
            ("", 3030),
            ("", 5001),
            ("", 5002),
            ("", 5003),
            ("", 5004),
        ]
        
        self.host = ''
        self.port = port
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Load Balancer iniciado e escutando em {self.host}:{self.port}")

        while True:

            client_socket, address = server_socket.accept()
            print(f"Conexão estabelecida com {address[0]}:{address[1]}")
            threading.Thread(target=self.handle_client, args=(client_socket,address[0],address[1],)).start()
  
    
    def handle_client(self,client_socket,host,port):
        request = client_socket.recv(1024).decode()

        """ if request.startswith("SERVER"):
            remote_host, remote_port = client_socket.getsockname()

            command = request.split()[1]

            if command == "UP":
                self.server_list.append((host,port))
                print(f"({remote_host},{remote_port}) added to Server List")
            else:
                for server in self.server_list:
                    if server == (host,port):
                        self.server_list.remove(server)
                    
                print(f"({remote_host},{remote_port}) Removed from Server List")    

            return """
        
        command, filename, tolerance, data = request.split("/")

        if command == "deposit":
            self.handle_deposit(filename,int(tolerance),data)
        
        elif command == "retrieve":
            data = self.handle_retrieve(filename)
            client_socket.send(data.encode())
            client_socket.close()
        
  



    def handle_deposit(self, filename, tolerance, data):

        if tolerance-1 > len(self.server_list):
            print("Less servers than replicas")
            return
        
        servers = []
        idx = 0
        while tolerance:
            server_host, server_port =  self.server_list[idx]
            print(server_host, server_port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_host, int(server_port)))

            name,ext = filename.split(".")
            sock.send(f"deposit/{name}_{idx}.{ext}/{data}".encode())

            servers.append(self.server_list[idx]) 

           
            tolerance-=1;idx+=1
            sock.close()

        self.file_table[filename] = servers
        

    def handle_retrieve(self,filename):
        if not self.file_table[filename]:
            print("File Not Found on Any Server")
            return None
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #  Pega o primeiro Server
        server_host,server_port = self.file_table[filename][0]
        sock.connect((server_host,server_port))
        sock.send(f"retrieve/{filename}".encode())

        data = sock.recv(1024).decode()
        sock.close()
        return data
        
    
    def add_server(self, client_sock):
        client_request = client_sock.recv(1024).decode('utf-8')
        print(f"Requisição recebida: {client_request}")
        #server_name = self.choose_server() 
        #self.forward_request(client_request, server_name)
        client_sock.close()
    
if __name__ == "__main__":
    # host = '127.0.0.1'
    # port = 5000
    # host = 127.0.0.1
    host = os.getenv("PROXY_HOST")
    port = int(os.getenv("PROXY_PORT"))
    lb = LoadBalancer(host, port)
    lb.start()