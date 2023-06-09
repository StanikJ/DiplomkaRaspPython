import bluetooth
import threading

from Config import Config
from BluetoothService import BluetoothService
from MessageModel import MessageModel

config = Config()
bluetoothService = BluetoothService(config.server_mac_address, config.server_port, config.message_size, config.clients_queue)

def handle_client(client_sock, client_info):
    try:
        data_from_client = bluetoothService.read_data()
        message = MessageModel.from_sock(data_from_client)
        
    except:
        print()
        #ak sa komunikacia potvrdi az vo vlakne tak potom tu bude socket.declain a musi tu vlakno zabit same seba
        #client_sock.close()
        #print("Connection closed with", client_info)
        # Remove the client from the dictionary when it disconnects
        #mac_address = client_dict.pop(client_info[0], None)
        #if mac_address is not None:
            #print("Removed client with MAC address", mac_address)

def send_message(mac_address, message):
    print()

def recieve_message(mac_address, message):
    print()

bluetoothService.bind()
bluetoothService.listen()
print("Waiting for connections...")

client_dict = {}

while True:
    #potvrd klienta
    client_sock, client_info = bluetoothService.accept()
    if bluetoothService.auth_connection(config.secret_key_message):
        # bud vymen spravy a ak je to ok potvrd ho alebo to riesit v threade priamo
        client_dict[client_info[0]] = client_sock # store the MAC address in the dictionary macaddress = client socket podla toho budem komunikovat
        thread = threading.Thread(target=handle_client, args=(client_sock, client_info))
        thread.daemon = True
        thread.start()
    else:
        client_sock.close()
