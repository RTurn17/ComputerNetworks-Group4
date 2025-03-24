import socket
import time

# Define the server details
SERVER_IP = '127.0.0.1'

# Define the ports for different tasks
PORTS = {
    "move": 5000,
    "telemetry": 5001,
    "data": 5002,
    "errors": 5003
}

# Generate RSA keys (for simplicity, generating them directly here)
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Function to encrypt message using public key
def encrypt_message(public_key, message):
    try:
        ciphertext = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext
    except Exception as e:
        print(f"Encryption error: {str(e)}")
        return None

# Function to handle movement
def movement_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORTS["move"]))
    
    while True:
        command = client_socket.recv(1024).decode()
        
        if command == "exit":
            print("\nExiting movement mode.")
            break
        elif command:
            print(f"|nReceived movement command: {command}")
            for _ in range(5):  # Print "Moving..." every second for 5 seconds
                print("Moving...")
                time.sleep(1)
            print(f"\nMoved to requested location: {command}")
        
        # Send confirmation to server
        client_socket.sendall(f"Moved to {command}".encode())

# Function to handle telemetry
def telemetry_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORTS["telemetry"]))

    while True:
        command = client_socket.recv(1024).decode()

        if command.startswith("Request telemetry data"):
            print("\nReceived telemetry request.")
            
            # Wait 3 seconds before sending data
            for _ in range(3):
                print("\nGathering data...")
                time.sleep(1)
        
        if command == "Request telemetry data for battery.":
            # Respond with detailed battery information
            data = (
                "\nBattery Voltage: 11.8V\n"
                "Battery Current: -1.2A\n"
                "Battery State of Charge (SOC): 75%\n"
                "Battery Health:\n"
                "   Charge Cycles: 200 cycles\n"
                "   Internal Resistance: 0.015 ohms\n"
                "   Capacity: 1500mAh\n"
            )
            client_socket.sendall(data.encode())
        
        elif command == "Request telemetry data for wheels.":
            # Respond with wheel telemetry data
            data = (
                "\nWheel Speed:\n"
                "   Front Left Wheel: 0.5 m/s\n"
                "   Front Right Wheel: 0.5 m/s\n"
                "   Rear Left Wheel: 0.4 m/s\n"
                "   Rear Right Wheel: 0.5 m/s \n"
                "Wheel Torque:\n"
                "   Front Left Wheel: 2.5 Nm\n"
                "   Front Right Wheel: 2.4 Nm\n"
                "   Rear Left Wheel: 2.3 Nm\n"
                "   Rear Right Wheel: 2.5 Nm\n"
            )
            client_socket.sendall(data.encode())
        
        elif command == "Request telemetry data for thermal conditions.":
            # Respond with thermal condition data
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
            return

# Function to handle data sending
def data_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORTS["data"]))

    print("\nServer asks to send data.")
        
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
            print("\nAll data sent.")
            
    except FileNotFoundError:
            print("\nCSV file not found.")


# Function to send errors
def error_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORTS["errors"]))

    while True:
        # Receive error request from server
        error_request = client_socket.recv(1024).decode()
        print(f"\nReceived request: {error_request}")
        
        # Determine appropriate response
        if error_request == "Request hardware error.":
            response = "Hardware Error"
        elif error_request == "Request out of sight error.":
            response = "Out of Sight Error"
        else:
            response = "Unknown Error Request"

        # Wait 1 second before sending response
        time.sleep(1)

        # Send response to server
        client_socket.sendall(response.encode())
        print(f"Sent response: {response}")

# Start clients in separate threads
import threading

threads = [
    threading.Thread(target=movement_client),
    threading.Thread(target=telemetry_client),
    threading.Thread(target=data_client),
    threading.Thread(target=error_client)
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()