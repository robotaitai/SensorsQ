
import json
import logging
import uuid

sensor_message = {}
sensor_message_json = {}

class MqttAgent:

    def __init__(self, args):

        self.args = args
        self.client = None
        self.connected_to_mqtt = None


        # DO NOT REMOVE: for debug purposes
        # from pudb import set_trace

        self.connection_error_strings = {
            0: "Connection successful",
            1: "Connection refused, incorrect protocol version",
            2: "Connection refused, invalid client identifier",
            3: "Connection refused, server unavailable",
            4: "Connection refused, bad username or password",
            5: "Connection refused, not authorised"
        }
        self.init_mqtt()



    def publish(self, message_name, message_value):

        # set_trace()
        try:

            self.sensor_message = {
                "input_id": str(uuid.uuid4()),
                message_name: message_value
            }

            self.sensor_message_json = json.dumps(self.sensor_message)
            print("publishing:")
            print(json.dumps(self.sensor_message, sort_keys=True, indent=4))

            self.client.publish("sensors", self.sensor_message_json)

        except Exception as e:
            logging.exception(e)
        finally:
            print("-----------------------------------------")



    def lstr(self, value):
        return str(value).lower()

    def publish_door_message(self, door_name, is_open):
        self.publish(
            "doors_open",
            {
                door_name: self.lstr(is_open)
            }
        )


    def publish_seat_message(self, seat_name, is_occupied):
        self.publish(
            "seats_occupied",
            {
                seat_name: self.lstr(is_occupied)
            }
        )


    def publish_seatbelt_message(self, seat_name, is_fastened):
        self.publish(
            "seatbelts_buckled",
            {
                seat_name: self.lstr(not is_fastened)
            }
        )

    def publish_steering_message(self, pin_num, touched):
        self.publish(
            "external" ,{"steering_wheel" :{"touch":
                {
                    pin_num: self.lstr(touched)
                }}}
        )


    ##################################################################################################
    ## GPIO-MQTT hooks
    ##################################################################################################


    def on_engine_gpio_changed(self, is_off):
        self.publish(
            "engine",
            {
                "engine_on": self.lstr(not is_off)
            }
        )


    def on_driver_door_gpio_changed(self, is_open):
        self.publish_door_message("front_left", is_open)


    def on_passenger_door_gpio_changed(self, is_open):
        self.publish_door_message("front_right", is_open)


    def on_driver_seat_gpio_changed(self, is_occupied):
        self.publish_seat_message("front_left", is_occupied)


    def on_passenger_seat_gpio_changed(self, is_occupied):
        self.publish_seat_message("front_right", is_occupied)


    def on_driver_seatbelt_gpio_changed(self, is_unfastened):
        self.publish_seatbelt_message("front_left", not is_unfastened)


    def on_passenger_seatbelt_gpio_changed(self, is_unfastened):
        self.publish_seatbelt_message("front_right", not is_unfastened)


    def on_steering_touch_changed(self, pin_num, touched):
        self.publish_steering_message(pin_num, touched)


    ##################################################################################################
    ## GPIO-MQTT hooks
    ##################################################################################################


    def get_error_string(self, rc):
        if rc == 1: return


    def on_connect(self, client, userdata, flags, rc):
        self.connected_to_mqtt = (rc == 0)

        if self.connected_to_mqtt:
            print("MQTT connected")
        else:
            print("ERROR: %s" % self.connection_error_strings[rc])


    def on_disconnect(self, client, userdata, flags, rc=0):
        print("MQTT disconnected")



    def init_mqtt(self):
        # global client
        # mqtt package import
        try:
            import paho.mqtt.client as mqtt
        except Exception as e:
            print("ERROR: paho-mqtt package is not installed on this computer")
            print("       try to install it by callind: 'pip install paho-mqtt'")
            raise e


        # global args

        # setup mqtt
        self.host = self.args.mqtt
        print("Connecting to MQTT on %s..." % self.host)
        self.client = mqtt.Client("rpi_hw_sensors")
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.connect_started = False
        while not self.connect_started:
            try:
                self.client.connect(self.host)
                self.connect_started = True
            except Exception as e:
                pass

        self.client.loop_start()

