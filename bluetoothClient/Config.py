class Config:

    def __init__(self):
        self._server_mac_address = "E4:5F:01:54:77:74"
        self._server_port = 4
        self._my_mac_address = "B8:27:EB:64:7A:CF"
        self._secret_key_message = "thisisasecretkeytovalidation"
        self._message_size = 1024
        self._sending_timeout = 20

    @property
    def server_mac_address(self) -> str:
        return self._server_mac_address

    @property
    def server_port(self) -> int:
        return self._server_port

    @property
    def my_mac_address(self) -> str:
        return self._my_mac_address

    @property
    def secret_key_message(self) -> str:
        return self._secret_key_message

    @property
    def message_size(self) -> int:
        return self._message_size

    @property
    def sending_timeout(self) -> int:
        return self._sending_timeout