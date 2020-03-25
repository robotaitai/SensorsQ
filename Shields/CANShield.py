
import can
import threading
from Agents import sensorsAgent





class CANShield(sensorsAgent.SensorsAgent):

    def __init__(self, mqttAgent):
        bus = can.Bus(interface='socketcan', channel='can0', receive_own_messages=True)
        notifier =can.Notifier(bus, [can.Logger("recorded.log"), can.Parser()])
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

