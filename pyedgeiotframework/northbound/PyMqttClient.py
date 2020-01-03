"""
ToDo: clean up
ToDo: add subscribe_mqtt_topic --> mirror to --> PyPubSub

"""

import os
import time
import json

import paho.mqtt.client as mqtt
from pubsub import pub
from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PyMqttClient(EdgeService):
    MQTT_BROCKER_ADRESS = "localhost"
    if os.getenv("MQTT_BROCKER_ADRESS"):
        MQTT_BROCKER_ADRESS = os.getenv("MQTT_BROCKER_ADRESS")

    MQTT_BROCKER_PORT = 1883
    MQTT_KEEPALIVE = 60

    LOCAL_MQTT_CONNECTED_TOPIC = "local_mqtt_connected_topic"
    REMOTE_MQTT_CONNECTED_TOPIC = "remote_mqtt_connected_topic"

    TOPICS_LIST = []
    MIROR_TOPICS_LIST = []

    REMOTE_TYPE = "remote"
    LOCAL_TYPE = "local"

    BROCKER_NAME = LOCAL_TYPE

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.client = mqtt.Client()
        # ----
        self.client_connected = False
        # ----

    def run(self):
        # ----
        super().run()
        # ----
        if len(self.MIROR_TOPICS_LIST) > 0:
            for mirror_topic_item in self.MIROR_TOPICS_LIST:
                print("pypubsub subscribe to topic:{}".format(mirror_topic_item))
                # pub.subscribe(self.on_mirror_message, str(mirror_topic_item))
                # ----
                self.subscribe_command(
                    callback=self.on_mirror_message,
                    topic=str(mirror_topic_item)
                )
                # ----
        # ----
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_log = self.on_log
        # ----
        while True:
            if not self.client_connected:
                # ----
                try:
                    self.client.connect(self.MQTT_BROCKER_ADRESS, self.MQTT_BROCKER_PORT, self.MQTT_KEEPALIVE)
                    # self.client.loop_forever()
                    self.client.loop_start
                except Exception as e:
                    print("{} error: {}".format(self.__class__.__name__, e))
                # ----
            # time.pause(5)
            time.sleep(5)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Mqtt Connected with result code {0} to brocker: {1} at adress: {2}".format(str(rc), self.BROCKER_NAME,
                                                                                          self.MQTT_BROCKER_ADRESS))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")
        # client.subscribe("#")
        # ----
        # self.client.subscribe("#")
        # ----
        if len(self.TOPICS_LIST) > 0:
            for topic_item in self.TOPICS_LIST:
                print("mqtt subscribe to topic:{}".format(topic_item))
                self.client.subscribe(str(topic_item))

        # ----
        if self.BROCKER_NAME is self.LOCAL_TYPE:
            pub.sendMessage(self.LOCAL_MQTT_CONNECTED_TOPIC)
        else:
            pub.sendMessage(self.REMOTE_MQTT_CONNECTED_TOPIC)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        # ----
        # print('Local Mqtt receive topic "%s": %s brocker: %s at adress: %s' % (msg.topic, str(msg.payload), self.BROCKER_NAME,self.MQTT_BROCKER_ADRESS))
        pub.sendMessage(topicName=msg.topic, payload=msg.payload)

    def on_mirror_message(self, topic=None, payload=None, topicArg=None):
        # print('local mqtt mirror topic "%s"' % topic)
        if not topic:
            if topicArg:
                topic = topicArg
        self.client.publish(topic, json.dumps(payload))

    def on_publish(self, client, userdata, mid):
        # print("mqtt publish", userdata, mid)
        pass

    def on_log(self, client, userdata, level, buf):
        pass