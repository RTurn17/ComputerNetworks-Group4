import socket
import time
import random
import csv
import pyfiglet
from colorama import Fore, init
from rich.console import Console
import threading

welcome_message = """
███████╗ █████╗ ██████╗ ████████╗██╗  ██╗         █████╗ ██╗  ██╗
██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║  ██║        ██╔══██╗██║  ██║
██████╗ ███████║██████╔╝   ██║   ███████║        ██║  ██║███████║
██╔════╗██╔══██║██╔██╗     ██║   ██╔══██║        ██║  ██║╚════██║
███████╗██║  ██║██║╚██╗    ██║   ██║  ██║         █████╔╝     ██║
╚══════╝╚═╝  ╚═╝╚═╝ ╚═╝    ╚═╝   ╚═╝  ╚═╝         ╚════╝      ╚═╝
"""
print(welcome_message) # Earth Computer Welcome message
init(autoreset=True)
console=Console()
print(Fore.GREEN+ pyfiglet.figlet_format("EARTH STATION"))
host = socket.gethostbyname(socket.gethostname())
print(f"\n🔹 Server IP Address: {host}")
def receive_with_timeout(client_socket, timeout, retries):
    client_socket.settimeout(timeout) 
    attempt = 0 
    while attempt < retries: 
        try:
            data = client_socket.recv(1024).decode() 
            if data:
                return data
        except socket.timeout: 
            attempt += 1
            print(f"⚠️ Timeout after {timeout}s. Retrying... ({attempt}/{retries})")
    print("Failed to receive data after multiple retries.")
    return None


PORT = 5006  # Ensure both server and client use the same port
client_ip="172.20.10.10"
def establish_tcp_connection():
    """Establishes a TCP connection with the discovered client"""
    try:
        tcp_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind((host,port))
        tcp_socket.listen(1)
        client_socket, client_address = tcp_socket.accept()
        print(f"✅Connection established with {client_address} on port {port}")
        response = client_socket.recv(1024).decode()
        if response:
            print(f"Response from rover: {response}")
        else:
            print("No response received from rover.")

        # Example: Send a command after discovery
        client_socket.sendall(b"Hello from Earth Station!")

        # Receive acknowledgment
        
        
    except socket.timeout:
        print(f"❌ Connection timed out while trying to connect to {client_ip}.")
    except Exception as e:
        print(f"❌ Error establishing TCP connection: {e}")
    finally:
        tcp_socket.close()
        print(f"TCP socket closed for {client_ip}.")
def broadcast_discovery():
    global broadcasting
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(5)  # Avoid indefinite waiting
    broadcasting = True

    print("\n Broadcasting discovery messages...")
    sock.sendto(b"Discovering nearby rovers", ("255.255.255.255", PORT))
    time.sleep(1)

    print(" Waiting for response...")
    while broadcasting:
        try:
            establish_tcp_connection()
            data, addr = sock.recvfrom(1024)  # Receive UDP response
            message = data.decode()
            #print(f"✅ Received response: {message} from {addr}")

            # Switch to a TCP connection to communicate further
              
            broadcasting = False  # Stop after receiving a response

        except socket.timeout:
            #print(" No response received.")
            broadcasting = False  # Prevent infinite loop
        except Exception as e:
            print(f" Error during response: {e}")
        finally:
            sock.close()  # Ensure the socket is closed properly






print("\nSelect a port for communication:")
print("5000 → Movement Commands")
print("5001 → Telemetry Requests")
print("5002 → Data Transmission")
print("5003 → Error Messages")
print("5004 → Discover Nearby Rovers")
print("5005 → Group Communication")
print("5006 for braodcast")
port = int(input("\nEnter port number (5000-5006): ").strip())

if port == 5006:
    broadcast_thread = threading.Thread(target=broadcast_discovery, daemon=True)
    broadcast_thread.start()
    
    while True:
        time.sleep(1)


