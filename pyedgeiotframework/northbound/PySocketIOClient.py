"""
ToDo:
"""

import time
import socketio
from pubsub import pub
from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PySocketIOClient(EdgeService):

    SOCKET_IO_SERVER_ADRESS_PROTOCOL = "http"
    SOCKET_IO_SERVER_ADRESS = "localhost"
    SOCKET_IO_PORT = 4000

    SOCKET_IO_CLIENT_CONNECTED_TOPIC = "socket_io_client_connected_topic"
    SOCKET_IO_CLIENT_DISCONNECTED_TOPIC = "socket_io_client_disconnected_topic"

    TOPICS_LIST = ["/"]
    MIROR_TOPICS_LIST = []

    sio = None

    connected = False

    def __init__(self):
        # ---
        EdgeService.__init__(self)
        # ---
        # explode_topic_to_namespace(tmp_topic="/device/rpi_03/get_event")

    def run(self) -> None:
        # ---
        EdgeService.run(self)
        # ---
        self.sio = socketio.Client(logger=True)
        # ---
        self.sio.on('connect', self.connect_handler)
        self.sio.on('disconnect', self.disconnect_handler)
        self.sio.event('message', self.message_handler)
        # ---
        if len(self.TOPICS_LIST) > 0:
            for topic_item in self.TOPICS_LIST:
                print("client: socketIO subscribe to topic:{}".format(topic_item))
                # self.client.subscribe(str(topic_item))
                # self.sio.register_namespace(EdgeClientNamespace(str(topic_item)))
        # ---
        if len(self.MIROR_TOPICS_LIST) > 0:
            for mirror_topic_item in self.MIROR_TOPICS_LIST:
                # pub.subscribe(self.on_mirror_message, str(mirror_topic_item))
                self.subscribe_command(callback=self.on_mirror_message, topic=self.on_mirror_message)
        # ---
        while True:
            if not self.connected:
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
                except:
                    print("client: ConnectionError")
                    time.sleep(3)
            pass
        # ---

    # @sio.on('connect')
    def connect_handler(self):
        # ----
        print('client: Connected!')
        # ----
        self.connected = True
        # ----
        pub.sendMessage(self.SOCKET_IO_CLIENT_CONNECTED_TOPIC)
        # ----
        self.sio.send(data={"device": "rpi_03"})

    # @sio.on('disconnect')
    def disconnect_handler(self):
        # ----
        print('client: Disconnect!')
        # ----
        self.connected = False
        # ----
        pub.sendMessage(self.SOCKET_IO_CLIENT_DISCONNECTED_TOPIC)
        # ----

    def message_handler(self, sid, msg):  # , data, sid=None, namespace=None):
        print('Received message: ', msg)

    def on_mirror_message(self, topic=None, payload=None):
        # print('socketIO mirror topic "%s"' % topic)
        if self.connected:
            self.sio.send(payload, namespace=topic)


def explode_topic_to_namespace(tmp_topic: str):
    # ---
    tmp_dico = {
        "namespace": "",
        "event": ""
    }
    # ---
    result:str = tmp_topic.split("/")
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
        # self.sio.emit(event="message", namespace="/test", data=self.SOCKET_IO_CLIENT_CONNECTED_TOPIC)
        print("EdgeClientNamespace on_connect ", self.namespace)
        pass

    def on_disconnect(self):
        print("EdgeClientNamespace on_disconnect")
        pass

    def on_message(self,msg = None):
        print('EdgeClientNamespace Received message')
