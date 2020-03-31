import time
import smbus
from Agents import sensorsAgent

# i2c Params
address = 0x48
A2 = 0x43  # mods
A3 = 0x42  # mods
bus = smbus.SMBus(1)
A2_val = 0
A3_val = 0
A2_threshold = 3.0
A3_threshold = 3.0
last_touched = 0
pin_bit = 0

seats_value = {
    "frontR": None,
    "frontL": None
}

# GPIO pin numbers



# try:
#     import Adafruit_MPR121.MPR121 as MPR121
# except Exception as e:
#     print("ERROR: MPR121  package is not installed on this computer")
#     raise e

# gpio package import
try:
    import RPi.GPIO as GPIO
except Exception as e:
    print("ERROR: RPi package is not installed on this computer")
    raise e



class SensorsShield(sensorsAgent.SensorsAgent):

    def __init__(self, mqttAgent):
        # super(mqttAgent)
        self.agent = mqttAgent
        self.leftDoorPBN = 24
        self.rightDoorPBN = 23
        self.ignitionPBN = 25
        self.leftSBPBN = 27
        self.rightSBPBN = 17

        # GPIO initial values
        self.gpio_value = {
            self.leftDoorPBN: 0,
            self.rightDoorPBN: 0,
            self.ignitionPBN: 0,
            self.leftSBPBN: 0,
            self.rightSBPBN: 0
        }

        # MPR package import

        # Initialize communication with MPR121 using default I2C bus of device, and
        # default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
        self.bus = smbus.SMBus(1)
        #TODO
        # self.cap = MPR121.MPR121()
        # if not self.cap.begin():
        #     print('Error initializing MPR121.  Check your wiring!')
        #     sys.exit(1)
        # self.last_touched = self.cap.touched()





    def handle(self, pin):

        components = {
                self.leftDoorPBN: "FLDoor",
                self.rightDoorPBN: "FRDoor",
                self.ignitionPBN: "ignition",
                self.leftSBPBN: "FLSB",
                self.rightSBPBN: "FRSB"
            }

        pin_name = components.get(pin, "none")

        new_value = GPIO.input(pin)
        if self.gpio_value.get(pin) != new_value:
            self.gpio_value[pin] = new_value
            print("%s is: %s" % (pin_name, "closed" if new_value else "open"))
            self.updateMqttAgent(pin_name, new_value)


    def read_pcf8591(self):
        global A2_val
        global A3_val
        bus.write_byte(address, A2)
        A2_val = bus.read_byte(address) * 3.3 / 255
        time.sleep(0.1)
        bus.write_byte(address, A3)
        A3_val = bus.read_byte(address) * 3.3 / 255


    #    print ("A2: ", A2_val,"    --    A2 threshold: ", A2_threshold)
    #    print ("A3: ", A3_val,"    --    A3 threshold: ", A3_threshold)


    def update_seats(self):
        global A2_val
        global A3_val
        self.read_pcf8591()
        #    print ("A2: ", A2_val,"    --    A2 threshold: ", A2_threshold)
        #    print ("A3: ", A3_val,"    --    A3 threshold: ", A3_threshold)

        frontR = A2_val > A2_threshold
        if frontR != seats_value['frontR']:
            self.updateMqttAgent("FRseat", frontR)
            seats_value["frontR"] = frontR

        frontL = A3_val > A3_threshold
        if frontL != seats_value["frontL"]:
            self.updateMqttAgent("FLseat", frontL)
            seats_value["frontL"] = frontL





    def init_gpio(self):
        # gpio package import
        try:
            import RPi.GPIO as GPIO
        except Exception as e:
            print("ERROR: RPi package is not installed on this computer")
            raise e

        # setup hardware
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.leftDoorPBN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.rightDoorPBN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.ignitionPBN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.leftSBPBN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.rightSBPBN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # setup interrupts
        GPIO.add_event_detect(self.leftDoorPBN, GPIO.BOTH, self.handle)
        GPIO.add_event_detect(self.rightDoorPBN, GPIO.BOTH, self.handle)
        GPIO.add_event_detect(self.ignitionPBN, GPIO.BOTH, self.handle)
        GPIO.add_event_detect(self.leftSBPBN, GPIO.BOTH, self.handle)
        GPIO.add_event_detect(self.rightSBPBN, GPIO.BOTH, self.handle)


    def sync_gpio(self):

        # read the current data
        self.handle(self.leftDoorPBN)
        self.handle(self.rightDoorPBN)
        self.handle(self.ignitionPBN)
        self.handle(self.leftSBPBN)
        self.handle(self.rightSBPBN)







































    #
    # def handleLD(self, pin):
    #     new_value = GPIO.input(pin)
    #     if self.gpio_value.get(pin) != new_value:
    #         self.gpio_value[pin] = new_value
    #         print("%s is: %s" % ("leftDoor", "closed" if new_value else "open"))
    #         self.updateMqttAgent("leftDoor", new_value)
    #         # self.onChange(pin, new_value)
    #
    # def handleRD(self, pin):
    #     new_value = GPIO.input(pin)
    #     if self.gpio_value.get(pin) != new_value:
    #         self.gpio_value[pin] = new_value
    #         print("%s is: %s" % ("rightDoor", "closed" if new_value else "open"))
    #         self.updateMqttAgent("rightDoor", new_value)
    #         # self.onChange(pin, new_value)
    #
    # def handleIGN(self, pin):
    #     new_value = GPIO.input(pin)
    #     if self.gpio_value.get(pin) != new_value:
    #         self.gpio_value[pin] = new_value
    #         print("%s is: %s" % ("ignition", "closed" if new_value else "open"))
    #         self.updateMqttAgent("ignition", new_value)
    #         # self.onChange(pin, new_value)
    #
    # def handleLSB(self, pin):
    #     new_value = GPIO.input(pin)
    #     if self.gpio_value.get(pin) != new_value:
    #         self.gpio_value[pin] = new_value
    #         print("%s is: %s" % ("leftSB", "closed" if new_value else "open"))
    #         self.updateMqttAgent("leftSB", new_value)
    #         # self.onChange(pin, new_value)
    #
    # def handleRSB(self, pin):
    #     new_value = GPIO.input(pin)
    #     if self.gpio_value.get(pin) != new_value:
    #         self.gpio_value[pin] = new_value
    #         print("%s is: %s" % ("rightSB", "closed" if new_value else "open"))
    #         self.updateMqttAgent("rightSB", new_value)
    #         # self.onChange(pin, new_value)
    #
    #     # setup interrupts
    #     GPIO.add_event_detect(self.leftDoorPBN, GPIO.BOTH, self.handleLD)
    #     GPIO.add_event_detect(self.rightDoorPBN, GPIO.BOTH, self.handleRD)
    #     GPIO.add_event_detect(self.ignitionPBN, GPIO.BOTH, self.handleIGN)
    #     GPIO.add_event_detect(self.leftSBPBN, GPIO.BOTH, self.handleLSB)
    #     GPIO.add_event_detect(self.rightSBPBN, GPIO.BOTH, self.handleRSB)
