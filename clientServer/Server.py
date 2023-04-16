import bluetooth
import threading

from Config import Config
from BluetoothService import BluetoothService

config = Config()
bluetoothService = BluetoothService(Config.server_mac_address, Config.server_port, Config.message_size, Config.clients_queue)

def handle_client(client_sock, client_info):
    try:
        print()
    except:
        print()

def send_message(mac_address, message):
    print()

bluetoothService.bind()
bluetoothService.listen()
print("Waiting for connections...")

client_dict = {}

while True:
    #potvrd klienta
    client_sock, client_info = bluetoothService.accept()
    # bud vymen spravy a ak je to ok potvrd ho alebo to riesit v threade priamo
    client_dict[client_info[0]] = client_sock # store the MAC address in the dictionary macaddress = client socket podla toho budem komunikovat
    thread = threading.Thread(target=handle_client, args=(client_sock, client_info))
    thread.daemon = True
    thread.start()