else:
    def start_server(port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"\n🌍Earth Computer04 is listening on port {port}...")
        client_socket, client_address = server_socket.accept()
        print(f"✅Connection established with {client_address} on port {port}")
        return server_socket, client_socket

    server_socket, client_socket = start_server(port)

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
                client_socket.send(command.encode())
                time.sleep(random.uniform(1.0, 2.0))
                response = client_socket.recv(1024).decode()
                time.sleep(random.uniform(1.0, 2.0))
                print(f"\n📡Client response: {response}")
            except Exception as e:
                print(f"\n⚠️Error: {e}")
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
                print("\n🚪Exiting telemetry mode.")
                break
            else:
                print("\n❌Invalid choice, please try again.")
                continue
            time.sleep(random.uniform(1.0, 2.0))
            data = client_socket.recv(1024).decode()
            print(f"\n📊Received telemetry data: {data}")

    def receive_and_save_data(client_socket):
        print("\n📥Requesting data...")
        client_socket.sendall("Send data.".encode())

        # Create a new CSV file for writing received data
        with open("received_data.csv", "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)

            while True:
                try:
                    data = receive_with_timeout(client_socket, 300, 1)
                    if data: 
                        if data == "All data sent.":
                            print("\nAll data received from client.")
                            break

                        print(data.strip())  # Print every line of received data
                        csv_writer.writerow([data.strip()])  # Write received data to CSV file
                    else:
                        print("\n⚠️No data received within the timeout. Closing data reception.")
                        break

                except Exception as e:
                    print(f"\nError while receiving data: {e}")
                    break

        print("\n📂Data saved to received_data.csv.")

        # Now receive the image file
        try:
            # Wait for the image start marker
            marker = client_socket.recv(1024).decode().strip()
            if marker == "IMAGE_START":
                image_data = b""
                while True:
                    chunk = client_socket.recv(1024)
                    if b"IMAGE_END" in chunk:
                        end_index = chunk.find(b"IMAGE_END")
                        image_data += chunk[:end_index]
                        break
                    image_data += chunk

                # Save the received image to file
                with open("received_image.jpg", "wb") as img_file:
                    img_file.write(image_data)
                print("\n📂Data image is downloaded.")
            else:
                print(f"\n⚠️Expected IMAGE_START marker but got: {marker}")
        except Exception as e:
            print(f"\nError while receiving image: {e}")

        # Now receive the video file
        try:
            # Wait for the video start marker
            marker = client_socket.recv(1024).decode().strip()
            if marker == "VIDEO_START":
                video_data = b""
                while True:
                    chunk = client_socket.recv(1024)
                    if b"VIDEO_END" in chunk:
                        end_index = chunk.find(b"VIDEO_END")
                        video_data += chunk[:end_index]
                        break
                    video_data += chunk

                # Save the received video to file
                with open("recieved_video.mp4", "wb") as video_file:
                    video_file.write(video_data)
                print("\n📂Data video is downloaded.")
            else:
                print(f"\n⚠️Expected VIDEO_START marker but got: {marker}")
        except Exception as e:
            print(f"\nError while receiving video: {e}")


    def send_error_request(client_socket):
            while True:
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
                    handle_hardware_error(client_socket)
                    break
                elif choice == '2':
                    client_socket.sendall("Request out of sight error.".encode())
                    time.sleep(random.uniform(1.0, 2.0))
                    data = client_socket.recv(1024).decode()
                    print(f"\n {data}")
                    handle_out_of_sight_error(client_socket)
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
            message = "Rover has stopped due to a hardware error. Head Department notified."
            client_socket.sendall(message.encode())
            print("\nStopping rover and sending notification to Head Department...")
            time.sleep(3)
            print("\n🛑Rover stopped. Awaiting further instructions from the Head Department.")
        elif choice == '2':
            message = "Backup sensor activated. Rover continues operation."
            client_socket.sendall(message.encode())
            time.sleep(3)
            print("\n🛰️Backup sensor activated. Rover continues operation.")
        else:
            print("\n❌Invalid choice. Please select a valid action.")
            handle_hardware_error(client_socket)

    def handle_out_of_sight_error(client_socket):
        print("\nSelect action to handle out of sight error:")
        print("1 → Stop rover's operations and notify Head Department")
        print("2 → Get Rovers coordinates")
        choice = input("Enter your choice (1-2): ").strip()
        if choice == '1':
            message = "Rover is out of sight. Head Department notified."
            client_socket.sendall(message.encode())
            print("\nStopping rover and sending notification to Head Department...")
            time.sleep(3)
            print("\n🛑Rover stopped. Awaiting further instructions from the Head Department.")
        elif choice == '2':
            message = "Rovers Coordinations Request."
            client_socket.sendall(message.encode())
            time.sleep(3)
            print("\nRovers Coordinations Requested.")
            coordinates = client_socket.recv(1024).decode()
            print(f"\n📍Rover Coordinates: {coordinates}")
        else:
            print("\n❌Invalid choice. Please select a valid action.")
            handle_out_of_sight_error(client_socket)

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

    if port == 5000:
        send_movement_commands(client_socket)
    elif port == 5001:
        send_telemetry_request(client_socket)
    elif port == 5002:
        receive_and_save_data(client_socket)
    elif port == 5003:
        send_error_request(client_socket)
    elif port == 5005:
        group_rover(client_socket)