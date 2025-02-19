import socket
import streamlit as st
import threading

# Dictionary to keep track of peers
peers = {}

# UDP Socket setup
UDP_IP = "127.0.0.1"  # Localhost for testing

# Function to listen for incoming messages
def listen_for_messages(peer_id, udp_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, udp_port))
    print(f"{peer_id} listening on port {udp_port}...")
    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            message = data.decode("utf-8")
            print(f"Received message from {addr}: {message}")
            sender_id = message.split(":")[0]
            if sender_id not in peers:
                peers[sender_id] = []
            peers[sender_id].append(message)

# Streamlit app for Peer 2
def main():
    st.title("P2P Communication Simulation - Peer 2")

    peer_id = st.text_input("Enter your Peer ID:", value="Peer2")
    udp_port = st.number_input("Enter your UDP Port:", value=5006, min_value=1024, max_value=65535)

    if peer_id:
        if peer_id not in peers:
            peers[peer_id] = []
            # Start the listener thread
            threading.Thread(target=listen_for_messages, args=(peer_id, udp_port), daemon=True).start()

        # Display the current state of peers excluding self
        st.write("Connected Peers:", [pid for pid in peers.keys() if pid != peer_id])

        if peers[peer_id]:
            st.subheader("Messages Received:")
            for msg in peers[peer_id]:
                st.write(msg)

        message = st.text_input("Send a message to another peer:")
        recipient = st.text_input("Recipient Peer ID:")
        if st.button("Send Message"):
            msg_to_send = f"{peer_id}: {message}"
            if recipient not in peers:
                peers[recipient] = []  # Register recipient if not already in peers
                st.warning(f"Recipient {recipient} added to peers.")
            else:
                st.info(f"Recipient {recipient} exists in peers.")

            # Determine the recipient's UDP port
            recipient_port = 5005 if recipient == "Peer1" else udp_port
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(msg_to_send.encode('utf-8'), (UDP_IP, recipient_port))
            st.success("Message sent!")

if __name__ == "__main__":
    main()
