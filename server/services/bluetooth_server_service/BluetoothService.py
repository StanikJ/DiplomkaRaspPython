import bluetooth 
import threading

from MessageModel import MessageModel
from models.drawers_model import DrawersModel
from helpers.database import db
from Config import Config
from typing import List

class BluetoothService:

    def __init__(self, pa_config: Config):
        self._mac_address = pa_config.server_mac_address
        self._server_port = pa_config.server_port
        self._sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self._message_size = pa_config.message_size
        self._server_connection_validation_message = "Connection granted."
        self._pa_clients_queue = pa_config.clients_queue
        self._client_dict = {}

    def bind(self):
        self._sock.bind((self._mac_address, self._server_port))

    def listen(self):
        self._sock.listen(self._pa_clients_queue)

    def accept(self):
        self._sock.accept()

    def send_data_to_client(self, pa_drawer_state: List[int], pa_mac_addr: str ):
        for key, value in self._client_dict.items():
            if key is pa_mac_addr:
                client_sock = value
                break
        message = MessageModel(pa_mac_addr, pa_drawer_state)
        messageJson = message.to_json()
        self.send_data(messageJson, client_sock)

    @staticmethod
    def send_data(pa_message: str, pa_client_sock ):
        pa_client_sock.send(pa_message.encode())
        pass

    def read_data(self, pa_client_sock) -> str:
        msg: bytes = pa_client_sock.recv(self._message_size)
        return msg.decode()

    def auth_connection(self, pa_message: str, pa_client_sock) -> bool:
        if self.read_data(pa_client_sock) == pa_message:
            BluetoothService.send_data(self._server_connection_validation_message, pa_client_sock)
            return True

    def start_bluetooth_server(self):
        self.bind()
        self.listen()
        wait_client_thread = threading.Thread(target=self.wait_for_clients)
        wait_client_thread.start()

    def wait_for_clients(self):   #vlastne vlakno
        while True:
            client_sock, client_info = self.accept()
            if self.auth_connection(self._config.secret_key_message, client_sock):
                # bud vymen spravy a ak je to ok potvrd ho alebo to riesit v threade priamo
                self._client_dict[client_info[0]] = client_sock # store the MAC address in the dictionary macaddress = client socket podla toho budem komunikovat
                thread = threading.Thread(target=self.handle_client, args=(client_sock, client_info))
                thread.daemon = True
                thread.start()
            else:
                client_sock.close()

    def handle_client(self, client_sock, client_info):
        while True:
            try:
                data_from_client = self.read_data(client_sock)
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
                self._client_dict.pop(client_info[0], None)
                client_sock.close()
                return

    