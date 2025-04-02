# lunar_rover.py (Client)

import socket
import random
import time
import threading
import pyfiglet
from colorama import Fore, init
from rich.console import Console

welcome_message = """
██╗    ██╗   ██╗███╗   ██╗ █████╗ ██████╗       ██████╗ ██████╗ ██╗   ██╗███████╗██████╗
██║    ██║   ██║████╗  ██║██╔══██╗██╔══██╗      ██╔══██╗██╔══██╗██║   ██║██╔════╝██╔══██╗
██║    ██║   ██║██╔██╗ ██║███████║██████╔╝      ██████╔╝██║  ██║██║   ██║██████╗ ██████╔╝
██║    ██║   ██║██║╚██╗██║██╔══██║██╔██╗        ██╔██╗  ██║  ██║ ██║ ██║ ██╔════╗██╔██╗
██████╗╚██████╔╝██║ ╚████║██║  ██║██║╚██╗       ██║╚██╗ ██████╔╝  ╚███╔╝ ███████╗██║╚██╗  
╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝ ╚═╝       ╚═╝ ╚═╝ ╚═════╝    ╚══╝  ╚══════╝╚═╝ ╚═╝
"""

print(welcome_message)
init(autoreset=True)
console=Console()
print(Fore.CYAN+ pyfiglet.figlet_format("LETS EXPLORE THE MOON!"))

SERVER_IP = '192.168.69.184'  # Change to the Earth station's IP address
#SERVER_IP = '10.6.126.167' # example of a different IP

PORTS = {
    "move": 5000,
    "telemetry": 5001,
    "data": 5002,
    "errors": 5003,
    "discovery": 5004,
    "group": 5005,
    "broadcast":5006
}

def broadcast():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Socket
        sock.bind(("", 5006)) # Listen on all interfaces, port 5004

        print("Listening for discovery broadcasts...")
        while True:
            data, addr = sock.recvfrom(1024) # Receive UDP data
            message = data.decode()
            print(f"Received discovery message: {message} from {addr}")

            
            if "Lunar Rover Discovery" in message:
                response = "testing"
                server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_sock.connect((SERVER_IP, 5006))
                server_sock.sendall(response.encode())
                
                    
                print(f"address ,{addr}")
                print("Message sent")
                server_sock.close()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

"""# Server Authentication
def authenticate(client_socket):
    # Define array of passwords
    key = ["r8d4iUv43G", "sc80o1H4bM", "iWx6pMduF7", "4yV8dfX6ar", "m3C2gD8z7", "j8lnk1Egy8", "G5bl172eHv"]
    keyWord = int(time.time()) % 7
    correct_password = key[keyWord]
    
    # Receive the password from the server
    server_password = client_socket.recv(1024).decode()

    if server_password == correct_password:
        # If password is correct, send success response
        client_socket.send("correct".encode())
        return True
    else:
        # If password is incorrect, send failure response
        client_socket.send("incorrect".encode())
        return False """

