import socket 
import time 
import random 
import csv
import pyfiglet
from colorama import Fore,init
from rich.console import Console 


init(autoreset=True)
console=Console()
print(Fore.GREEN+ pyfiglet.figlet_format("EARTH STATION"))

#host = socket.gethostbyname(socket.gethostname()) # Get devices IP address #### Uncomment #### 
# Print the determined IP address
#print(f"\n🔹 Server IP Address: {host}") #### Uncomment ####

# Function to create and bind a socket on a given port of our choice
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create server socket using IPv4 and TCP
    server_socket.bind(("localhost", port)) # Binding to port and choosen device IP ######## CHANGE TO IP ###########
    server_socket.listen(1) # Listening to any connections
    print(f"\n🌍Earth Computer04 is listening on port {port}...")

    client_socket, client_address = server_socket.accept() # Wait for client to connect
    print(f"✅Connection established with {client_address} on port {port}")

    return server_socket, client_socket # Returns the connection

# START:
 # Earth Computer Welcome message

# Ask user which port to use
print("\nSelect a port for communication:")
print("5000 → Movement Commands")
print("5001 → Telemetry Requests")
print("5002 → Data Transmission")
print("5003 → Error Messages")
print("5004 → Discover Nearby Rovers")
print("5005 - Group Communication")
port = int(input("\nEnter port number (5000-5005): ").strip())

# Start the server on the chosen port
server_socket, client_socket = start_server(port)

# Function for Movement Port to request certain coordinates to rover
def send_movement_commands(client_socket):
    while True:
        try:
            x = input("\nEnter target X coordinate (or 'exit' to close connection): ").strip()
            if x.lower() == "exit":
                client_socket.send("exit".encode())
                print("\n🚪Exiting movement mode.")
                break
            
            y = input("Enter target Y coordinate: ").strip()

            command = f"{x},{y}" 
            client_socket.send(command.encode()) # Send coordinates as a comma-separated string
            time.sleep(random.uniform(1.0, 2.0)) # Random delay between 1 and 2 seconds (simulation)

            # Wait for a response from the client
            response = client_socket.recv(1024).decode()
            time.sleep(random.uniform(1.0, 2.0))
            print(f"\n📡Client response: {response}")

        except Exception as e:
            print(f"\n⚠️Error: {e}")
            break

# Function for Telemetry Port to request certain telemetry data to rover
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
            print("\n🚪Exiting telemetry mode.")
            break
        else:
            print("\n❌Invalid choice, please try again.")
            continue

        # Receive and print telemetry response
        time.sleep(random.uniform(1.0, 2.0))
        data = client_socket.recv(1024).decode()
        print(f"\n📊Received telemetry data: {data}")

