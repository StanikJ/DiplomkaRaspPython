import bluetooth

# create a list to store MAC addresses
clients = []

def handle_client(client_socket, client_address):
    clients.append(client_address[0])
    print(f"Connected clients: {clients}")
    
    client_socket.send("Welcome to the Bluetooth server!")
    
    # wait for client to disconnect
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            # process client data (replace this with your own code)
        except bluetooth.BluetoothError:
            break

    clients.remove(client_address[0])
    
    client_socket.close()


server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1 
server_socket.bind(("", port))
server_socket.listen(5)


clients_mac_addresses = {}
clients_sockets = {}
print("Waiting for Bluetooth connections...")

while True:
    client_socket, client_address = server_socket.accept()
    clients_sockets[client_address] = client_sock
    clients_mac_addresses[client_address[0]] = client_address[0] # store the MAC address in the dictionary
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()