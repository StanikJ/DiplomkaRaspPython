import bluetooth
import threading
import time
import json
import RPi.GPIO as GPIO

#instead of RFCOMM use BLE library for security, cryptography,
#public-private key

#server multiple threads for each socket


serverMacAddress = "00:1A:7D:DA:71:13"
serverPortNumber = 4
myMacAddress = "AA:AA:AA:AA:AA:AA"

validationMessage = "thisisasecretkeytovalidation"
drawer1Pin = 12
drawer2Pin = 18
pin1State = 0
pin2State = 0

connectionGrantedFlag = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(drawer1Pin, GPIO.OUT)
GPIO.setup(drawer2Pin, GPIO.OUT)
GPIO.output(drawer1Pin, pin1State)
GPIO.output(drawer2Pin, pin2State)



def send_message():
    while True:
        dataForServer = {
            "MACaddr":myMacAddress,
            "drawer1":pin1State,
            "drawer2":pin2State
        }
        dataJsonForServer = json.dumps(dataForServer)
        client_sock.send(dataJsonForServer)
        time.sleep(20)

def recieve_message():
    while True:
        dataJsonForClient = client_sock.recv(1024)
        dataForClient = json.loads(dataJsonForClient.decode('utf-8'))
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
        client_sock.send(validationMessage)
        validationResponse = client_sock.recv(1024)
        validateTrim = validationResponse.decode('utf-8')
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
            print('Connection error:', error)
            print('Retrying in 5 seconds...')
            time.sleep(5)
        else:
            print('Connection error:', error)
            print('Retrying in 5 seconds...')
            time.sleep(5)