# Function to handle movement request        
def movement_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORTS['move']))

        while True:
            command = client_socket.recv(1024).decode()
            if command == "exit":
                print("\nExiting movement mode.")
                break
            elif command:
                time.sleep(random.uniform(1.0, 2.0))
                print(f"\nReceived movement command: {command}")
                for _ in range(5):
                    print("Moving...")
                    time.sleep(1)
                print(f"\nMoved to requested location: {command}")
                client_socket.sendall(f"Moved to {command}".encode())

    except ConnectionError:
        print("Port 5000: Movement, not on use.")
    except Exception as e:
        print(f"\nUnexpected error in movement_client(): {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass

# Function to handle telemetry request
def telemetry_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORTS["telemetry"]))

        while True:
            command = client_socket.recv(1024).decode()

            if command.startswith("Request telemetry data"):
                time.sleep(random.uniform(1.0, 2.0))
                print("\nReceived telemetry request.")

                for _ in range(3):
                    print("\nGathering data...")
                    time.sleep(1)

            if command == "Request telemetry data for battery.":
                data = (
                    "\nBattery Voltage: 11.8V\n"
                    "Battery Current: -1.2A\n"
                    "Battery State of Charge (SOC): 75%\n"
                    "Battery Health:\n"
                    "  Charge Cycles: 200 cycles\n"
                    "  Internal Resistance: 0.015 ohms\n"
                    "  Capacity: 1500mAh\n"
                )
                client_socket.sendall(data.encode())

            elif command == "Request telemetry data for wheels.":
                data = (
                    "\nWheel Speed:\n"
                    "  Front Left Wheel: 0.5 m/s\n"
                    "  Front Right Wheel: 0.5 m/s\n"
                    "  Rear Left Wheel: 0.4 m/s\n"
                    "  Rear Right Wheel: 0.5 m/s \n"
                    "Wheel Torque:\n"
                    "  Front Left Wheel: 2.5 Nm\n"
                    "  Front Right Wheel: 2.4 Nm\n"
                    "  Rear Left Wheel: 2.3 Nm\n"
                    "  Rear Right Wheel: 2.5 Nm\n"
                )
                client_socket.sendall(data.encode())

            elif command == "Request telemetry data for thermal conditions.":
                data = (
                    "\nAmbient Temperature: 127°C (260°F)\n"
                    "Electronics Temperature: 15°C (59°F)\n"
                    "Battery Temperature: 47°C (116.6°F)\n"
                    "Wheel Temperature: 48°C (118.4°F)\n"
                )
                client_socket.sendall(data.encode())

            elif command == "Exit":
                print("\nExiting telemetry mode.")
                break
            else:
                print("\nUnknown telemetry request.")
                continue

    except ConnectionError:
        print("Port 5001: Telemetry, not on use.")
    except Exception as e:
        print(f"\nUnexpected error in telemetry_client(): {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass

# Function to handle data sending
def data_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORTS["data"]))

        time.sleep(random.uniform(1.0, 2.0))
        print("\nServer asks to send data.")
        
        # Open the CSV file and send it line by line with a delay simulation
        try:
            with open("data_dummy1.csv", 'r') as file:
                for line in file:
                    client_socket.sendall(line.encode())  # Send line by line to the server
                    time.sleep(1)  # Wait for 1 second before sending the next line

            # After sending all CSV lines:
            client_socket.sendall("All data sent.".encode())
            print("\n All data sent.")
        except FileNotFoundError:
            print("\nCSV file not found.")
        
        # Now send the image file (additional feature) with handshake
        try:
            with open("image_dummy.jpg", "rb") as image_file:
                # Signal the start of the image transfer
                client_socket.sendall("IMAGE_START".encode())
                time.sleep(0.5)
                # Read and send the image in chunks (1KB per chunk)
                while True:
                    chunk = image_file.read(1024)
                    if not chunk:
                        break
                    client_socket.sendall(chunk)
                time.sleep(0.5)
                # Signal the end of the image transfer
                client_socket.sendall("IMAGE_END".encode())
            time.sleep(0.5)
            print("\n Data image sent. Waiting for server acknowledgment...")
            
            # Wait for the server's acknowledgment for the image
            ack = client_socket.recv(1024).decode().strip()
            if ack == "IMAGE_RECEIVED":
                print("\n Server confirmed image receipt.")
            else:
                print("\n Expected acknowledgment for image transfer:", ack)
        except FileNotFoundError:
            print("\n⚠Image file not found.")
        
        # Now send the video file (additional feature)
        try:
            with open("dummy_video.mp4", "rb") as video_file:
                # Signal the start of the video transfer
                client_socket.sendall("VIDEO_START".encode())
                time.sleep(0.5)
                # Read and send the video in chunks (1KB per chunk)
                while True:
                    chunk = video_file.read(1024)
                    if not chunk:
                        break
                    client_socket.sendall(chunk)
                time.sleep(0.5)
                # Signal the end of the video transfer
                client_socket.sendall("VIDEO_END".encode())
            print("\nVideo data is sent.")
        except FileNotFoundError:
            print("\nVideo file not found.")

    except ConnectionError:
        print("Port 5002: Data, not on use.")
    except Exception as e:
        print(f"\nUnexpected error in data_client(): {e}")
    finally:
        client_socket.close()


