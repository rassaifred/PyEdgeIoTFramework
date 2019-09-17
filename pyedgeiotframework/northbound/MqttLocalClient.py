from threading import Thread
import paho.mqtt.client as mqtt
from pubsub import pub
import os


class MqttLocalClient(Thread):

    MQTT_BROCKER_ADRESS = "localhost"
    if os.getenv("MQTT_BROCKER_ADRESS"):
        MQTT_BROCKER_ADRESS = os.getenv("MQTT_BROCKER_ADRESS")
    
    MQTT_BROCKER_PORT = 1883
    MQTT_KEEPALIVE = 60

    LOCAL_MQTT_CONNECTED_TOPIC = "local_mqtt_connected_topic"
    
    TOPICS_LIST = []
    MIROR_TOPICS_LIST = []

    BROCKER_NAME = "local"

    def __init__(self):
        Thread.__init__(self)
        # ----
        print(self.__class__.__name__ + ":init")
        # ----
        self.client = mqtt.Client()
        # ----

    def run(self):
        print(self.__class__.__name__ + ":run")
        # ----
        if len(self.MIROR_TOPICS_LIST) > 0:
            for mirror_topic_item in self.MIROR_TOPICS_LIST:
                pub.subscribe(self.on_mirror_message, str(mirror_topic_item))
        # ----
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # ----
        try:
            self.client.connect(self.MQTT_BROCKER_ADRESS, self.MQTT_BROCKER_PORT, self.MQTT_KEEPALIVE)
        except ConnectionRefusedError:
            print("ConnectionRefusedError")
        # ----
        self.client.loop_forever()
        # ----
        while True:
            pass
        
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Local Mqtt Connected with result code {0} to brocker: {1} at adress: {2}".format(str(rc), self.BROCKER_NAME, self.MQTT_BROCKER_ADRESS))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")
        # client.subscribe("#")
        # ----
        # self.client.subscribe("#")
        # ----
        if len(self.TOPICS_LIST) > 0:
            for topic_item in self.TOPICS_LIST:
                print("local mqtt subscribe to topic:{}".format(topic_item))
                self.client.subscribe(str(topic_item))
        # ----
        pub.sendMessage(self.LOCAL_MQTT_CONNECTED_TOPIC)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        # ----
        # print('Local Mqtt receive topic "%s": %s brocker: %s at adress: %s' % (msg.topic, str(msg.payload), self.BROCKER_NAME,self.MQTT_BROCKER_ADRESS))
        pub.sendMessage(msg.topic, payload=msg.payload)

    def on_mirror_message(self, topic=None, payload=None):
        # print('local mqtt mirror topic "%s"' % topic)
        self.client.publish(topic, payload)
