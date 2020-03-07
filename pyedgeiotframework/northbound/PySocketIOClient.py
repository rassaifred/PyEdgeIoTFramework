"""
ToDo:
"""

import os
import time
import socketio
from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PySocketIOClient(EdgeService):
    SOCKET_IO_SERVER_ADRESS_PROTOCOL = "http"

    if os.getenv("SOCKET_IO_SERVER_ADRESS_PROTOCOL"):
        SOCKET_IO_SERVER_ADRESS_PROTOCOL = os.getenv("SOCKET_IO_SERVER_ADRESS_PROTOCOL")

    SOCKET_IO_SERVER_ADRESS = "localhost"

    if os.getenv("SOCKET_IO_SERVER_ADRESS"):
        SOCKET_IO_SERVER_ADRESS = os.getenv("SOCKET_IO_SERVER_ADRESS")

    SOCKET_IO_PORT = 4000

    if os.getenv("SOCKET_IO_PORT"):
        SOCKET_IO_PORT = os.getenv("SOCKET_IO_PORT")

    SOCKET_IO_CLIENT_CONNECTED_TOPIC = "socket_io_client_connected_topic"

    SOCKET_IO_CLIENT_DISCONNECTED_TOPIC = "socket_io_client_disconnected_topic"

    TOPICS_LIST = ["/"]
    MIROR_TOPICS_LIST = []

    sio = None

    def __init__(self):
        # ---
        EdgeService.__init__(self)
        # ---
        # explode_topic_to_namespace(tmp_topic="/device/rpi_03/get_event")
        # ---
        self.sio = socketio.Client(logger=False)
        # ---
        # self.sio.on('connect', self.connect_handler)
        # self.sio.on('disconnect', self.disconnect_handler)
        # ---
        if len(self.TOPICS_LIST) > 0:
            for topic_item in self.TOPICS_LIST:
                # print("client: 0 socketIO subscribe to topic:{}".format(topic_item))
                # self.client.subscribe(str(topic_item))
                self.sio.register_namespace(EdgeClientNamespace(str(topic_item)))

    def run(self) -> None:
        # ---
        EdgeService.run(self)
        # ---
        if len(self.MIROR_TOPICS_LIST) > 0:
            for mirror_topic_item in self.MIROR_TOPICS_LIST:
                # print("client: 0 socketIO subscribe mirror topic:{}".format(mirror_topic_item))
                self.subscribe_command(callback=self.on_mirror_message, topic=mirror_topic_item)

        # ---
        while True:
            if not self.sio.connected:
                # ---
                try:
                    self.sio.connect(
                        "{0}://{1}:{2}".format(
                            self.SOCKET_IO_SERVER_ADRESS_PROTOCOL,
                            self.SOCKET_IO_SERVER_ADRESS,
                            self.SOCKET_IO_PORT
                        ),
                        transports=['websocket', 'polling']
                    )

                    # ---
                except Exception as e:
                    print("{} error: {}".format(self.__class__.__name__, e))
            time.sleep(5)
        # ---

    # @sio.on('connect')
    def connect_handler(self):
        # ----
        print('client: Connected!')
        # ----
        # ----
        # pub.sendMessage(self.SOCKET_IO_CLIENT_CONNECTED_TOPIC)
        self.dispatch_event(self.SOCKET_IO_CLIENT_CONNECTED_TOPIC)
        # ----
        if len(self.TOPICS_LIST) > 0:
            for topic_item in self.TOPICS_LIST:
                print("client: 1 socketIO subscribe to topic:{}".format(topic_item))
                # self.client.subscribe(str(topic_item))
                self.sio.register_namespace(EdgeClientNamespace(str(topic_item)))
                pass
        # ---

    # @sio.on('disconnect')
    def disconnect_handler(self):
        # ----
        print('client: Disconnect!')
        # ----
        # ----
        # pub.sendMessage(self.SOCKET_IO_CLIENT_DISCONNECTED_TOPIC)
        self.dispatch_event(topic=self.SOCKET_IO_CLIENT_DISCONNECTED_TOPIC)
        # ----

    def on_mirror_message(self, topic=None, payload=None):
        # print('socketIO mirror topic "%s"' % topic)
        if self.sio.connected:
            self.sio.emit(payload, namespace=topic)


def explode_topic_to_namespace(tmp_topic: str):
    # ---
    tmp_dico = {
        "namespace": "",
        "event": ""
    }
    # ---
    result: str = tmp_topic.split("/")
    # ---
    event_tmp = result[len(result) - 1]
    # ---
    index_sep = tmp_topic.rfind('/')
    tmp_namespace = tmp_topic[0:index_sep]
    # ---
    tmp_dico["namespace"] = tmp_namespace
    tmp_dico["event"] = event_tmp
    # ---
    print(tmp_dico)
    # ---
    return tmp_dico


class EdgeClientNamespace(socketio.ClientNamespace):

    def on_connect(self):
        print("EdgeClientNamespace on_camfi_socket_connect ", self.namespace)
        pass

    def on_disconnect(self):
        print("EdgeClientNamespace on_camfi_socket_disconnect")
        pass

    def on_message(self, msg=None):
        print('EdgeClientNamespace Received message')
