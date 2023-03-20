import bluetooth
import threading
import json
import time
import sqlite3

conn = sqlite3.connect('test.db')#vytvorit test.db v priecinku

conn.execute('''CREATE TABLE TEST
    (ID INT PRIMARY KEY NOT NULL,
    MACADDRESS TEXT NOT NULL,
    DRAWER1 INT NOT NULL,
    DRAWER2 INT NOT NULL);''')

validationMessage = "thisisasecretkeytovalidation"
validateTheConnection = "Connection granted."
serverMacAddress = "00:1A:7D:DA:71:13"
serverPortNumber = 4

dataForClient = {
            "MACaddr":myMacAddress,
            "drawer1":1,
            "drawer2":1
}

oneTimeMessageFlag = False

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(serverMacAddress, serverPortNumber)
server_sock.listen(1)

client_sock, client_info = server_sock.accept()
validationMessageFromClient = client_sock.recv(1024)
if validationMessageFromClient == validationMessage:
    client_sock.send(validateTheConnection)
    while True:
        dataFromClient = client_sock.recv(1024)
        dataFromClientJson = json.loads(dataFromClient)
        print(dataFromClient)
        conn.execute("INSERT INTO TEST (MACADDRESS,DRAWER1,DRAWER2) \
        VALUES (?, ?, ?)",(dataFromClientJson["MACaddr"],dataFromClientJson["drawer1"],dataFromClientJson["drawer2"]));
        conn.commit()
        time.sleep(5)
        dataForClientJson = json.dumps(dataForClient)
        client_sock.send(dataForClientJson)
else:
    client_sock.send("NO!")
    client_sock.close()
