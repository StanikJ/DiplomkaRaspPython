import json

#pip install RPi.GPIO
#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(channel, GPIO.OUT)
#GPIO.output(channel, state)
#flags set to remeber the last state of output pin

# some JSON:
#x =  { 
#    "macAddress":"xx:xx:xx:xx:xx", 
#    "drawer1":1, 
#    "drawer2":0, 
#    "drawer3": None, 
#    "drawer": None
#    }

# parse x:
#y = json.dumps(x)

# the result is a Python dictionary:
#print(y)

def create_json(num_rows):
    data = {
        "info1": "some specific information",
        "info2": "some more specific information",
        "rows": []
    }

    for i in range(num_rows):
        row = {
            "field1": "value1"
        }
        data["rows"].append(row)

    json_data = json.dumps(data)
    return json_data

json_data = create_json(5)
print(json_data)