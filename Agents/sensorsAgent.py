class SensorsAgent:

    def __init__(self, mqttAgent):

        self.agent = mqttAgent #calling MQTT agent for some publishments later
        self.leftDoorPBN = None
        self.rightDoorPBN = None
        self.ignitionPBN = None
        self.leftSBPBN = None
        self.rightSBPBN = None


    def updateMqttAgent(self, component, value):

        #implementation of switch-cases in Python

        switcher = {
            "leftDoor": self.agent.on_driver_door_gpio_changed,
            "rightDoor": self.agent.on_passenger_door_gpio_changed,
            "ignition": self.agent.on_engine_gpio_changed,
            "leftSB": self.agent.on_driver_seatbelt_gpio_changed,
            "rightSB": self.agent.on_passenger_seatbelt_gpio_changed,
            "FRseat": self.agent.on_passenger_seat_gpio_changed,
            "FLseat": self.agent.on_driver_seat_gpio_changed
        }
        call = switcher.get(component, lambda: "invalid argument")
        call(value==0)



    def handle(self):
        raise Exception("you need to define handle function!!!!")

