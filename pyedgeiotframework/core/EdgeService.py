"""
ToDo: add requirements mechanism
"""

from threading import Thread
from pubsub import pub


class EdgeService(Thread):

    def __new__(cls, *args, **kwargs):
        super().__new__(cls)
        # ---
        print(cls.__name__ + ":new")
        # create our object and return it
        obj = super().__new__(cls)
        return obj

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
