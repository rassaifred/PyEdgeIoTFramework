"""
ToDo:
"""

import socketio
from pubsub import pub
from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PySocketIOClient(EdgeService):

    SOCKET_IO_SERVER_ADRESS = "localhost"
    SOCKET_IO_PORT = 4000

    SOCKET_IO_CONNECTED_TOPIC = "socket_io_connected_topic"
    SOCKET_IO_DISCONNECTED_TOPIC = "socket_io_disconnected_topic"

    TOPICS_LIST = []
    MIROR_TOPICS_LIST = []

    sio = None

    def __init__(self):
        # ---
        EdgeService.__init__(self)
        # ---
        self.sio = socketio.Client(logger=True)
        # ---

    def run(self) -> None:
        # ---
        EdgeService.run(self)
        # ----
        if len(self.MIROR_TOPICS_LIST) > 0:
            for mirror_topic_item in self.MIROR_TOPICS_LIST:
                pub.subscribe(self.on_mirror_message, str(mirror_topic_item))
        # ---
        try:
            self.sio.connect("{0}:{1}".format(self.SOCKET_IO_SERVER_ADRESS, self.SOCKET_IO_PORT))
        except ConnectionRefusedError:
            print("ConnectionRefusedError")
        # ---
        while True:
            pass
        # ---

    @sio.on('connect')
    def connect_handler(self):
        # ----
        print('Connected!')
        # ----
        if len(self.TOPICS_LIST) > 0:
            for topic_item in self.TOPICS_LIST:
                print("socketIO subscribe to topic:{}".format(topic_item))
                # self.client.subscribe(str(topic_item))
                self.sio.register_namespace(EdgeClientNamespace(str(topic_item)))
        # ----
        pub.sendMessage(self.SOCKET_IO_CONNECTED_TOPIC)
        # ----

    @sio.on('disconnect')
    def disconnect_handler(self):
        # ----
        print('Disconnect!')
        # ----
        pub.sendMessage(self.SOCKET_IO_DISCONNECTED_TOPIC)
        # ----

    def message_handler(self, data, sid=None, namespace=None):
        print('Received message: ', data)

    def on_mirror_message(self, topic=None, payload=None):
        # print('socketIO mirror topic "%s"' % topic)
        self.sio.send(payload, namespace=topic)


class EdgeClientNamespace(socketio.ClientNamespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_message(self):
        pass