# Function for Data Port to request certain temperature data to rover
def receive_and_save_data(client_socket):
    print("\n📥Requesting data...")
    client_socket.sendall("Send data.".encode())

    # Create a new csv file for writing received data
    with open("received_data.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)

        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    print("\n⚠️No data received, client may have disconnected.")
                    break
                if data == "All data sent.":
                    print("\n✅All data received from client.")
                    break

                print(data.strip()) # Print every line of received data 
                time.sleep(random.uniform(1.0, 2.0))
                csv_writer.writerow([data.strip()]) # Write received data to CSV file

            except Exception as e:
                print(f"\nError while receiving data: {e}")
                break

    print("\n📂Data saved to received_data.csv.")

def send_error_request(client_socket):
     while True:
        # Choose error simulation type
        print("\nSelect error simulation type:")
        print("1 → Hardware Error")
        print("2 → Out of Sight Error")
        print("3 → Exit")
        
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            client_socket.sendall("Request hardware error.".encode())
            time.sleep(random.uniform(1.0, 2.0))
            data = client_socket.recv(1024).decode()
            print(f"\n {data}")
            handle_hardware_error(client_socket) # Call function for hardware error handling
            break
        elif choice == '2':
            client_socket.sendall("Request out of sight error.".encode())
            time.sleep(random.uniform(1.0, 2.0))
            data = client_socket.recv(1024).decode()
            print(f"\n {data}")
            handle_out_of_sight_error(client_socket) # Call function for out of sight error handling
            break
        elif choice == '3':
            client_socket.sendall("Exit".encode())
            print("\n🚪Exiting telemetry mode.")
            break
        else:
            print("\n❌Invalid choice, please try again.")
            continue

def handle_hardware_error(client_socket):
    print("\nSelect action to handle hardware error:")
    print("1 → Stop rover's operations and notify Head Department")
    print("2 → Use backup sensor and continue operations")

    choice = input("Enter your choice (1-2): ").strip()

    if choice == '1': # Stop rover operations and notify head department
        message = "Rover has stopped due to a hardware error. Head Department notified."
        client_socket.sendall(message.encode())

        print("\nStopping rover and sending notification to Head Department...")
        
        time.sleep(3) # Simulating the stop action
        
        print("\n🛑Rover stopped. Awaiting further instructions from the Head Department.")
        
        
    elif choice == '2': # Use backup sensor and continue operation
        message = "Backup sensor activated. Rover continues operation."
        client_socket.sendall(message.encode())

        time.sleep(3)

        print("\n🛰️Backup sensor activated. Rover continues operation.")
        
    else:
        print("\n❌Invalid choice. Please select a valid action.")
        handle_hardware_error(client_socket)  # Recursive call to handle error again

def handle_out_of_sight_error(client_socket):
    print("\nSelect action to handle out of sight error:")
    print("1 → Stop rover's operations and notify Head Department")
    print("2 → Get Rovers coordinates")

    choice = input("Enter your choice (1-2): ").strip()

    if choice == '1': # Stop rover operations and notify head department
        message = "Rover is out of sight. Head Department notified."
        client_socket.sendall(message.encode())

        print("\nStopping rover and sending notification to Head Department...")

        time.sleep(3)
    
        print("\n🛑Rover stopped. Awaiting further instructions from the Head Department.")

        
    elif choice == '2': # Ask for coordinates to know rovers location
        message = "Rovers Coordinations Request."
        client_socket.sendall(message.encode())

        time.sleep(3)

        print("\nRovers Coordinations Requested.")
       
        coordinates = client_socket.recv(1024).decode()

        print(f"\n📍Rover Coordinates: {coordinates}")

    else:
        print("\n❌Invalid choice. Please select a valid action.")
        handle_out_of_sight_error(client_socket)  # Recursive call to handle error again
        
def send_discovery_request(client_socket):
    while True:
        choice = input("\nEnter 'Discover nearby devices' to discover or 'Exit' to quit: ").strip()

        if choice == 'Discover nearby devices': # Want to discover nearby lunar devices
            print("\nᯤRequesting rover to discover nearby devices...")
            client_socket.sendall("Nearby discovery.".encode())

            nearby_rovers_message = client_socket.recv(1024).decode() # List of nearby rovers found
            #print(f"\nReceived from rover: {nearby_rovers_message}")

            # User can choose a rover from the discovered rovers to connect to (simulation)
            nearby_rovers = nearby_rovers_message.split(": ")[1].split(", ")
            print(f"\n🤖Nearby rovers found: {', '.join(nearby_rovers)}")
            chosen_rover = input("\nChoose a rover to connect to: ").strip()

            client_socket.sendall(chosen_rover.encode())

            connection_response = client_socket.recv(1024).decode()
            #print(f"\nRover response: {connection_response}")

            if "Connecting to" in connection_response:
                    print(f"\nConnection established with {chosen_rover}.")
            else:
                    print(f"\nFailed to connect to {chosen_rover}. Please check the rover selection.")
            
        elif choice == 'Exit':
            client_socket.sendall("Exit".encode())
            print("\n🚪Exiting discovery mode.")
            break
            
        else:
            print("\n❌Invalid choice. Please select a valid action.")
            handle_hardware_error(client_socket)  # Error handling for invalid input


# Close connections

def group_rover(client_socket):
        while True:
            command = input("\nEnter 'Status' to get group rover data or 'Exit' to quit: ").strip()
            if command.lower() == "exit":
                client_socket.sendall("Exit".encode())
                print("\n🚪 Exiting group rover mode.")
                break
            elif command.lower() == "status":
                client_socket.sendall("Status".encode())
                time.sleep(random.uniform(1.0, 2.0))
                response = client_socket.recv(1024).decode()
                print(f"\n📡 Received response: {response}")
            else:
                print("\n❌ Invalid choice. Try again.")



if port == 5000:  # Movement Commands
        print("\n🚀Handling movement commands...")
        send_movement_commands(client_socket)

elif port == 5001:  # Telemetry Requests
        print("\n📊Handling telemetry requests...")
        send_telemetry_request(client_socket)

elif port == 5002:  # Data Transmission
        print("\n📡Handling data requests...")
        receive_and_save_data(client_socket)

elif port == 5003:  # Error Messages
        print("\n⚠Listening for error messages...")
        send_error_request(client_socket)

elif port == 5004:  # Rover discovery
        print("\n🤖Listening for nearby lunar devices...")
        send_discovery_request(client_socket)
elif port == 5005:
        print("\n🤖 Handling group rover communication...")
        group_rover(client_socket)

    # Close connections
client_socket.close()
server_socket.close()
print("\n🔴Server connection closed.")


    