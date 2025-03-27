import socket
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

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
def movement_client(public_key):  # Added public_key as a parameter
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORTS["move"]))
    
    while True:
        command = client_socket.recv(1024).decode()
        
        if command == "exit":
            print("\nExiting movement mode.")
            break
        elif command:
            print(f"\nReceived movement command: {command}")
            for _ in range(5):  # Print "Moving..." every second for 5 seconds
                print("Moving...")
                time.sleep(1)
            print(f"\nMoved to requested location: {command}")
        
        # Encrypt the confirmation message before sending
        encrypted_message = encrypt_message(public_key, f"Moved to {command}")
        
        if encrypted_message:
            client_socket.sendall(encrypted_message)
        else:
            print("ACCESS DENIED: Encryption failed due to mismatched keys.")
            break

# Function to handle telemetry
def telemetry_client(public_key):  # Added public_key as a parameter
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
            # Encrypt and send the telemetry data
            encrypted_data = encrypt_message(public_key, data)
            if encrypted_data:
                client_socket.sendall(encrypted_data)
            else:
                print("ACCESS DENIED: Encryption failed due to mismatched keys.")
                break
        
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
            encrypted_data = encrypt_message(public_key, data)
            if encrypted_data:
                client_socket.sendall(encrypted_data)
            else:
                print("ACCESS DENIED: Encryption failed due to mismatched keys.")
                break
        
        elif command == "Request telemetry data for thermal conditions.":
            # Respond with thermal condition data
            data = (
                "\nAmbient Temperature: 127°C (260°F)\n"
                "Electronics Temperature: 15°C (59°F)\n"
                "Battery Temperature: 47°C (116.6°F)\n"
                "Wheel Temperature: 48°C (118.4°F)\n"
            )
            encrypted_data = encrypt_message(public_key, data)
            if encrypted_data:
                client_socket.sendall(encrypted_data)
            else:
                print("ACCESS DENIED: Encryption failed due to mismatched keys.")
                break
        
        elif command == "Exit":
            print("\nExiting telemetry mode.")
            break
        else:
            print("\nUnknown telemetry request.")
        
# Function to handle data sending
def data_client(public_key):  # Added public_key as a parameter
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORTS["data"]))

    print("\nServer asks to send data.")
        
    # Open the CSV file and send it line by line with a delay
    try:
        with open("data_dummy1.csv", 'r') as file:
            for line in file:
                # Encrypt each line before sending to the server
                encrypted_line = encrypt_message(public_key, line.strip())  # Encrypt each line
                if encrypted_line:
                    client_socket.sendall(encrypted_line)
                    time.sleep(1)
                else:
                    print("ACCESS DENIED: Encryption failed due to mismatched keys.")
                    break

            # After sending all lines, notify the server
            encrypted_message = encrypt_message(public_key, "All data sent.".strip())  # Encrypt notification message
            if encrypted_message:
                client_socket.sendall(encrypted_message)
                print("\nAll data sent.")
            else:
                print("ACCESS DENIED: Encryption failed for final message.")
            
    except FileNotFoundError:
        print("\nCSV file not found.")


# Function to send errors
def error_client(public_key):  # Added public_key as a parameter
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORTS["errors"]))

    while True:
        error_request = client_socket.recv(1024).decode()
        print(f"\nReceived request: {error_request}")
        
        if error_request == "Request hardware error.":
            response = "Hardware Error"
        elif error_request == "Request out of sight error.":
            response = "Out of Sight Error"
        else:
            response = "Unknown Error Request"

        time.sleep(1)

        # Encrypt the error response before sending to the server
        encrypted_response = encrypt_message(public_key, response)  # Encrypt response
        if encrypted_response:
            client_socket.sendall(encrypted_response)
        else:
            print("ACCESS DENIED: Encryption failed due to mismatched keys.")
            break

        print(f"Sent response: {response}")


# Start clients in separate threads
import threading

# Generate the public key once (shared among clients)
_, public_key = generate_rsa_keys()

threads = [
    threading.Thread(target=movement_client, args=(public_key,)),
    threading.Thread(target=telemetry_client, args=(public_key,)),
    threading.Thread(target=data_client, args=(public_key,)),
    threading.Thread(target=error_client, args=(public_key,))
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
