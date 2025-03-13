import socket
import time

# Define the server host and port (same as server-side)
HOST = '10.0.0.59'  # Localhost (loopback) for the same machine
PORT = 12334        # Port where the server is listening

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Send the initial connection message to the server
client_socket.sendall("Connection established with Lunar Rover 04".encode())

# Receive the initial response from the server
response = client_socket.recv(1024)
print(f"Received from server: {response.decode()}")

# Keep the connection open until the server closes it
while True:
    # Receive command from the server (for moving, etc.)
    command = client_socket.recv(1024).decode()

    if command == "Please move to a new location.":
        print("Server says: Please move to a new location.")
        # Respond with "moving"
        client_socket.sendall("moving".encode())
        print("Sent 'moving' to server.")

        # Wait for a few seconds to simulate the movement
        time.sleep(3)

        # Send confirmation back to the server
        client_socket.sendall("Moved to a new location.".encode())
        print("Sent 'Moved to a new location.' to server.")

    elif command == "1":
        print("Server asks to send data1.")
        
        # Open the CSV file and send it line by line with a delay
        try:
            with open("data_dummy1.csv", 'r') as file:
                for line in file:
                    # Send each line to the server
                    client_socket.sendall(line.encode())

                    # Wait for 1 second before sending the next line
                    time.sleep(1)

            # After sending all lines, notify the server
            client_socket.sendall("All data sent.".encode())
            print("All data sent.")
            
        except FileNotFoundError:
            print("CSV file not found.")

    elif command == "2":
        print("Server asks to send data2.")
        
        # Open the CSV file and send it line by line with a delay
        try:
            with open("data_dummy2.csv", 'r') as file:
                for line in file:
                    # Send each line to the server
                    client_socket.sendall(line.encode())

                    # Wait for 1 second before sending the next line
                    time.sleep(1)

            # After sending all lines, notify the server
            client_socket.sendall("All data sent.".encode())
            print("All data sent.")
            
        except FileNotFoundError:
            print("CSV file not found.")

    elif command == "3":
        print("Server asks to send data3.")

        # Open the CSV file and send it line by line with a delay
        try:
            with open("data_dummy3.csv", 'r') as file:
                for line in file:
                    # Send each line to the server
                    client_socket.sendall(line.encode())

                    # Wait for 1 second before sending the next line
                    time.sleep(1)

            # After sending all lines, notify the server
            client_socket.sendall("All data sent.".encode())
            print("All data sent.")
            
        except FileNotFoundError:
            print("CSV file not found.")

    elif command == "Server is closing the connection.":
        print("Server is closing the connection.")
        break

# Close the client socket
client_socket.close()
