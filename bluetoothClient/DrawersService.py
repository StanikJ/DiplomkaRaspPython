# import RPi.GPIO as GPIO
from client.DrawerPinStateEnum import DrawerPinStateEnum
from typing import List


class DrawersService:

    def __init__(self, pa_drawers_pins: List[int]):
        self._drawers_pins = pa_drawers_pins
        self._drawers_pins_state: List[DrawerPinStateEnum.value] = pa_drawers_pins
        self._default_pin_mode = GPIO.OUT
        self._default_pin_state = DrawerPinStateEnum.ZERO
        self._init_drawers()
        self.default_state()

    def _init_drawers(self):
        # log operation logging.debug('This is a debug message')
        GPIO.setmode(GPIO.BCM)
        for drawer in self._drawers_pins:
            # add logger index a pin drawera
            GPIO.setup(drawer, self._default_pin_mode)

    def default_state(self):
        # log operation
        for index,drawer in  enumerate(self._drawers_pins):
            # add logger index a pin drawera
            GPIO.output(drawer, self._default_pin_state.value)
            self._drawers_pins_state[index] = self._default_pin_state

    def set_drawers_sate(self, pa_drawers_pin_states: List[DrawerPinStateEnum]):
        # log operation
        for index, drawer in enumerate(self._drawers_pins):
            # add logger index a pin drawera
            GPIO.output(drawer, pa_drawers_pin_states[index].value)
            self._drawers_pins_state[index].value = pa_drawers_pin_states[index].value

    def get_drawers_state(self) -> List[DrawerPinStateEnum]:
        return self._drawers_pins_state
