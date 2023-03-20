import bluetooth
import threading
import time

class BluetoothClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.connected = False
        self.send_thread = threading.Thread(target=self.send_message)
        self.receive_thread = threading.Thread(target=self.receive_message)

    def connect(self):
        try:
            self.sock.connect(self.server_address)
            self.connected = True
            print("Connected to server:", self.server_address)
            return True
        except bluetooth.BluetoothError as e:
            print("Error connecting to server:", e)
            return False

    def disconnect(self):
        if self.connected:
            self.sock.close()
            self.connected = False
            print("Disconnected from server:", self.server_address)

    def send_message(self):
        while self.connected:
            message = input("Enter message to send: ")
            if not message:
                continue
            self.sock.send(message)
            time.sleep(1)

    def receive_message(self):
        while self.connected:
            try:
                data = self.sock.recv(1024)
                if data:
                    print("Received message from server:", data.decode())
            except bluetooth.BluetoothError as e:
                print("Error receiving message:", e)
                self.disconnect()
                break

if __name__ == "__main__":
    server_address = ("<server bluetooth address>", 1)
    client = BluetoothClient(server_address)
    client.connect()
    if client.connected:
        client.send_thread.start()
        client.receive_thread.start()

#-------------------------------------------------------------
import bluetooth
import time

server_address = 'XX:XX:XX:XX:XX:XX'  # replace with server's MAC address
port = 3

while True:
    try:
        print('Attempting to connect to server...')
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((server_address, port))
        print('Connected to server!')

        while True:
            # Send a message to the server
            message = 'Hello, server!'
            sock.send(message.encode())

            # Wait for a response from the server
            data = sock.recv(1024)
            print('Received message from server:', data.decode())

            time.sleep(20)

    except bluetooth.btcommon.BluetoothError as error:
        print('Connection error:', error)
        print('Retrying in 5 seconds...')
        time.sleep(5)

#-------------------------------------------------------------
import RPi.GPIO as GPIO
import time

# Set up the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Initialize the state variable
pin_state = GPIO.LOW

try:
    while True:
        # Toggle the state of the output pin
        if pin_state == GPIO.LOW:
            GPIO.output(18, GPIO.HIGH)
            pin_state = GPIO.HIGH
        else:
            GPIO.output(18, GPIO.LOW)
            pin_state = GPIO.LOW

        # Wait for one second
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()