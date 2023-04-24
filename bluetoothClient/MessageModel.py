from DrawerPinStateEnum import DrawerPinStateEnum
import json
from typing import List


class MessageModel:
    def __init__(self, pa_mac_address: str, pa_drawers: List[DrawerPinStateEnum]) -> None:
        self._macAddress = pa_mac_address
        self._drawers = pa_drawers

    @property
    def mac_address(self) -> str:
        return self._macAddress

    @property
    def drawers(self) -> List[DrawerPinStateEnum]:
        return self._drawers

    @mac_address.setter
    def mac_address(self, pa_mac_address: str):
        self._macAddress = pa_mac_address

    @drawers.setter
    def drawers(self, pa_drawers: List[DrawerPinStateEnum]):
        self._drawers = pa_drawers

    @staticmethod
    def from_sock(pa_message: str):
        data_dict = json.loads(pa_message)
        drawers_state: List[DrawerPinStateEnum] = []
        for drawer in data_dict['drawers']:
            drawers_state.append(drawer)
            #if drawer == 1:
            #    drawers_state.append(DrawerPinStateEnum.ONE.value)
            #else:
            #    drawers_state.append(DrawerPinStateEnum.ZERO.value)
        return MessageModel(data_dict['macAddress'], drawers_state)

    def to_json(self) -> str:
        drawers_state = []
        for drawer in self._drawers:
            #drawers_state.append(drawer.value)
            if drawer == DrawerPinStateEnum.ONE.value:
                drawers_state.append(1)
            else:
                drawers_state.append(0)
        return json.dumps({'macAddress': self._macAddress, 'drawers': drawers_state})