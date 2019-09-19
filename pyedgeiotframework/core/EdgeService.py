"""
ToDo: add requirements mechanism
"""

from threading import Thread
from pubsub import pub


class EdgeService(Thread):

    def __int__(self):
        Thread.__init__(self)
        # ----
        print(self.__class__.__name__ + ":init")
        # ----

    def run(self) -> None:
        # ----
        print(self.__class__.__name__ + ":run")
        # ----

    def dispatch_event(self, topic=None, payload=None):
        pub.sendMessage(topicName=topic, payload=payload)

    def subscribe_command(self, callback=None, topic=None):
        if topic and callback:
            pub.subscribe(callback, topic)
