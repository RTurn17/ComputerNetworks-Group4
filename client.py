import streamlit as st
import socket
import threading
import json
import time
import random

# Configurations
GROUND_STATION_IP = "127.0.0.1"
GROUND_STATION_PORT = 6000

# Generate a unique Rover ID and a dynamic port
ROVER_ID = f"Rover_{random.randint(1000, 9999)}"
PORT = random.randint(5000, 6000)  # Avoid port conflicts

# Store messages & connected peers
if "messages" not in st.session_state:
    st.session_state.messages = []
if "peers" not in st.session_state:
    st.session_state.peers = {}

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

# Function to generate sensor data
def generate_sensor_data():
    return json.dumps({
        "rover_id": ROVER_ID,
        "timestamp": time.time(),
        "temperature": round(100 * (0.5 + 0.5 * time.perf_counter() % 1), 2),
        "radiation": round(50 * (0.5 + 0.5 * time.perf_counter() % 1), 2),
        "terrain": "rocky" if time.perf_counter() % 2 > 1 else "smooth"
    })

# Function to send data to a peer
def send_to_peer(peer_ip, peer_port, message):
    msg_data = json.dumps({"sender": ROVER_ID, "message": message})
    sock.sendto(msg_data.encode(), (peer_ip, peer_port))
    st.session_state.messages.append(f"✅ Sent to {peer_ip}:{peer_port} → {message}")

# Function to send sensor data to Earth
def send_to_ground_station():
    message = generate_sensor_data()
    sock.sendto(message.encode(), (GROUND_STATION_IP, GROUND_STATION_PORT))
    st.session_state.messages.append("🚀 Sent sensor data to Earth station")

# Function to receive messages
def receive_messages():
    while True:
        data, addr = sock.recvfrom(1024)
        try:
            decoded_data = json.loads(data.decode())

            if isinstance(decoded_data, dict) and "message" in decoded_data:
                st.session_state.messages.append(f"📩 From {decoded_data['sender']}: {decoded_data['message']}")
            else:
                st.session_state.messages.append(f"🌍 Sensor Data Received: {decoded_data}")

            # Auto-update connected peers
            st.session_state.peers[addr] = decoded_data.get("sender", "Unknown")

        except json.JSONDecodeError:
            st.session_state.messages.append(f"🛑 Received Invalid Data: {data.decode()}")

# Start background thread for receiving messages
threading.Thread(target=receive_messages, daemon=True).start()

# Streamlit UI
st.title("🌕 P2P Lunar Rover Communication")
st.write(f"**Your Rover ID:** `{ROVER_ID}` (Port: `{PORT}`)")

# Register a new peer
peer_ip = st.text_input("🔗 Enter Peer IP Address")
peer_port = st.number_input("🔗 Enter Peer Port", min_value=1024, max_value=65535, value=5005)

if st.button("Connect to Peer"):
    st.session_state.peers[(peer_ip, peer_port)] = f"Peer_{peer_ip}:{peer_port}"
    st.success(f"🔗 Connected to Peer {peer_ip}:{peer_port}")

# Send message section
message = st.text_input("💬 Enter message to send")

if st.button("Send Message"):
    if peer_ip and peer_port and message:
        send_to_peer(peer_ip, peer_port, message)

# Send sensor data
if st.button("Send Sensor Data to Earth Station"):
    send_to_ground_station()

# Display connected peers
st.subheader("🔗 Connected Peers")
for (ip, port), name in st.session_state.peers.items():
    st.write(f"🛰️ `{name}` at `{ip}:{port}`")

# Display received messages
st.subheader("📩 Messages")
for msg in st.session_state.messages:
    st.write(msg)
