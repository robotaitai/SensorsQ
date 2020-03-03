

import sys
import time
import threading
from Agents import mqttAgent
from Shields import sensorsShield
import argparse


#IP = "192.168.1.16"  # ofri
IP = "192.168.100.181" #bench
# IP = "192.168.10.106"



def check_user_input():
    global exit_program

    var = ""
    while not exit_program:
        var = raw_input("")
        exit_program = (var == 'q' or var == 'Q')

def update_steering_touch(last_touched):
    #    global last_touched
    sensor.current_touched = sensor.cap.touched()

    for i in range(12):
        # Each pin is represented by a bit in the touched value.  A value of 1
        # means the pin is being touched, and 0 means it is not being touched.
        pin_bit = 1 << i
        if sensor.current_touchedx & pin_bit and not sensor.last_touched & pin_bit:
            print('{0} touched!'.format(i))
            agent.on_steering_touch_changed(i, 1)

        if not sensor.current_touched & pin_bit and sensor.last_touched & pin_bit:
            print('{0} released!'.format(i))
            agent.on_steering_touch_changed(i, 0)
    last_touched = sensor.current_touched
    return last_touched


## MAIN CODE
exit_program = False

parser = argparse.ArgumentParser(description='RPi HW Sensors Controller')
parser.add_argument('--mqtt', default=IP, type=str, help='MQTT broker IP address')
parser.add_argument('--service', help='run in service mode (no used input)', action='store_true')
args = parser.parse_args()

agent = mqttAgent.MqttAgent(args)

# agent.init_mqtt()
sensor = sensorsShield.SensorsShield(agent)
sensor.init_gpio()



while agent.connected_to_mqtt is None:
    pass

if agent.connected_to_mqtt:
    sensor.sync_gpio()
    if 'pudb' in sys.modules:
        if not agent.args.service:
            print("Press CTRL+C to stop...")

        while True:
            sensor.update_seats()
          #  last_touched = sensor.update_steering_touch(last_touched) #TODO
            time.sleep(0.1)
    else:
        if not agent.args.service:
            print("Press q+Enter to stop...")
            threading.Thread(target=check_user_input).start()

        while not exit_program:
            sensor.update_seats()
         #   last_touched = sensor.SensorsShield.update_steering_touch(last_touched)
            time.sleep(0.1)