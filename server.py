import socket
import signal
import sys
import os
from utils import *
from dotenv import load_dotenv

load_dotenv()

proxy_port = int(os.getenv('PROXY_PORT'))
proxy_host = os.getenv('PROXY_HOST')

def send_server_up_notification(port):
    send_message(
        f"SERVER UP:{port}",
        proxy_host,
        proxy_port
    )

def handle_shutdown(host, port):
    print(f'Server at {host}:{port} shutting down')
    send_message(
        f"SERVER DOWN:{port}",
        proxy_host,
        proxy_port
    )

def store_file(data, filename):
  
    try:
        open(filename,"w").write(data)

    except Exception as e:
        print(e)
 

def retrieve_file(client_socket,filename):
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect((proxy_host, proxy_port))
    
    data= open(f"{filename}", "r").read()
    # with open(filename, 'rb') as file:
    #     data = file.read(1024)
    #     while data:
    #         client_socket.send(data)
    #         data = file.read(1024)

    name,ext = filename.split(".")
    message = f"{name}_retrivied_.{ext}/{data}"
    client_socket.send(message.encode())
    client_socket.close()


def process_message(client_socket):
    message = client_socket.recv(1024).decode('utf-8')

    if message.startswith("retrieve"):
        print("RECOVER message received")
        command,filename = message.split("/")

        retrieve_file(client_socket,filename)
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
        filename = message.split("/")[1]
        data = message.split("/")[2]
        store_file(data, filename)
        # if not os.path.exists(filename):
        #     store_file(data, filename)
        # else:
        #     print(f'File {filename} already exists in this server')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg.startswith("PORT="):
            port = int(arg.split("=")[1])
            server_socket = start_server(port)
            send_server_up_notification(port)
        else:
            print("Error: Wrong argument. Use the format 'PORT=port_number'.")
    else:
        print("Error: No given argument.  Use the format 'PORT=port_number'.")

    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    print("Server recognized by proxy")
    while True:
        print("waiting message")
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        process_message(client_socket)
