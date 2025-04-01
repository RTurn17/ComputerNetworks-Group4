import socket
import time
import random
import csv

# Automatically determine the server's IP address
#host = socket.gethostbyname(socket.gethostname()) ##Uncomment

# Print the determined IP address
#print(f"\n🔹 Server IP Address: {host}") ##Uncomment

# Authentication
def authenticate(client_socket):
    # Define the correct passwords
    key = ["r8d4iUv43G", "sc80o1H4bM", "iWx6pMduF7", "4yV8dfX6ar", "m3C2gD8z7", "j8lnk1Egy8", "G5bl172eHv"]
    # key = ["sdlakfjklasdfj", "sdafsadf", "asdfsadf", "asdfsadf", "asdfsadf", "asdfsadf", "asdfasdf"]
    keyWord = int(time.time()) % 7
    current_password = key[keyWord]

    # send current password to client
    client_socket.send(current_password.encode())
    # Wait for client to confirm the password
    response = client_socket.recv(1024).decode()
    
    if response == "correct":
        return True
    else:
        return False

# Function to create and bind a socket on a given port
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", port))
    server_socket.listen(1)
    print(f"\n🌍Server is listening on port {port}...")

    client_socket, client_address = server_socket.accept()

    authented = True
    if(port == 5000 or port == 5001 or port == 5002 or port == 5003):
        authented = authenticate(client_socket)
        print(authented)

    if (authented):
        print(f"✅Connection established with {client_address} on port {port}")
        return server_socket, client_socket, 1
    else: 
        print("Authentication failed, connection terminating.")
        return server_socket, client_socket, 0

# Ask user which port to use
print("\nSelect a port for communication:")
print("5000 → Movement Commands")
print("5001 → Telemetry Requests")
print("5002 → Data Transmission")
print("5003 → Error Messages")
print("5004 → Discover Nearby Rovers")

port = int(input("\nEnter port number (5000-5004): ").strip())

# local_password = "securepassword123"
# # Ask the user to input the password
# password_input = input("\nPlease enter your password: ")
# # Check if user input correct password
# if (password_input == local_password):
#     # Start the server on the chosen port
#     server_socket, client_socket, auth = start_server(port)
#     if(auth == 0):
#         client_socket.close()
#         server_socket.close()
# else:
#     print("Incorrct Password\n")

# Start the server on the chosen port
server_socket, client_socket, auth = start_server(port)
if(auth == 0):
    client_socket.close()
    server_socket.close()

def send_movement_commands(client_socket):
    while True:
        try:
            x = input("\nEnter target X coordinate (or 'exit' to close connection): ").strip()
            if x.lower() == "exit":
                client_socket.send("exit".encode())
                print("\n🚪Exiting movement mode.")
                break
            
            y = input("Enter target Y coordinate: ").strip()

            # Send coordinates as a comma-separated string
            command = f"{x},{y}"
            client_socket.send(command.encode())
            time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)

            # Wait for a response from the client
            response = client_socket.recv(1024).decode()
            time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
            print(f"\n📡Client response: {response}")

        except Exception as e:
            print(f"\n⚠Error: {e}")
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
            print("\n🚪Exiting telemetry mode.")
            break
        else:
            print("\n❌Invalid choice, please try again.")
            continue

        # Receive and print telemetry response
        time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
        data = client_socket.recv(1024).decode()
        print(f"\n📊Received telemetry data: {data}")


def receive_and_save_data(client_socket):
    print("\n📥Requesting data...")
    client_socket.sendall("Send data.".encode())

    # Open CSV file for writing received data
    with open("received_data.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)

        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    print("\n⚠No data received, client may have disconnected.")
                    break
                if data == "All data sent.":
                    print("\n✅All data received from client.")
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

    print("\n📂Data saved to received_data.csv.")

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

    if choice == '1':
        # Stop rover operations and notify head department
        message = "Rover has stopped due to a hardware error. Head Department notified."
        client_socket.sendall(message.encode())
        print("\nStopping rover and sending notification to Head Department...")

        # Here, you can simulate sending a message to a real department (e.g., via an email API or other messaging system).
        # Simulating the stop action:
        time.sleep(3)
        #  - Disable rover functionality
        print("\n🛑Rover stopped. Awaiting further instructions from the Head Department.")
        # This might include disabling movement, sensors, etc., depending on your setup.
        
    elif choice == '2':
        # Use backup sensor and continue operation
        message = "Backup sensor activated. Rover continues operation."
        client_socket.sendall(message.encode())
        time.sleep(3)
        print("\n🛰Backup sensor activated. Rover continues operation.")
        # Simulate activation of a backup sensor here, or continue the rover with limited functionality.
    else:
        print("\n❌Invalid choice. Please select a valid action.")
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
        print("\n🛑Rover stopped. Awaiting further instructions from the Head Department.")
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
        print(f"\n📍Rover Coordinates: {coordinates}")
    else:
        print("\n❌Invalid choice. Please select a valid action.")
        handle_out_of_sight_error(client_socket)  # Recursive call to handle error again


def send_discovery_request(client_socket):
    while True:
        # Choose error type
        choice = input("\nEnter 'Discover nearby devices' to discover or 'Exit' to quit: ").strip()

        if choice == 'Discover nearby devices':
            print("\nᯤRequesting rover to discover nearby devices...")

            # Send the discovery command to the rover (client)
            client_socket.sendall("Nearby discovery.".encode())

            # Wait for the rover (client) to send back a list of nearby devices (rovers)
            nearby_rovers_message = client_socket.recv(1024).decode()
            #print(f"\nReceived from rover: {nearby_rovers_message}")

            # Ask the user to choose a rover from the discovered rovers
            nearby_rovers = nearby_rovers_message.split(": ")[1].split(", ")
            print(f"\n🤖Nearby rovers found: {', '.join(nearby_rovers)}")
            chosen_rover = input("\nChoose a rover to connect to: ").strip()

            # Send the user's choice of rover to the rover (client)
            client_socket.sendall(chosen_rover.encode())

            # Wait for rover (client) to acknowledge connection
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


if auth == 1:
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

# Close connections
client_socket.close()
server_socket.close()
print("\n🔴Server connection closed.")
