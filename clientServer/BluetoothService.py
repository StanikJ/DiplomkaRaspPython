import bluetooth 


class BluetoothService:

    def __init__(self, pa_mac_address: str, pa_server_port: int, pa_message_size: int, pa_clients_queue: int):
        self._mac_address = pa_mac_address
        self._server_port = pa_server_port
        self._sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self._message_size = pa_message_size
        self._server_connection_validation_message = "Connection granted."
        self._pa_clients_queue = pa_clients_queue

    def bind(self):
        self._sock.bind((self._mac_address, self._server_port))

    def listen(self):
        self._sock.listen(self._pa_clients_queue)

    def send_data(self, pa_message: str):
        self._sock.send(pa_message.encode())
        pass

    def read_data(self) -> str:
        msg: bytes = self._sock.recv(self._message_size)
        return msg.decode()

    def auth_connection(self, pa_message: str) -> bool:
        self.send_data(pa_message)
        return self.read_data() != self._server_connection_validation_message
