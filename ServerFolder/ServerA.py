import socket
import time
import random
import csv

# Function to create and bind a socket on a given port
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", port))
    server_socket.listen(1)
    print(f"\nServer is listening on port {port}...")

    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address} on port {port}")

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
                print("\nExiting movement mode.")
                break
            
            y = input("Enter target Y coordinate: ").strip()

            # Send coordinates as a comma-separated string
            command = f"{x},{y}"
            client_socket.send(command.encode())
            time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)

            # Wait for a response from the client
            response = client_socket.recv(1024).decode()
            time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
            print(f"\nClient response: {response}")

        except Exception as e:
            print(f"\nError: {e}")
            break

def send_telemetry_request(client_socket):
    while True:
        # Ask the user what telemetry data they want
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
            print("\nExiting telemetry mode.")
            break
        else:
            print("\nInvalid choice, please try again.")
            continue

        # Receive and print telemetry response
        time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
        data = client_socket.recv(1024).decode()
        print(f"\nReceived telemetry data: {data}")


def receive_and_save_data(client_socket):
    print("\nRequesting data...")
    client_socket.sendall("Send data.".encode())

    # Open CSV file for writing received data
    with open("received_data.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)

        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    print("\nNo data received, client may have disconnected.")
                    break
                if data == "All data sent.":
                    print("\nAll data received from client.")
                    break

                # Print received data
                print(data.strip())

                # Introduce a random delay between receiving each line
                time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds

                # Write received data to CSV file (assuming comma-separated values)
                csv_writer.writerow([data.strip()])

            except Exception as e:
                print(f"\nError while receiving data: {e}")
                break

    print("\nData saved to received_data.csv.")

def send_error_request(client_socket):
     while True:
        # Ask the user what telemetry data they want
        # Choose error type
        print("\nSelect error simulation type:")
        print("1 → Hardware Error")
        print("2 → Out of Sight Error")
        print("3 → Exit")
        
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            client_socket.sendall("Request hardware error.".encode())
            time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
            data = client_socket.recv(1024).decode()
            print(f"\n {data}")
            handle_hardware_error(client_socket)  # Handle hardware error
            break
        elif choice == '2':
            client_socket.sendall("Request out of sight error.".encode())
            time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
            data = client_socket.recv(1024).decode()
            print(f"\n {data}")
            handle_out_of_sight_error(client_socket)  # Handle out of sight error
            break
        elif choice == '3':
            client_socket.sendall("Exit".encode())
            print("\nExiting telemetry mode.")
            break
        else:
            print("\nInvalid choice, please try again.")
            continue

def handle_hardware_error(client_socket):
    print("\nSelect action to handle hardware error:")
    print("1 → Stop rover's operations and notify Head Department")
    print("2 → Use backup sensor and continue operations")

    choice = input("Enter your choice (1-2): ").strip()

    if choice == '1':
        # Stop rover operations and notify head department
        message = "Rover has stopped due to a hardware error. Head Department notified."
        client_socket.sendall(message.encode())
        print("\nStopping rover and sending notification to Head Department...")

        # Here, you can simulate sending a message to a real department (e.g., via an email API or other messaging system).
        # Simulating the stop action:
        time.sleep(3)
        #  - Disable rover functionality
        print("\nRover stopped. Awaiting further instructions from the Head Department.")
        # This might include disabling movement, sensors, etc., depending on your setup.
        
    elif choice == '2':
        # Use backup sensor and continue operation
        message = "Backup sensor activated. Rover continues operation."
        client_socket.sendall(message.encode())
        time.sleep(3)
        print("\nBackup sensor activated. Rover continues operation.")
        # Simulate activation of a backup sensor here, or continue the rover with limited functionality.
    else:
        print("\nInvalid choice. Please select a valid action.")
        handle_hardware_error(client_socket)  # Recursive call to handle error again

def handle_out_of_sight_error(client_socket):
    print("\nSelect action to handle out of sight error:")
    print("1 → Stop rover's operations and notify Head Department")
    print("2 → Get Rovers coordinates")

    choice = input("Enter your choice (1-2): ").strip()

    if choice == '1':
        # Stop rover operations and notify head department
        message = "Rover is out of sight. Head Department notified."
        client_socket.sendall(message.encode())
        print("\nStopping rover and sending notification to Head Department...")

        # Simulating the stop action:
        time.sleep(3)
        #  - Disable rover functionality
        print("\nRover stopped. Awaiting further instructions from the Head Department.")
        # This might include disabling movement, sensors, etc., depending on your setup.
        
    elif choice == '2':
        # Use backup sensor and continue operation
        message = "Rovers Coordinations Request."
        client_socket.sendall(message.encode())
        time.sleep(3)
        print("\nRovers Coordinations Requested.")
        # Simulate activation of a backup sensor here, or continue the rover with limited functionality.
         # Receive and print telemetry response
        coordinates = client_socket.recv(1024).decode()
        print(f"\nRover Coordinates: {coordinates}")
    else:
        print("\nInvalid choice. Please select a valid action.")
        handle_out_of_sight_error(client_socket)  # Recursive call to handle error again


if port == 5000:  # Movement Commands
    print("\nHandling movement commands...")
    send_movement_commands(client_socket)

elif port == 5001:  # Telemetry Requests
    print("\nHandling telemetry requests...")
    send_telemetry_request(client_socket)

elif port == 5002:  # Data Transmission
    print("\nHandling data requests...")
    receive_and_save_data(client_socket)

elif port == 5003:  # Error Messages
    print("\nListening for error messages...")
    send_error_request(client_socket)

# Close connections
client_socket.close()
server_socket.close()
print("\nServer connection closed.")
