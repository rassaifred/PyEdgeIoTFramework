"""
ToDo:
"""

import time
import socketio
import eventlet
from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PySocketIOServer(EdgeService):

    SOCKET_IO_SERVER_ADRESS = 'localhost'
    SOCKET_IO_SERVER_PORT = 4000

    SOCKET_IO_SERVER_CONNECTED_TOPIC = "socket_io_server_connected_topic"
    SOCKET_IO_SERVER__DISCONNECTED_TOPIC = "socket_io_server__disconnected_topic"

    TOPICS_LIST = ["/"]
    MIROR_TOPICS_LIST = []

    sio = None
    app = None

    registred = False

    def __init__(self):
        # ---
        EdgeService.__init__(self)
        # ---
        self.sio = socketio.Server(cors_allowed_origins='*', always_connect=True)
        # ----
        # self.sio.on('connect', self.connect_handler)
        # self.sio.on('disconnect', self.disconnect_handler)

        # ---
        if len(self.TOPICS_LIST) > 0:
            for topic_item in self.TOPICS_LIST:
                print("server: socketIO subscribe to topic:{}".format(topic_item))
                # self.client.subscribe(str(topic_item))
                self.sio.register_namespace(EdgeServerNamespace(str(topic_item)))
                pass
        # ---

    def run(self) -> None:
        # ---
        EdgeService.run(self)
        # ----
        print('server socket io run')
        # ----

        """self.sio.on('connect', self.connect_handler)
        self.sio.on('disconnect', self.disconnect_handler)
        self.sio.event('my_event', self.my_event)
        self.sio.event('my_broadcast_event', self.my_broadcast_event)
        self.sio.event('join', self.join)
        self.sio.event('leave', self.leave)
        self.sio.event('close_room', self.close_room)
        self.sio.event('my_room_event', self.my_room_event)
        self.sio.event('disconnect_request', self.disconnect_request)
        self.sio.event('connect', self.connect)
        self.sio.event('disconnect', self.disconnect)"""

        # ----
        # wrap with a WSGI application
        self.app = socketio.WSGIApp(self.sio)
        # ----
        eventlet.wsgi.server(
            eventlet.listen(
                (
                    self.SOCKET_IO_SERVER_ADRESS,
                    self.SOCKET_IO_SERVER_PORT
                )
            ),
            self.app
        )
        # ----
        while True:
            pass
        # ----

    """def disconnect_handler(self, sid):
        print('server: Client({}) disconnected!'.format(sid))

    def connect_handler(self, sid, environ):
        print('server: Client({}) Connected!'.format(sid))
        if not self.registred:
            # ---
            self.registred = True
            # ---
            if len(self.TOPICS_LIST) > 0:
                for topic_item in self.TOPICS_LIST:
                    print("server: socketIO subscribe to topic:{}".format(topic_item))
                    # self.client.subscribe(str(topic_item))
                    self.sio.register_namespace(EdgeServerNamespace(str(topic_item)))
                    pass
            # ---"""


class EdgeServerNamespace(socketio.Namespace):

    # @sio.event
    def on_disconnect_request(self, sid):
        self.disconnect(sid)

    # @sio.event
    def on_connect(self, sid, environ):
        print('EdgeServerNamespace: Client({}) Connected!'.format(sid))
        # self.send(data={'data': 'Connected', 'count': 0})

    # @sio.event
    def on_disconnect(sid):
        print('EdgeServerNamespace: Client disconnected')

    def on_message(self, sid, message= None):
        print('EdgeServerNamespace: Received message {0} : {1} {2}'.format(self.namespace, sid, message))
        # self.emit(event="message", data=msg, room=sid)
        # self.send(data={'data': message})

