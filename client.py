import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    while True:

        try:
            filename = "teste.txt"
            fi = open(filename,"r")

            data = fi.read()

            if not data:
                break

            while data:
                client_socket.send(str(data).encode())
                
                data= fi.read()
                
            print("File sent")
            fi.close()
        
        except IOError:
            print("Filename Not Found")

if __name__ == "__main__":
    main()
