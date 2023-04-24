import RPi.GPIO as GPIO
from DrawerPinStateEnum import DrawerPinStateEnum
from DrawerPinEnum import DrawerPinEnum
from typing import List


class DrawersService:

    def __init__(self, pa_drawers_pins: List[int]):
            self._drawers_pins = pa_drawers_pins
            self._drawers_pins_state: List[DrawerPinStateEnum.value] = [None, None]#pa_drawers_pins
            self._default_pin_mode = GPIO.OUT
            self._default_pin_state = DrawerPinStateEnum.ZERO.value
            self._init_drawers()
            self.default_state()

    def _init_drawers(self):
        # log operation logging.debug('This is a debug message')
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for drawer in self._drawers_pins:
            # add logger index a pin drawera
            GPIO.setup(drawer, GPIO.OUT)#self._default_pin_mode)
        #GPIO.setup(5, GPIO.OUT)
        #GPIO.setup(6, GPIO.OUT)

    def default_state(self):
        # log operation
        for index,drawer in  enumerate(self._drawers_pins):
            # add logger index a pin drawera
            GPIO.output(drawer, self._default_pin_state)
            self._drawers_pins_state[index] = self._default_pin_state

    def set_drawers_state(self, pa_drawers_pin_states: List[int]):#DrawerPinStateEnum]):
        # log operation
        for index,drawer in enumerate(self._drawers_pins):
            # add logger index a pin drawera
            GPIO.output(drawer, pa_drawers_pin_states[index])
            self._drawers_pins_state[index] = pa_drawers_pin_states[index]
            #if drawer == DrawerPinEnum.FIRST.value:
            #    GPIO.output(23, pa_drawers_pin_states[index])
            #else:
            #    GPIO.output(24, pa_drawers_pin_states[index])
            #self._drawers_pins_state[index] = pa_drawers_pin_states[index]
            
    def get_drawers_state(self) -> List[DrawerPinStateEnum]:
        return self._drawers_pins_state
    
    
    