import bluetooth
import threading

from helpers.database import db

from Config import Config
from BluetoothService import BluetoothService
from MessageModel import MessageModel
from models.drawers_model import DrawersModel

config = Config()
bluetoothService = BluetoothService(config.server_mac_address, config.server_port, config.message_size, config.clients_queue)

def handle_client(client_sock, client_info):
    while True:
        try:
            data_from_client = bluetoothService.read_data(client_sock)
            messageModel = MessageModel.from_sock(data_from_client)
            drawerModel = DrawersModel.query.filter_by(MACaddr=messageModel.mac_address).first()
            if drawerModel is not None:
                for drawer, drawerIndex in enumerate(messageModel.drawers):
                    if drawerIndex == 0:
                        drawerModel.drawer1 = drawer.value
                    if drawerIndex == 1:
                        drawerModel.drawer2 = drawer.value
                db.session.commit()
                continue
            
            drawerModel = DrawersModel(MACaddr=messageModel.mac_address, drawer1=messageModel.drawers[0].value, drawer2=messageModel.drawers[1].value)
            db.session.add(drawerModel)#ak vrati pitchovinu zmenit nazov
            db.session.commit() 
        except:
            print()
            client_dict.pop(client_info[0], None)
            client_sock.close()
            return
            #ak sa komunikacia potvrdi az vo vlakne tak potom tu bude socket.declain a musi tu vlakno zabit same seba
            #client_sock.close()
            #print("Connection closed with", client_info)
            # Remove the client from the dictionary when it disconnects
            #mac_address = client_dict.pop(client_info[0], None)
            #if mac_address is not None:
                #print("Removed client with MAC address", mac_address)

bluetoothService.bind()
bluetoothService.listen()
print("Waiting for connections...")

client_dict = {}

while True:
    #potvrd klienta
    client_sock, client_info = bluetoothService.accept()
    if bluetoothService.auth_connection(config.secret_key_message, client_sock):
        # bud vymen spravy a ak je to ok potvrd ho alebo to riesit v threade priamo
        client_dict[client_info[0]] = client_sock # store the MAC address in the dictionary macaddress = client socket podla toho budem komunikovat
        thread = threading.Thread(target=handle_client, args=(client_sock, client_info))
        thread.daemon = True
        thread.start()
    else:
        client_sock.close()
