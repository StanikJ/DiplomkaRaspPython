from drawerEnum import DrawerEnum
import json

class MessageModel:
    def __init__(self, paMacAddress:str, paDrawers:DrawerEnum) -> None:
        self._macAddress = paMacAddress
        self._drawers = paDrawers

    @property
    def macAddress(self) -> str:
        return self._macAddress

    @property
    def drawers(self) -> DrawerEnum:
        return self._drawers

    @macAddress.setter
    def macAddress(self, paMacAddress:str):
        self._macAddress = paMacAddress
    
    @drawer.setter
    def drawers(self, paDrawers:DrawerEnum):
        self._drawers = paDrawers

    @staticmethod
    def fromSocket(socketMsg:str) -> MessageModel:
        pass

    def toSocket(self) -> str:
        return json.dumps(self.__dict__)