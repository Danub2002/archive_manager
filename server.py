import socket

def main():
    # AF_INET => Usa IPV4 ,  SOCK_STREAM => TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server listening for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        

        data = client_socket.recv(1024).decode()

        if not data:
            print("Null Data")
            continue
        

        filename = "output.txt"
        fo = open(filename,"w")
        while data:
            if not data:
                break
            
            fo.write(data)
            data = client_socket.recv(recv).decode()

        client_socket.sendall(b"ACK")
        
        print("File recieved")

if __name__ == "__main__":
    main()
