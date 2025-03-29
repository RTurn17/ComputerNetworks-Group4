import socket
import random
import time
import threading

# Define the server details
SERVER_IP = 'localhost' #localhost for same laptop ######## CHANGE TO IP ###########
ROVER_ID = "Rover_04"  # Unique identifier for your rover

# Define the ports for different tasks
PORTS = {
    "move": 5000,
    "telemetry": 5001,
    "data": 5002,
    "errors": 5003,
    "discovery": 5004 
}

# Function to handle movement
def movement_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORTS["move"]))

        while True:
            command = client_socket.recv(1024).decode()
            if command == "exit":
                print("\n🚪Exiting movement mode.")
                break

            elif command:
                time.sleep(random.uniform(1.0, 2.0))  
                print(f"\n📡Received movement command: {command}") 
                for _ in range(5):
                    print("Moving...")
                    time.sleep(1)
                print(f"\n📍Moved to requested location: {command}")

                # Send confirmation to server
                client_socket.sendall(f"Moved to {command}".encode())
    
    except ConnectionError:
        print("\nPort 5000: Movement, not on use.")
    except Exception as e:
        print(f"\n⚠️Unexpected error in movement_client(): {e}")
    finally:
        client_socket.close()

# Function to handle telemetry
def telemetry_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORTS["telemetry"]))

        while True:
            command = client_socket.recv(1024).decode()

            if command.startswith("Request telemetry data"):
               time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
               print("\nReceived telemetry request.")
            
               # Wait 3 seconds before sending data
               for _ in range(3):
                   print("\n📥Gathering data...")
                   time.sleep(1)
        
            if command == "Request telemetry data for battery.":
                # Respond with detailed battery information
                data = (
                "\n🔋Battery Voltage: 11.8V\n"
                "🔋Battery Current: -1.2A\n"
                "🔋Battery State of Charge (SOC): 75%\n"
                "🔋Battery Health:\n"
                "   Charge Cycles: 200 cycles\n"
                "   Internal Resistance: 0.015 ohms\n"
                "   Capacity: 1500mAh\n"
                )
                client_socket.sendall(data.encode())
        
            elif command == "Request telemetry data for wheels.":
               # Respond with wheel telemetry data
                data = (
                "\n🛞Wheel Speed:\n"
                "   Front Left Wheel: 0.5 m/s\n"
                "   Front Right Wheel: 0.5 m/s\n"
                "   Rear Left Wheel: 0.4 m/s\n"
                "   Rear Right Wheel: 0.5 m/s \n"
                "🛞Wheel Torque:\n"
                "   Front Left Wheel: 2.5 Nm\n"
                "   Front Right Wheel: 2.4 Nm\n"
                "   Rear Left Wheel: 2.3 Nm\n"
                "   Rear Right Wheel: 2.5 Nm\n"
                )
                client_socket.sendall(data.encode())
        
            elif command == "Request telemetry data for thermal conditions.":
                # Respond with thermal condition data
                data = (
                "\n🌡Ambient Temperature: 127°C (260°F)\n"
                "🌡Electronics Temperature: 15°C (59°F)\n"
                "🌡Battery Temperature: 47°C (116.6°F)\n"
                "🌡Wheel Temperature: 48°C (118.4°F)\n"
                )
                client_socket.sendall(data.encode())
        
            elif command == "Exit":
                print("\n🚪Exiting telemetry mode.")
                break
            else:
                print("\n⚠️Unknown telemetry request.")
                continue
        
    except ConnectionError:
        print("\nPort 5001: Telemetry, not on use.")
    except Exception as e:
        print(f"\n⚠️Unexpected error in telemetry_client(): {e}")
    finally:
        client_socket.close()

# Function to handle data sending
def data_client():
    try: 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORTS["data"]))

        time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
        print("\n📊Server asks to send data.")
        
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
                print("\n✅All data sent.")
            
        except FileNotFoundError:
                print("\n⚠️CSV file not found.")

    except ConnectionError:
        print("\nPort 5002: Data, not on use")
    except Exception as e:
        print(f"\n⚠️Unexpected error in data_client(): {e}")
    finally:
        client_socket.close()


