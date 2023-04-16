import bluetooth
import threading
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exampleForD.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret_key'
db = SQLAlchemy(app)

class DataFromClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    MACaddr = db.Column(db.String(80), unique=True, nullable=False)
    drawer1 = db.Column(db.Integer, nullable=False)
    drawer2 = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, MACaddr, drawer1, drawer2):
        self.MACaddr = MACaddr
        self.drawer1 = drawer1
        self.drawer2 = drawer2

    def update_timestamp(self):
        self.time = datetime.utcnow()

class DataToClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    MACaddr = db.Column(db.String(80), unique=True, nullable=False)
    drawer1 = db.Column(db.Integer, nullable=False)
    drawer2 = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, MACaddr, drawer1, drawer2):
        self.MACaddr = MACaddr
        self.drawer1 = drawer1
        self.drawer2 = drawer2

    def update_timestamp(self):
        self.time = datetime.utcnow()

validation_message = "nepamatam si"
validate_the_connection = "Connection granted."
server_mac_address = "E4:5F:01:54:77:74"
server_port = 4
size = 1024

#funkcia pre webserver 
def function_to_check_if_clients_work():
    time_values = DataFromClient.query(DataFromClient.time).all()
    now = datetime.utcnow()
    now_extract_minute = now - timedelta(minutes=1)

    for value in time_values:
        if now_extract_minute > value:
            row_to_delete = db.query.filter_by(time=value).first()
            db.session.delete(row_to_delete)
            db.session.commit()

clients = []

def handle_client(client_sock, client_info):
    try:
        print("Accepted connection from", client_info)
        validation_message_from_client = client_sock.recv(size)
        message_to_validate = validation_message_from_client.decode()
        if validation_message == message_to_validate:
            client_sock.send(validate_the_connection.encode())
            try:
                data = client_sock.recv(size)
                data_json = json.loads(data.decode())
                drawer1, drawer2 = data_json['drawers']
                data_from_client = DataFromClient.query.filter_by(MACaddr=data_json["macAddress"]).first()
                if data_from_client:
                    data_from_client.drawer1 = drawer1
                    data_from_client.drawer2 = drawer2
                else:
                    data_from_client = DataFromClient(MACaddr=data_json["macAddress"], drawer1=drawer1, drawer2=drawer2)
                    db.session.add(data_from_client)

                data_from_client.update_timestamp()
                db.session.commit()
            except:

            else:
            #rozparsuj json data a vytvor zanam v DB s MAC addr, drawer1 a drawer2 a aj v druhej DB rovnaky zanam
            # tuto hned pockaj na data a vytvor v DB zaznam potom skoc do while a tam cakaj na update z db alebo z update z klienta
            while True:  #tento while neviem ako ma byt aby iba cakal ze ci nieco pride alebo sa updatne row v DB
                if data: # ak sa updatne row v DB odosli JSON na clienta
                    client_sock
                elif data: 
                    client_sock
        else:
            client_sock.close()
            threading.Thread(target=threading.Thread._delete, args=(threading.get_ident(),)).start() # toto zabije vlakno ako same seba

        data = "Hello, world!"
        client_sock.send(data.encode())
        while True:
            data = client_sock.recv(1024).decode()
            if not data:
                break
            print("Received data from", client_info, ":", data)
            client_sock.send(data.encode())
    except Exception as e:
        print("Exception in client thread:", e)
    finally:
        client_sock.close()
        print("Connection closed with", client_info)
        # Remove the client from the dictionary when it disconnects
        mac_address = client_dict.pop(client_info[0], None)
        if mac_address is not None:
            print("Removed client with MAC address", mac_address)

def send_message(mac_address, message):
    client_sock = None
    for client_info, client_mac_address in client_dict.items():
        if client_mac_address == mac_address:
            client_socket = clients[client_info]
            break
    if client_sock is None:
        print("No client with MAC address", mac_address, "found")
        return
    try:
        client_sock.send(message.encode())
        print("Message sent to client with MAC address", mac_address)
    except Exception as e:
        print("Exception while sending message to client with MAC address", mac_address, ":", e)

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind((server_mac_address, server_port))
server_sock.listen(1) #toto cislo je ze kolko clientov moze cakat v rade na pripojenie

print("Waiting for connections...")

clients = {}
client_dict = {}
while True:
    client_sock, client_info = server_sock.accept()
    clients[client_info] = client_sock
    client_dict[client_info[0]] = client_info[0] # store the MAC address in the dictionary
    thread = threading.Thread(target=handle_client, args=(client_sock, client_info))
    thread.daemon = True
    thread.start()
