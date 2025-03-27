# Function to authenticate the client
def authenticate(client_socket):
    # Define the correct password
    correct_password = "securepassword123"
    
    # Receive the password from the server
    server_password = client_socket.recv(1024).decode()

    if server_password == correct_password:
        # If password is correct, send a confirmation
        client_socket.send("Password correct".encode())
        print("\n🔑 Authentication successful.")
        return True
    else:
        # If password is incorrect, send failure response
        client_socket.send("Invalid password".encode())
        print("\n❌ Authentication failed.")
        return False