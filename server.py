import socket
import subprocess
import threading
import os
import pam

# tries to authenticate linux user using pan
def authenticate_user(username, password, id):
    try:
        if pam.authenticate(username, password, service='login'):
            log(id, f"User {username} authenticated successfully")
            return True
        else:
            log(id, f"Authentication failed.")
            return False
    except Exception as e:
        log(id, f"Authentication failed: {e}")
        return False
    
def log(connection_id, message):
    print(f"[{connection_id}] {message}")

# Handles incoming client data and executes commands.
def handle_client(client_socket, id):
    client_socket.send(b"Welcome to the Remote Command Execution Console!\nUsername:\n")
    username = client_socket.recv(1024).decode("utf-8")
    password = ""

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
                if authenticate_user(username, password, id):
                    client_socket.send(f"User {username} authenticated - type command or \"exit\" to terminate connection\n>>>".encode("utf-8"))
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

        # Change directory command
        if command.split(" ")[0] == "cd":
            directory = command[3:]
            try:
                os.chdir(directory)
                response = f"Changed directory to: {os.getcwd()}\n"
            except FileNotFoundError as e:
                response = e.strerror + "\n"

        else:
            try:
                # Execute the command using subprocess
                response = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)

            except subprocess.CalledProcessError as e:
                # If the command execution fails, send the error message
                response = f"Error: {e.output}"

        log(id, f"Command output:\n{response}")

        # Send the command output or error back to the client
        response += ">>> "
        client_socket.send(response.encode("utf-8"))

    # Close the client socket when the connection is terminated
    client_socket.close()
    log(id, "Connection closed.")

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

    connection_num = 1

    while True:
        # Accept a connection from a client
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}. Connection id: {connection_num}")

        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,connection_num))
        client_handler.start()
        connection_num += 1

if __name__ == "__main__":
    start_server()
