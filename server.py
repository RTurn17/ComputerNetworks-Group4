import socket
import json

PORT = 6000  # Ground station port

# Create a UDP socket for receiving data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

print(f"🌍 Ground Station Listening on Port {PORT}...")

while True:  # Keep the server running indefinitely
    try:
        data, addr = sock.recvfrom(1024)  # Receive message
        sensor_data = json.loads(data.decode())  # Decode JSON
        print(f"🔍 Raw Data Received: {sensor_data}")  # Debug print

        if isinstance(sensor_data, dict) and "rover_id" in sensor_data:
            print(f"✅ Received from {sensor_data['rover_id']}: {sensor_data}")
        else:
            print(f"⚠️ Rover: {sensor_data}")

    except json.JSONDecodeError:
        print(f"🛑 Invalid JSON: {data.decode()}")

    except Exception as e:
        print(f"❌ Error: {e}")
