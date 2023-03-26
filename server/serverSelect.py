import bluetooth
import json
import select
# Set server Bluetooth address and port
server_mac = "00:11:22:33:44:55"
server_port = 1
# Create Bluetooth socket and bind to server address/port
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind((server_mac, server_port))
server_sock.listen(1)
print("Waiting for client connection...")
# Create list to keep track of connected clients
clients = []
# Define function to send message to client with given MAC address
def send_message(mac, message):
    for client in clients:
        if client['mac'] == mac:
            client['sock'].send(message.encode())
while True:
    # Use select to monitor server socket for new connections and client sockets for incoming messages
    readable, _, _ = select.select([server_sock] + [client['sock'] for client in clients], [], [])
    for sock in readable:
        # If server socket is readable, accept new client connection and add to list of clients
        if sock == server_sock:
            client_sock, client_info = server_sock.accept()
            clients.append({'sock': client_sock, 'info': client_info, 'mac': None})
            print(f"New client connected: {client_info}")
        # If client socket is readable, receive message and process
        else:
            client = [client for client in clients if client['sock'] == sock][0]
            data = sock.recv(1024).decode()
            print(f"Received message from {client['info']}: {data}")
            # Parse JSON message and extract MAC address and message content
            try:
                message = json.loads(data)
                mac = message['mac']
                content = message['content']
                # Update client's MAC address if not already set
                if client['mac'] is None:
                    client['mac'] = mac
                # Send message to client with specified MAC address
                send_message(mac, content)
            except:
                print("Invalid JSON message format")
                continue
# Close all sockets and exit program
for client in clients:
    client['sock'].close()
    
server_sock.close()
print("Server shutdown")