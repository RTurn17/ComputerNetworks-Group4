import socket
import csv
import time

# Configuration for server connection
SERVER_IP = '172.20.10.4'  # Update to the actual server IP if needed
SERVER_PORT = 5000       # Update to the actual server port if needed

def load_csv_data(filename):
    """Load CSV data from file and return header and rows."""
    data = []
    try:
        with open(filename, 'r', encoding='latin1') as file:  # specify encoding
            reader = csv.reader(file)
            header = next(reader)  # Read header
            for row in reader:
                data.append(row)
        print(f"CSV file '{filename}' loaded successfully. Total rows: {len(data)}")
        return header, data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None, None

def client_program(filename):
    header, data = load_csv_data(filename)
    if header is None or data is None:
        return

    print("Connecting to server...")
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((SERVER_IP, SERVER_PORT))
            print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
        except Exception as e:
            print(f"Connection error: {e}")
            return

        print("Waiting for server request...")

        while True:
            try:
                # Wait for a message from the server
                msg = client_socket.recv(1024).decode()
                if not msg:
                    print("Server closed connection.")
                    break

                print(f"Received message from server: {msg.strip()}")

                # Check if server is asking for data
                if msg.strip() == "REQUEST_DATA":
                    print("Server requested data. Preparing to send all CSV data...")

                    # Optional: send a signal that data sending is about to start
                    client_socket.sendall("DATA_START".encode())
                    time.sleep(0.5)

                    # First send the header (could be useful for the server to know columns)
                    header_line = ','.join(header)
                    client_socket.sendall((header_line + "\n").encode())
                    print(f"Sent header: {header_line}")

                    # Loop through each row and send it
                    for row in data:
                        row_line = ','.join(row)
                        client_socket.sendall((row_line + "\n").encode())
                        print(f"Sent data row: {row_line}")
                        # Simulate delay between sending rows if desired
                        time.sleep(0.01)

                    # Optional: signal the end of data transmission
                    client_socket.sendall("DATA_END".encode())
                    print("All CSV data sent to server.")
                    break
            except Exception as e:
                print(f"Error during communication: {e}")
                break

if __name__ == "__main__":
    # Ensure the CSV file is in the same directory or provide the full path.
    FILENAME = "Lunar Project _ Group4(Day data).csv"
    client_program(FILENAME)
