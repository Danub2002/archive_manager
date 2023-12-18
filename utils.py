import socket
import os
from dotenv import load_dotenv

load_dotenv()

def start_server(port):
    #host = os.getenv('SERVER_HOST')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)  

    print(f"Up and running on '':{port}")

    return server_socket


def send_message(message, address, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, port))
    client_socket.send(message.encode('utf-8')) 
    client_socket.close()