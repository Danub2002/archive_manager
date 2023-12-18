import socket
import os
from utils import send_message

proxy_port = int(os.getenv("PROXY_PORT"))
proxy_host = os.getenv("PROXY_HOST")
client_host = os.getenv("CLIENT_HOST")
client_port = int(os.getenv("CLIENT_PORT"))


def deposit(filename, tolerance):
  with open(filename, "r") as file:
    data = file.read()    

  message = f'deposit/{filename}/{tolerance}/{data}'
  print(message)
  send_message(message,proxy_host,proxy_port)


def retrieve(filename):
  message = f"retrieve/{filename}"

  client_socket = server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect((proxy_host, proxy_port))

  client_socket.send(message.encode())
  response = client_socket.recv(1024).decode()

  filename,data = response.split("/")
  client_socket.close()


  with open(f"./{filename}","w") as file:
    file.write(data)


while True:
    
  print("Socket Connected to Proxy")

  # Chooses action 
  print("Welcome to the archive manager, choose the operating mode:")
  print("1 - Deposit Mode")
  print("2 - Recovery Mode")
  mode = input()
  filename = input("Enter the file name:")
  

  if mode == "1":
    tolerance = input("Enter Tolerance:")
    deposit(filename,tolerance)
  else:
    retrieve(filename)


  