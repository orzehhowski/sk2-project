import socket

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")
        client_socket.send(b"")

        welcome_mess = client_socket.recv(4096).decode("utf-8")
        print(welcome_mess, end="")
        while True:
            # Get user input for the command to send to the server
            command = input()

            # Send the command to the server
            client_socket.send(command.encode("utf-8"))

            if command.lower() == 'exit':
                break

            # Receive and print the server's response
            response = client_socket.recv(4096).decode("utf-8")
            print(response, end="")

    finally:
        # Close the client socket when done
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    server_ip = '127.0.0.1'
    server_port = 8888

    connect_to_server(server_ip, server_port)
