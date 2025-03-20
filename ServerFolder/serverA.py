import socket
import time
import random
import csv

# Automatically determine the server's IP address
host = socket.gethostbyname(socket.gethostname())

# Print the determined IP address
print(f"\n🔹 Server IP Address: {host}")

# Function to create and bind a socket on a given port
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"\n🌍 Server is listening on {host}:{port}...")

    client_socket, client_address = server_socket.accept()
    print(f"✅ Connection established with {client_address} on port {port}")

    return server_socket, client_socket

# Ask user which port to use
print("\nSelect a port for communication:")
print("5000 → Movement Commands")
print("5001 → Telemetry Requests")
print("5002 → Data Transmission")
print("5003 → Error Messages")

port = int(input("\nEnter port number (5000-5003): ").strip())

# Start the server on the chosen port
server_socket, client_socket = start_server(port)

def send_movement_commands(client_socket):
    while True:
        try:
            x = input("\nEnter target X coordinate (or 'exit' to close connection): ").strip()
            if x.lower() == "exit":
                client_socket.send("exit".encode())
                print("\n🚪 Exiting movement mode.")
                break
            
            y = input("Enter target Y coordinate: ").strip()

            # Send coordinates as a comma-separated string
            command = f"{x},{y}"
            client_socket.send(command.encode())

            # Wait for a response from the client
            response = client_socket.recv(1024).decode()
            print(f"\n📡 Client response: {response}")

        except Exception as e:
            print(f"\n⚠️ Error: {e}")
            break

def send_telemetry_request(client_socket):
    while True:
        print("\nSelect telemetry request:")
        print("1 → Battery Telemetry")
        print("2 → Wheel Telemetry")
        print("3 → Thermal Conditions")
        print("4 → Exit")
        
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            client_socket.sendall("Request telemetry data for battery.".encode())
        elif choice == '2':
            client_socket.sendall("Request telemetry data for wheels.".encode())
        elif choice == '3':
            client_socket.sendall("Request telemetry data for thermal conditions.".encode())
        elif choice == '4':
            client_socket.sendall("Exit".encode())
            print("\n🚪 Exiting telemetry mode.")
            break
        else:
            print("\n❌ Invalid choice, please try again.")
            continue

        # Receive and print telemetry response
        data = client_socket.recv(1024).decode()
        print(f"\n📊 Received telemetry data: {data}")


def receive_and_save_data(client_socket):
    print("\n📥 Requesting data...")
    client_socket.sendall("Send data.".encode())

    # Open CSV file for writing received data
    with open("received_data.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                print("\n⚠️ No data received, client may have disconnected.")
                break
            if data == "All data sent.":
                print("\n✅ All data received from client.")
                break

            # Print received data
            print(data.strip())

            # Write received data to CSV file (assuming comma-separated values)
            csv_writer.writerow([data.strip()])

    print("\n📂 Data saved to received_data.csv.")

def send_error_request(client_socket):
    while True:
        print("\nSelect error type to send:")
        print("1 → Hardware Error")
        print("2 → Out of Sight Error")
        print("3 → Exit")
        
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            client_socket.sendall("Request hardware error.".encode())
        elif choice == '2':
            client_socket.sendall("Request out of sight error.".encode())
        elif choice == '3':
            client_socket.sendall("Exit".encode())
            print("\n🚪 Exiting error mode.")
            break
        else:
            print("\n❌ Invalid choice, please try again.")
            continue

        # Receive and print telemetry response
        data = client_socket.recv(1024).decode()
        print(f"\n⚠️ Received error data: {data}")


if port == 5000:  # Movement Commands
    print("\n🚀 Handling movement commands...")
    send_movement_commands(client_socket)

elif port == 5001:  # Telemetry Requests
    print("\n📊 Handling telemetry requests...")
    send_telemetry_request(client_socket)

elif port == 5002:  # Data Transmission
    print("\n📡 Handling data requests...")
    receive_and_save_data(client_socket)

elif port == 5003:  # Error Messages
    print("\n⚠️ Listening for error messages...")
    send_error_request(client_socket)

# Close connections
client_socket.close()
server_socket.close()
print("\n🔴 Server connection closed.")
