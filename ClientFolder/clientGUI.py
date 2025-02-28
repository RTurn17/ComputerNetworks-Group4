import streamlit as st
import socket
import threading
import json
import os  # Import the os module for checking file existence
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
#sock.bind(("", PORT))

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

from PIL import Image
from PIL import Image
import base64
from io import BytesIO

# Function to convert image to base64
def img_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Load the image
image_path = r"C:\Users\aneob\Downloads\image.png"
img = Image.open(image_path)

# Set background image
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('data:image/png;base64,{img_to_base64(img)}');
        background-size: cover;
        background-position: center center;
    }}
    /* Custom title style */
    .title {{
        font-size: 36px;
        color: white;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        padding-top: 100px;
    }}
    /* Custom text style with Courier New font */
    .text1 {{
        font-size: 12px;
        color: white;
        font-family: 'Courier New', Courier, monospace;
        text-align: left;
        padding-left: 75px;
    }}
    /* New custom normal text with Arial font, bold and padding below title/header */
    .custom-text {{
        font-size: 12px;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        text-align: left;
        padding-left: 170px;
        padding-top: 1px;   /* Padding to push it down below header */
    }}
    /* Connected Peers Styling */
    .peer-card {{
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        padding: 10px;
        margin: 10px;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }}
    .peer-card:hover {{
        transform: scale(1.05);
    }}
    .peer-ip {{
        font-size: 14px;
        color: white;
    }}
    .peer-name {{
        font-size: 16px;
        font-weight: bold;
        color: white;
    }}
    /* Blinking effect for sending data */
    @keyframes blink {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
    }}
    .blinking {{
        animation: blink 1s infinite;
        color: green;
        font-weight: bold;
    }}
    /* Smaller font size for sending data status */
    .small-text {{
        font-size: 15px;
    }}
    /*Error image styling */
    .error-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);  /* Semi-transparent background */
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10;
    }}
    .error-image {{
    width: 20%;  /* Adjust width to make the image smaller */
    max-width: 100px;  /* Maximum width for the image */
    max-height: 70px;  /* Maximum height for the image */
}}
    .error-button {{
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 20px;
        color: white;
        background-color: red;
        padding: 10px;
        border: none;
        cursor: pointer;
    }}
    
    </style>
    """,
    unsafe_allow_html=True)

# Custom Title
st.markdown("<h1 class='title'>  Lunar Rover Communication</h1>", unsafe_allow_html=True)
# Custom Text
st.markdown("<p class='text1'>Welcome to the lunar rover GUI! Let's explore the moon.</p>", unsafe_allow_html=True)
# New Text with dynamic ROVER_ID and PORT, and padding below header
st.markdown(
    f"<p class='custom-text'><b>Your Rover ID:</b> <code>{ROVER_ID}</code> (Port: <code>{PORT}</code>)</p>",
    unsafe_allow_html=True
)

# Register a new peer
peer_ip = st.text_input("Enter Peer IP Address")
peer_port = st.number_input("Enter Peer Port", min_value=1024, max_value=65535, value=5005)

if st.button("Connect to Peer"):
    st.session_state.peers[(peer_ip, peer_port)] = f"Peer_{peer_ip}:{peer_port}"
    st.success(f"Connected to Peer {peer_ip}:{peer_port}")

# Display connected peers in styled cards
st.write("🔗 **Connected Peers:**")
for (ip, port), name in st.session_state.peers.items():
    st.markdown(f"""
        <div class="peer-card">
            <span class="peer-name">{name}</span>
            <span class="peer-ip">{ip}:{port}</span>
        </div>
    """, unsafe_allow_html=True)

st.write("📩 **Status:**")
# Set up session state for tracking the current message
if 'current_status' not in st.session_state:
    st.session_state.current_status = "Gathering Data..."

# Display the current status message dynamically with smaller font size and normal text
status_message = st.empty()  # Placeholder for dynamic updates
status_message.markdown(f"<p class='small-text'>{st.session_state.current_status}</p>", unsafe_allow_html=True)

# Simulate receiving a request to update status from another peer
if st.button("Request Data from Lunar Vehicle"):
    # Change status to "Processing Request..." and make it blink with smaller text
    st.session_state.current_status = "Processing Request..."
    status_message.markdown(f"<p class='blinking small-text'>{st.session_state.current_status}</p>", unsafe_allow_html=True)
    
    # Simulate a delay while processing the request
    time.sleep(2)

    # Change status to "Sending Data..." and make it blink with smaller text
    st.session_state.current_status = "Sending Data..."
    status_message.markdown(f"<p class='blinking small-text'>{st.session_state.current_status}</p>", unsafe_allow_html=True)
    
    # Simulate data transfer delay
    time.sleep(3)

    # Change status to "Data Sent" with smaller text
    st.session_state.current_status = "Data Sent!"
    status_message.markdown(f"<p class='small-text'>{st.session_state.current_status}</p>", unsafe_allow_html=True)

    # Return to the default "Gathering Data" message after a short delay
    time.sleep(2)
    st.session_state.current_status = "Gathering Data"
    status_message.markdown(f"<p class='small-text'>{st.session_state.current_status}</p>", unsafe_allow_html=True)

# Set up session state for tracking the current message and error state
if 'current_status' not in st.session_state:
    st.session_state.current_status = "Gathering Data"
if 'error_active' not in st.session_state:
    st.session_state.error_active = False

# Function to toggle error state and show image
def toggle_error():
    st.session_state.error_active = not st.session_state.error_active

# Button to toggle error state
error_button = st.button("ERROR" if not st.session_state.error_active else "Cancel Error", key="error_button", on_click=toggle_error)

# Path to your image in the Downloads folder
image_path = r"C:\Users\aneob\Downloads\errormessage.jpg"  # Exact path to your image

# Display error image if error state is active
if st.session_state.error_active:
    if os.path.exists(image_path):
        error_image = Image.open(image_path)
        st.image(error_image, use_container_width=True, caption="Hardware Malfunction/Out of sight!!", output_format="JPEG")
    else:
        st.error("Error image not found. Please make sure the image exists in your Downloads folder.")
