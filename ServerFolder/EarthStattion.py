import socket 
import time 
import random 
import csv
import pyfiglet
from colorama import Fore,init
from rich.console import Console 


welcome_message = """
███████╗ █████╗ ██████╗ ████████╗██╗  ██╗         █████╗ ██╗  ██╗
██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║  ██║        ██╔══██╗██║  ██║
██████╗ ███████║██████╔╝   ██║   ███████║        ██║  ██║███████║
██╔════╗██╔══██║██╔██╗     ██║   ██╔══██║        ██║  ██║╚════██║
███████╗██║  ██║██║╚██╗    ██║   ██║  ██║         █████╔╝     ██║
╚══════╝╚═╝  ╚═╝╚═╝ ╚═╝    ╚═╝   ╚═╝  ╚═╝         ╚════╝      ╚═╝
"""
local_password = "Group04"

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
    print(f"Connection established with {client_address} on port {port}")

    return server_socket, client_socket # Returns the connection

# START:
print(welcome_message) # Earth Computer Welcome message
init(autoreset=True)
console=Console()
print(Fore.GREEN+ pyfiglet.figlet_format("EARTH STATION"))


# Ask user which port to use
print("\nSelect a port for communication:")
print("5000 → Movement Commands")
print("5001 → Telemetry Requests")
print("5002 → Data Transmission")
print("5003 → Error Messages")
print("5004 → Discover Nearby Rovers")
print("5005 - Group Communication")
port = int(input("\nEnter port number (5000-5005): ").strip())

# Ask the user to input the password
password_input = input("\nPlease enter your password: ")
# Check if user input is correct password
if password_input == local_password:
    print("Correct Password\n")
    # Start the server on the chosen port
    server_socket, client_socket = start_server(port)
    
    #client_socket.close()  # Close the client socket after use
    #server_socket.close()  # Close the server socket after use
    #print("\nServer connection closed.")
else:
    print("Incorrect Password\n")

# Start the server on the chosen port
#server_socket, client_socket = start_server(port)


# Function to receive data from rover with an specific timeout and retries
def receive_with_timeout(client_socket, timeout, retries):
    client_socket.settimeout(timeout) # Sets timeout for socket connection
    attempt = 0 # Tracks attempts made to get data
    while attempt < retries: # Loop until reaches specified amount of retries
        try:
            data = client_socket.recv(1024).decode() # Answer from rover
            if data:
                return data
        except socket.timeout: # If not data is received before timout:
            attempt += 1
            print(f"⚠️ Timeout after {timeout}s. Retrying... ({attempt}/{retries})")
    print("❌ Failed to receive data after multiple retries.")
    return None


# Function for Movement Port 5000 to request certain coordinates to rover
def send_movement_commands(client_socket):
    while True:
        try:
            x = input("\nEnter target X coordinate (or 'exit' to close connection): ").strip()
            if x.lower() == "exit":
                client_socket.send("exit".encode())
                print("\nExiting movement mode.")
                break
            
            y = input("Enter target Y coordinate: ").strip()

            command = f"{x},{y}" 
            client_socket.send(command.encode()) # Send coordinates as a comma-separated string
            time.sleep(random.uniform(1.0, 2.0)) # Random delay between 1 and 2 seconds (simulation)

            # Wait for a response from the client
            response = receive_with_timeout(client_socket, 10, 1)
            time.sleep(random.uniform(1.0, 2.0))
            if response:
                print(f"\nClient response: {response}")
            else:
                print("\n⚠️No response from rover. Exiting movement mode.")
                break

        except Exception as e:
            print(f"\n⚠️Error: {e}")
            break


# Function for Telemetry Port 5001 to request certain telemetry data to rover
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
            print("\n❌Invalid choice, please try again.")
            continue

        # Receive and print telemetry response
        time.sleep(random.uniform(1.0, 2.0))
        data = receive_with_timeout(client_socket, 10, 1)
        if data:
            print(f"\nReceived telemetry data: {data}")
        else:
            print("\n⚠️ Timeout occurred while receiving telemetry data.")


