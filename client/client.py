import bluetooth
import threading
import time
import json
import RPi.GPIO as GPIO
import logging

serverMacAddress = "00:1A:7D:DA:71:13"
serverPortNumber = 4
myMacAddress = "AA:AA:AA:AA:AA:AA"

validationMessage = "thisisasecretkeytovalidation"
drawer1Pin = 12
drawer2Pin = 18
pin1State = 0
pin2State = 0
size = 1024

connectionGrantedFlag = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(drawer1Pin, GPIO.OUT)
GPIO.setup(drawer2Pin, GPIO.OUT)
GPIO.output(drawer1Pin, pin1State)
GPIO.output(drawer2Pin, pin2State)

# Create logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# Create a file handler
fh = logging.FileHandler('mylog.txt')
fh.setLevel(logging.ERROR)
# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
# Add the file handler to the logger
logger.addHandler(fh)


def send_message():
    while True:
        dataForServer = {
            "MACaddr":myMacAddress,
            "drawer1":pin1State,
            "drawer2":pin2State
        }
        dataForServerJson = json.dumps(dataForServer)
        client_sock.send(dataForServerJson.encode())
        time.sleep(20)

def recieve_message():
    while True:
        dataForClientJson = client_sock.recv(size)
        dataForClient = json.loads(dataForClientJson.decode())
        if "drawer1" in dataForClient:
            pin1State = dataForClient["drawer1"]
            GPIO.output(drawer1Pin, pin1State)
        if "drawer2" in dataForClient:
            pin2State = dataForClient["drawer2"]
            GPIO.output(drawer2Pin, pin2State)

while True:
    try:
        client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        client_sock.connect((serverMacAddress, serverPortNumber))
        print('Connected to server!')
        client_sock.send(validationMessage.encode())
        validationResponse = client_sock.recv(size)
        validateTrim = validationResponse.decode()
        if validateTrim == "Connection granted.":
            connectionGrantedFlag = True
            send_thread = threading.Thread(target=send_message)
            receive_thread = threading.Thread(target=recieve_message)
            send_thread.start()
            receive_thread.start()

    except bluetooth.btcommon.BluetoothError as error:
        if connectionGrantedFlag == True:
            connectionGrantedFlag = False
            send_thread.join()
            receive_thread.join()
            print('Connection error: ', error)
            print('Retrying in 5 seconds...')
            logger.exception(error)
            time.sleep(5)
        else:
            print('Connection error: ', error)
            print('Retrying in 5 seconds...')
            logger.exception(error)
            time.sleep(5)
    except Exception as e:
        if connectionGrantedFlag == True:
            connectionGrantedFlag = False
            send_thread.join()
            receive_thread.join()
            print('Connection error: ', e)
            print('Retrying in 5 seconds...')
            logger.exception(e)
            time.sleep(5)
        else:
            print('Connection error: ', e)
            print('Retrying in 5 seconds...')
            logger.exception(e)
            time.sleep(5)
            # sam si vytvori mylog.txt file ale mozno mu bude treba pridat permissions na write 
