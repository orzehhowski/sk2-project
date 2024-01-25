import socket
import subprocess
import threading
import pam
from pexpect import spawn, EOF

# tries to authenticate linux user using pan
def authenticate_user(username, password):
    try:
        if pam.authenticate(username, password, service='login'):
            print(f"User {username} authenticated successfully")
            return True
        else:
            print(f"Authentication failed.")
            return False
    except Exception as e:
        print(f"Authentication failed: {e}")
        return False

# Handles incoming client data and executes commands.
def handle_client(client_socket):
    client_socket.send(b"Welcome to the Remote Command Execution Console!\nUsername:\n")
    username = client_socket.recv(1024).decode("utf-8")

    # authentication loop
    while True:
        if not username:
            client_socket.send(b"authentication failed. Try again\nUsername:\n")
        else:
            client_socket.send(b"Password:\n")
            password = client_socket.recv(1024).decode("utf-8")
            if not password:
                client_socket.send(b"authentication failed. Try again\nUsername:\n")
            else:
                if authenticate_user(username, password):
                    client_socket.send(f"User {username} authenticated\n>>>".encode("utf-8"))
                    break
                else:
                    client_socket.send(b"authentication failed. Try again\nUsername:\n")
        username = client_socket.recv(1024).decode("utf-8")

    # remote console loop
    while True:
        # Receive command from the client
        command = client_socket.recv(1024).decode("utf-8")
        if (not command) or command == "exit":
            break

        try:
            # Execute the command using subprocess
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            response = result
        except subprocess.CalledProcessError as e:
            # If the command execution fails, send the error message
            response = f"Error: {e.output}"

        # Send the command output or error back to the client
        response += ">>> "
        client_socket.send(response.encode("utf-8"))

    # Close the client socket when the connection is terminated
    client_socket.close()

def start_server():
    # Define the host and port to bind the server to
    host = '127.0.0.1'
    port = 8888

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified address and port
    server_socket.bind((host, port))

    # Listen for incoming connections (up to 5 connections in the queue)
    server_socket.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        # Accept a connection from a client
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()