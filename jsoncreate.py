import json
import RPi.GPIO as GPIO

pocetZasuviek = 3
zasuvka1 = 5
zasuvka2 = 6
zasuvka3 = 7

zasuvkyPins = [zasuvka1, zasuvka2, zasuvka3]

def create_json(num_fields, gpio_pins):
    GPIO.setmode(GPIO.BCM)
    data = {
        "info1": "some specific information",
        "info2": "some more specific information",
    }

    # Read data from GPIO pins and include in field values
    for i in range(num_fields):
        GPIO.setup(gpio_pins[i], GPIO.IN)
        data["Zasuvka{}".format(i+1)] = GPIO.input(gpio_pins[i])

    json_data = json.dumps(data)
    GPIO.cleanup()
    return json_data

json_data = create_json(pocetZasuviek, zasuvkyPins)
print(json_data)