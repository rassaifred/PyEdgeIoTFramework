"""
ToDo: add requirements mechanism
"""

from threading import Thread
from pubsub import pub


class EdgeService(Thread):

    def __init__(self):
        print(self.__class__.__name__ + ":init")
        # ----
        super().__init__()
        # ----

    def run(self) -> None:
        # ----
        print(self.__class__.__name__ + ":run")
        # ----

    def dispatch_event(self, topic=None, payload=None):
        # print("dispatch event {} {}".format(topic,payload))
        pub.sendMessage(topicName=topic, payload=payload)

    def subscribe_command(self, callback=None, topic=None):
        # print("subscribe event {}".format(topic))
        if topic and callback:
            pub.subscribe(callback, topic)