# Function for Data Port 5002 to request certain temperature data to rover
def receive_and_save_data(client_socket):
    print("\n📥Requesting data...")
    client_socket.sendall("Send data.".encode())

    # Create a new csv file for writing received data
    with open("received_data.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)

        while True:
            try:
                data = receive_with_timeout(client_socket, 300, 1)
                if data: 
                   if data == "All data sent.":
                      print("\nAll data received from client.")
                      break
                   
                   print(data.strip()) # Print every line of received data 
                  # time.sleep(random.uniform(1.0, 2.0))
                   csv_writer.writerow([data.strip()]) # Write received data to CSV file
                else:
                    print("\n⚠️No data received within the timeout. Closing data reception.")
                    break

            except Exception as e:
                print(f"\nError while receiving data: {e}")
                break

    print("\n📂Data saved to received_data.csv.")


# Function for Error Port 5003 to simulate error scenarios
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
            data = receive_with_timeout(client_socket, 10, 1)
            if data:
               print(f"\n {data}")
               handle_hardware_error(client_socket) # Call function for hardware error handling
            break
        elif choice == '2':
            client_socket.sendall("Request out of sight error.".encode())
            time.sleep(random.uniform(1.0, 2.0))
            data = receive_with_timeout(client_socket, 10, 1)
            if data:
               print(f"\n {data}")
               handle_out_of_sight_error(client_socket) # Call function for out of sight error handling
            break
        elif choice == '3':
            client_socket.sendall("Exit".encode())
            print("\nExiting telemetry mode.")
            break
        else:
            print("\n❌Invalid choice, please try again.")
            continue

# Function for hardware (sensors) error simulation
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
        
        print("\nRover stopped. Awaiting further instructions from the Head Department.")
        
        
    elif choice == '2': # Use backup sensor and continue operation
        message = "Backup sensor activated. Rover continues operation."
        client_socket.sendall(message.encode())

        time.sleep(3)

        print("\nBackup sensor activated. Rover continues operation.")
        
    else:
        print("\n❌Invalid choice. Please select a valid action.")
        handle_hardware_error(client_socket)  # Recursive call to handle error again

# Function for rover out of sight error simulation
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
    
        print("\nRover stopped. Awaiting further instructions from the Head Department.")

        
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
        

# Function for Discovery Port 5004 to simulate discovering nearby rovers
def send_discovery_request(client_socket):
    while True:
        choice = input("\nEnter 'Discover nearby devices' to discover or 'Exit' to quit: ").strip()

        if choice == 'Discover nearby devices': # Want to discover nearby lunar devices
            print("\nRequesting rover to discover nearby devices...")
            client_socket.sendall("Nearby discovery.".encode())

            nearby_rovers_message = receive_with_timeout(client_socket, 10, 1) # List of nearby rovers found
            #print(f"\nReceived from rover: {nearby_rovers_message}")
            
            if nearby_rovers_message:
               # User can choose a rover from the discovered rovers to connect to (simulation)
               nearby_rovers = nearby_rovers_message.split(": ")[1].split(", ")
               print(f"\n🤖Nearby rovers found: {', '.join(nearby_rovers)}")
               chosen_rover = input("\nChoose a rover to connect to: ").strip()

               client_socket.sendall(chosen_rover.encode())

               connection_response = receive_with_timeout(client_socket, 10, 1) 
               #print(f"\nRover response: {connection_response}")
               if connection_response:
                  if "Connecting to" in connection_response:
                       print(f"\nConnection established with {chosen_rover}.")
                  else:
                       print(f"\nFailed to connect to {chosen_rover}. Please check the rover selection.")
               else: 
                    print("\n⚠️ Timeout occurred while receiving rover connection data.")
            else: 
                print("\n⚠️ Timeout occurred while receiving discovery data.")

        elif choice == 'Exit':
            client_socket.sendall("Exit".encode())
            print("\nExiting discovery mode.")
            break
            
        else:
            print("\n❌Invalid choice. Please select a valid action.")
            handle_hardware_error(client_socket)  # Error handling for invalid input


# Function for Grooup Port 5005 to collaborate with other groups
def group_rover(client_socket):
        while True:
            command = input("\nEnter 'Status' to get group rover data or 'Exit' to quit: ").strip()
            if command.lower() == "exit":
                client_socket.sendall("Exit".encode())
                print("\nExiting group rover mode.")
                break
            elif command.lower() == "status":
                client_socket.sendall("Status".encode())
                time.sleep(random.uniform(1.0, 2.0))
                response = client_socket.recv(1024).decode()
                print(f"\nReceived response: {response}")
            else:
                print("\n❌Invalid choice. Try again.")


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

elif port == 5004:  # Rover discovery
    print("\nListening for nearby lunar devices...")
    send_discovery_request(client_socket)

elif port == 5005:
    print("\nHandling group rover communication...")
    group_rover(client_socket)

# Close connections
client_socket.close()
server_socket.close()
print("\n🔴Server connection closed.")
