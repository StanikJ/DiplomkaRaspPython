import bluetooth
import threading
import time
import json
import RPi.GPIO as GPIO
import logging

from Config import Config
from DrawerPinEnum import DrawerPinEnum
from DrawerPinStateEnum import DrawerPinStateEnum
from DrawersService import DrawersService
from MessageModel import MessageModel
from BluetoothService import BluetoothService

config = Config()
drawerService = DrawersService([DrawerPinEnum.FIRST.value,
                                DrawerPinEnum.SECOND.value
                                ])
# pom = MessageModel.from_sock('{"macAddress": "AA:AA:AA:AA:AA:AA", "drawers": [0, 1, 1]}')
# print(pom)
# print(pom.mac_address)
# print(pom.drawers[0])
#
# print(pom.__dict__)
# message = MessageModel(config.my_mac_address,
#                        [DrawerPinStateEnum.ZERO, DrawerPinStateEnum.ZERO, DrawerPinStateEnum.ONE])
# print(message)
# print(message.to_json())
#
# exit(1)
bluetoothService = BluetoothService(config.server_mac_address, config.server_port, config.message_size)

logging.basicConfig(filename='logs.log', format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

logging.debug('This is a debug message')

isRunning: bool = True
isConnected: bool = False
send_state_thread = None

def send_state():
    while isRunning and isConnected:
        # TODO mozno bude treba doplnit try catch
        drawer_state = drawerService.get_drawers_state()
        message = MessageModel(config.my_mac_address, drawer_state)
        bluetoothService.send_data(message.to_json())
        time.sleep(config.sending_timeout)

while isRunning:
    try:
        if isConnected is False:
            bluetoothService.connect()
            # prehodit print na logger debug
            print('Connecting to server!')
            if bluetoothService.auth_connection(config.secret_key_message):
                raise Exception("Failed validation secret message.")

        # prehodit print na logger debug
        print('Connected to server!')
        isConnected = True

        send_state_thread = threading.Thread(target=send_state)
        send_state_thread.start()

        data = MessageModel.from_sock(bluetoothService.read_data())
        drawerService.set_drawers_sate(data.drawers)
        drawer_state = drawerService.get_drawers_state()
        message = MessageModel(config.my_mac_address, drawer_state)
        bluetoothService.send_data(message.to_json())

    except bluetooth.btcommon.BluetoothError as error:
        print('Connection error: ', error)
        logging.exception(error)

    except Exception as error:
        print('Connection error: ', error)
        logging.exception(error)
    finally:
        send_state_thread.join()
        print('Retrying in 5 seconds...')
        isConnected = False
        time.sleep(5)
