import socket
import time
import random

# Define the server host and port
HOST = '10.0.0.59'  # Localhost (loopback) for the same machine
PORT = 12334        # Port to bind to

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen(1)
print("Server is waiting for a connection...")

# Accept a connection from the client
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

# Receive the initial data from the client
data = client_socket.recv(1024)
print(f"Received from client: {data.decode()}")

# Send a response back to the client
client_socket.sendall("Connection established Earth Server 04!".encode())

# Simulate random latency (1 to 3 seconds)
def simulate_latency():
    delay = random.uniform(1, 3)  # Random delay between 1 and 3 seconds
    time.sleep(delay)

# Function to simulate packet loss (10% chance of packet loss)
def simulate_packet_loss():
    return random.random() > 0.1  # 90% chance of not dropping the packet

# Start the communication loop
while True:
    # Ask for user input on what to do
    print("\nWhat would you like the rover to do?")
    print("1. Move")
    print("2. Send Data")
    print("3. Close Connection")

    command = input("Enter choice (move/send data/close connection): ").strip().lower()

    if command == "move":
        # Simulate latency before sending move request
        simulate_latency()
        # Send move request to the client
        client_socket.sendall("Please move to a new location.".encode())

        # Receive response from the client (simulate latency)
        simulate_latency()

       # Client informs that it has moved
        response = client_socket.recv(1024)
        if simulate_packet_loss():  # Simulate packet loss here
            print(f"Client response: {response.decode()}")
        else:
            print("Packet lost, no response from client.")


        # Wait for a few seconds to simulate moving
        time.sleep(3)
        
        simulate_latency()
        # Client informs that it has moved
        response = client_socket.recv(1024)
        if simulate_packet_loss():  # Simulate packet loss here
            print(f"Client response: {response.decode()}")
        else:
            print("Packet lost, no response from client.")

    elif command == "send data":
        # Ask the user for the error scenario they want to simulate
        print("\nSelect simulation scenario before sending data:")
        print("1. Without Errors")
        print("2. Hardware Error")
        print("3. Out of Sight")

        option = input("Enter choice (1/2/3): ").strip()

        # Simulate latency before asking the client to send data
        simulate_latency()
        # Send the option to the client
        client_socket.sendall(option.encode())

        #  Receive and print data from the client line by line
        while True:
            #simulate_latency()
            data = client_socket.recv(1024).decode()
            #if simulate_packet_loss():  # Simulate packet loss here
            if data == "All data sent.":
                print("All data received from client.")
                break
            else:
                print(f"{data.strip()}")
            #else:
                #print("Packet lost, skipping this packet.")


    elif command == "close connection":
        simulate_latency()
        # Close the connection to the client and server
        print("Closing connection.")
        client_socket.sendall("Server is closing the connection.".encode())
        break

    else:
        print("Invalid command. Please type 'move', 'send data', or 'close connection'.")

# Close the client and server sockets
client_socket.close()
server_socket.close()