# Function to send errors
def error_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORTS["errors"]))

        while True:
            # Receive error request from server
            error_request = client_socket.recv(1024).decode()
            #print(f"\nReceived request: {error_request}")
        
             # Respond to the server based on the error message
            if error_request == "Request hardware error.":
                time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
                # Hardware error encountered, simulate handling it
                print("\n⚠️Sensor Malfunctioning!")
            
                # Respond based on the server's choice (either stop or use backup)
                error_response = "Sensor Hardware error encountered!"
                client_socket.sendall(error_response.encode())
            
                action_taken = client_socket.recv(1024).decode()
                time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
                print(f"\nAction taken: {action_taken}")

                if action_taken == "Rover has stopped due to a hardware error. Head Department notified.":
                   time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
                   print("\n🛑Stopping Rover...")
                   break
                elif action_taken == "Backup sensor activated. Rover continues operation.":
                    time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
                    print("\n🚨Activating backup sensor and continuing rover's operation...")
                    break

            elif error_request == "Request out of sight error.":
                time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
                print("\n...")
                # Handle the out of sight error accordingly...
                 # Respond based on the server's choice (either stop or use backup)
                error_response = "⚠️Rover Out Of Sight!"
                client_socket.sendall(error_response.encode())
    
                action_taken = client_socket.recv(1024).decode()
                time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
                print(f"\nAction taken: {action_taken}")
    
                if action_taken == "Rover is out of sight. Head Department notified.":
                   time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
                   print("\n🛑Stopping Rover...")
                   break
                elif action_taken == "Rovers Coordinations Request.":
                     time.sleep(random.uniform(1.0, 2.0))  # Random delay between 1 and 2 seconds (simulation)
                     print("\n📍Getting Rovers Coordinates...")
                     coordinates = "30.20"
                     client_socket.sendall(coordinates.encode())
                     break

            else:
                print("\n⚠️Unknown error request.")
                continue
            
    except ConnectionError:
        print("\nPort 5003: Error simulation, not on use")
    except Exception as e:
        print(f"\n⚠️Unexpected error in error_client(): {e}")
    finally:
        client_socket.close()


#Discover othe rorvers:
def discovery_client(): 
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORTS["discovery"]))

        while True:
            command = client_socket.recv(1024).decode()
            if command == "Exit":
                print("\n🚪Exiting discovery mode.")
                break

            elif command =="Nearby discovery.":
                time.sleep(random.uniform(1.0, 2.0))  
                print(f"\n🤖Searching for nearby rovers...")

                # Simulating a list of nearby rovers found (In a real scenario, you might query for available rovers)
                nearby_rovers = ["Rover_03", "Rover_13"]

                # Send the list of nearby rovers to the server
                print(f"\n🤖Nearby rovers found: {', '.join(nearby_rovers)}")
                client_socket.sendall(f"Nearby rovers: {', '.join(nearby_rovers)}".encode())

                # Wait for server to respond with a choice of rover to connect to
                chosen_rover = client_socket.recv(1024).decode()
                print(f"\n🤖Server selected rover: {chosen_rover}")

                if chosen_rover in nearby_rovers:
                    print(f"\nAttempting to connect to {chosen_rover}...")

                    # Simulate connection establishment with the chosen rover
                    # In a real-world scenario, the client could try to connect to the specific rover
                    # Here we just simulate a successful connection to the chosen rover
                    client_socket.sendall(f"Connecting to {chosen_rover}".encode())

                    # Now the server can handle further communication with the chosen rover
                    print(f"\n✅Connection established with {chosen_rover}.")
                else:
                    print(f"\nInvalid rover selected by server.")
    
    except ConnectionError:
        print("\nPort 5004: Discovery, not on use")
    except Exception as e:
        print(f"\n⚠️Unexpected error in discovery_client(): {e}")
    finally:
        client_socket.close()

# Start clients in separate threads

threads = [
    threading.Thread(target=movement_client),
    threading.Thread(target=telemetry_client),
    threading.Thread(target=data_client),
    threading.Thread(target=discovery_client),
    threading.Thread(target=error_client)
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
