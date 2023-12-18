import socket
import signal
import sys
import os
from utils import *

from dotenv import load_dotenv

load_dotenv()

servers_ports=(3030, 5001, 5002, 5003, 5004)
proxy_port = int(os.getenv('PROXY_PORT'))
proxy_host = os.getenv('PROXY_HOST')

""" def send_server_up_notification():
    send_message(
        "SERVER UP",
        proxy_host,
        proxy_port
    )

def handle_shutdown(host, port):
    print(f'Server at {host}:{port} shutting down')
    send_message(
        "SERVER DOWN",
        proxy_host,
        proxy_port
    ) """

def store_file(client_socket, filename):
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)


def retrieve_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((proxy_host, proxy_port))

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)

    client_socket.close()


def process_message(client_socket):
    message = client_socket.recv(1024).decode('utf-8')

    if message.startswith("retrieve"):
        print("RECOVER message received")
        filename = message.split(' ')[1].split('.')[0]

        retrieve_file(filename+"-processed.txt")
        print(f"Recovering file: {filename}")
        print("\nRelaying file to proxy...")

    elif message.startswith("DELETE"):
        filename = message.split(" ")[1]
        if os.path.exists(filename):
            os.remove(filename)
            print(f"The file '{filename}' has been deleted.")
        else:
            print(f"The file '{filename}' does not exist on this server.")
    elif message.startswith("deposit"):
        filename = message.split(" ")[1]
        if not os.path.exists(filename):
            store_file(client_socket, filename)
        else:
            print(f'File {filename} already exists in this server')

if __name__ == "__main__":
    """ if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg.startswith("PORT="):
            port = int(arg.split("=")[1])
            server_socket = start_server(port)
            send_server_up_notification()
        else:
            print("Error: Wrong argument. Use the format 'PORT=port_number'.")
    else:
        print("Error: No given argument.  Use the format 'PORT=port_number'.")

    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown) """
    
    """ for server_port in servers_ports:
        server_socket = start_server(server_port)
        print(f'server up and running at localhost:{server_port}') """
    
    server_socket = start_server(servers_ports[0])
    print(f'server up and running at localhost:{servers_ports[0]}')

    #print("Server recognized by proxy")
    while True:
        
        print("waiting message")
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        process_message(client_socket)