# Function to send error simulations
def error_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORTS["errors"]))

        while True:
            error_request = client_socket.recv(1024).decode()
            if error_request == "Request hardware error.":
                time.sleep(random.uniform(1.0, 2.0))
                print("\nSensor Malfunctioning!")

                error_response = "Sensor Hardware error encountered!"
                client_socket.sendall(error_response.encode())

                action_taken = client_socket.recv(1024).decode()
                time.sleep(random.uniform(1.0, 2.0))
                print(f"\nAction taken: {action_taken}")

                if action_taken == "Rover has stopped due to a hardware error. Head Department notified.":
                    time.sleep(random.uniform(1.0, 2.0))
                    print("\nStopping Rover...")
                    break
                elif action_taken == "Backup sensor activated. Rover continues operation.":
                    time.sleep(random.uniform(1.0, 2.0))
                    print("\nActivating backup sensor and continuing rover's operation...")
                    break

            elif error_request == "Request out of sight error.":
                time.sleep(random.uniform(1.0, 2.0))
                print("\n...")

                error_response = "Rover Out Of Sight!"
                client_socket.sendall(error_response.encode())

                action_taken = client_socket.recv(1024).decode()
                time.sleep(random.uniform(1.0, 2.0))
                print(f"\nAction taken: {action_taken}")

                if action_taken == "Rover is out of sight. Head Department notified.":
                    time.sleep(random.uniform(1.0, 2.0))
                    print("\nStopping Rover...")
                    break
                elif action_taken == "Rovers Coordinations Request.":
                    time.sleep(random.uniform(1.0, 2.0))
                    print("\nGetting Rover's Coordinates...")
                    coordinates = "30.20"
                    client_socket.sendall(coordinates.encode())
                    break

            elif error_request == "Exit":
                print("\nExiting error mode.")
                break
            else:
                print("\n⚠️Unknown Error request.")
                continue

    except ConnectionError:
        print("Port 5003: Error simulation, not on use")
    except Exception as e:
        print(f"\nUnexpected error in error_client(): {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass

# Function to discover othe rorvers
def discovery_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORTS["discovery"]))

        while True:
            command = client_socket.recv(1024).decode()
            if command == "Exit":
                print("\nExiting discovery mode.")
                break

            elif command == "Nearby discovery.":
                time.sleep(random.uniform(1.0, 2.0))
                print(f"\nSearching for nearby rovers...")

                nearby_rovers = ["Rover_03", "Rover_13"]

                print(f"\nNearby rovers found: {', '.join(nearby_rovers)}")
                client_socket.sendall(f"Nearby rovers: {', '.join(nearby_rovers)}".encode())

                chosen_rover = client_socket.recv(1024).decode()
                print(f"\nServer selected rover: {chosen_rover}")

                if chosen_rover in nearby_rovers:
                    print(f"\nAttempting to connect to {chosen_rover}...")
                    client_socket.sendall(f"Connecting to {chosen_rover}".encode())
                    print(f"\nConnection established with {chosen_rover}.")
                else:
                    print(f"\nInvalid rover selected by server.")

    except ConnectionError:
        print("Port 5004: Discovery, not on use")
    except Exception as e:
        print(f"\nUnexpected error in discovery_client(): {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass

# Function for group rover communication
def group_rover():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind(("0.0.0.0",PORTS["group"]))
        client_socket.listen(1)
        server_address, client_address = client_socket.accept()

        print("\n client is listening on 5005")
        print(f"\n connected {client_address}")

        while True:
            command = server_address.recv(1024).decode()
            if command == "Exit":
                break
            elif command == "Status":
                location = "xy sol=yu"
                nearby_rovers = ["Rover_03", "Rover_013"]
                status_message = f"Location: {location} | Nearby rovers: {', '.join(nearby_rovers)}"
                server_address.sendall(status_message.encode())
    except Exception as e:
        print(f"\nError in group_rover(): {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass

threads = [
    threading.Thread(target=movement_client),
    threading.Thread(target=telemetry_client),
    threading.Thread(target=data_client),
    threading.Thread(target=discovery_client),
    threading.Thread(target=error_client),
    threading.Thread(target=group_rover),
    threading.Thread(target=broadcast)
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()