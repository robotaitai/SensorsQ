
import can
import threading
import time
from Agents.sensorsAgent import SensorsAgent





class CANShield(SensorsAgent):

    def __init__(self, mqttAgent):
        bus = can.Bus(interface='socketcan', channel='can0', receive_own_messages=True)
        notifier =can.Notifier(bus, [can.Logger("recorded.log"), can.Parser(self)])
        print("CAN Thread started")
        self.agent = mqttAgent

    def sync_gpio(self):
        pass

    # threading.Thread(target=CANShield.update_can()).start()


    @staticmethod
    def update_can():
        bus = can.Bus(interface='socketcan', channel='can0', receive_own_messages=True)
        can.Notifier(bus, [can.Logger("recorded.log"), can.Printer()])
        print("CAN Thread started")

    # @staticmethod
    def onChange(self, need_to_update):
        while not self.agent.connected_to_mqtt:
            time.sleep(100)
        for key in need_to_update:
            print("update on: ", key," now: " ,need_to_update[key] )
            SensorsAgent.updateMqttAgent(self.agent, key, need_to_update[key])