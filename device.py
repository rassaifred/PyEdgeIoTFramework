# ToDo: add mqtt local
# ToDo: add PubSub

import os
from threading import Thread
from pubsub import pub
import sentry_sdk
from sentry_sdk import configure_scope
from modules.mqtt import MqttLocalClient
from modules.power.PyPower import PyPower
from modules.radar.PyPing import PyPing
from modules.oled.PyOled import PyOled
from modules.buzzer import PyBuzzer


buzzGpio = 27


class DeviceEdge(Thread):

    # PubSub TOPIC
    LOCAL_MQTT_CONNECTED_TOPIC = "local_mqtt_connected_topic"
    RADAR_DISTANCE_TOPIC = "radar_distance_topic"
    BUZZER_BEEP_TOPIC = "buzzer_beep_topic"

    def __init__(self):
        Thread.__init__(self)
        # ----
        print(self.__class__.__name__ + ":init")
        # ----
        self.DEVICE_ID = "virtual_dev_{0}".format(os.name)
        # ---
        if os.getenv('CUSTOM_DEVICE_ID'):
            self.DEVICE_ID = os.getenv('CUSTOM_DEVICE_ID')
        # ---
        print("DEVICE_ID: " + self.DEVICE_ID)
        sentry_sdk.init("https://dc448482f0154329a104fff05357d008@sentry.io/1551410")
        # ---
        with configure_scope() as scope:
            scope.user = {"id": self.DEVICE_ID}
        # ----
        self.local_mqtt_client = MqttLocalClient.MqttLocalClient()
        # ----
        self.local_mqtt_client.TOPICS_LIST = [
            self.BUZZER_BEEP_TOPIC
        ]
        # ----
        self.local_mqtt_client.MIROR_TOPICS_LIST = [
            self.RADAR_DISTANCE_TOPIC
        ]
        # ----
        self.power_py = PyPower()
        # ----
        self.radar_py = PyPing()
        # ----
        self.oled_disp = PyOled()
        # ----

    def run(self):
        # ----
        print(self.__class__.__name__ + ":run")
        # ----
        self.local_mqtt_client.start()
        # ----
        pub.subscribe(self.startup, self.LOCAL_MQTT_CONNECTED_TOPIC)
        pub.subscribe(self.buzz_beep_callback, self.BUZZER_BEEP_TOPIC)
        # ----
        while True:
            pass

    def buzz_beep_callback(self,payload=None):
        PyBuzzer.buzzer_beep()

    def startup(self,payload=None):
        # ----
        self.power_py.start()
        # ----
        self.radar_py.start()
        # ----
        self.oled_disp.start()


if __name__ == '__main__':
    serviceMain = DeviceEdge()
    serviceMain.start()
