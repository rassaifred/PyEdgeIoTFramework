"""
ToDo:
"""

import socketio
import eventlet
from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PySocketIOServer(EdgeService):

    SOCKET_IO_SERVER_ADRESS = 'localhost'
    SOCKET_IO_SERVER_PORT = 4000

    SOCKET_IO_SERVER_CONNECTED_TOPIC = "socket_io_server_connected_topic"
    SOCKET_IO_SERVER__DISCONNECTED_TOPIC = "socket_io_server__disconnected_topic"

    TOPICS_LIST = ["/", "/test"]
    MIROR_TOPICS_LIST = []

    sio = None
    app =None

    def __init__(self):
        # ---
        EdgeService.__init__(self)
        # ---

    def hello_world(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['Hello, World!\r\n']

    def run(self) -> None:
        # ---
        EdgeService.run(self)
        # ----
        print('server socket io run')
        # ----
        self.sio = socketio.Server(async_mode='eventlet', always_connect=True, cors_allowed_origins='*')
        # self.sio.on('connect', self.connect_handler)
        # self.sio.on('disconnect', self.disconnect_handler)
        # self.sio.event('message', self.message_handler)
        # ----
        # wrap with a WSGI application
        self.app = socketio.WSGIApp(self.sio)
        # ----
        # self.app = socketio.WSGIApp(self.sio, self.hello_world)
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

    # @sio.on('connect')
    def connect_handler(self, sid, environ):
        # ----
        print('server: Client({}) Connected!'.format(sid))
        self.sio.enter_room(sid, "sid_room")
        # ----
        """if len(self.TOPICS_LIST) > 0:
            for topic_item in self.TOPICS_LIST:
                print("server: socketIO subscribe to topic:{}".format(topic_item))
                # self.client.subscribe(str(topic_item))
                self.sio.register_namespace(EdgeServerNamespace(str(topic_item)))"""
        # ----
        self.dispatch_event(topic=self.SOCKET_IO_SERVER_CONNECTED_TOPIC)
        # ----

    def message_handler(self, sid, msg): # , data, sid=None, namespace=None):
        print('server: Received message: ', msg)

    # @sio.on('disconnect')
    def disconnect_handler(self, sid):
        # ----
        print('server: Client({}) Disconnect!'.format(sid))
        # ----
        self.dispatch_event(topic=self.SOCKET_IO_SERVER__DISCONNECTED_TOPIC)


class EdgeServerNamespace(socketio.Namespace):
    def on_connect(self, sid, environ):
        # self.enter_room(sid, room="local_room")
        # self.emit(event="message", skip_sid=sid,namespace=self.namespace,data="bienvenue")
        pass

    def on_disconnect(self, sid):
        pass

    def on_message(self, sid, msg= None):
        print('EdgeServerNamespace: Received message {0} : {1} {2}'.format(self.namespace, sid, msg))
        self.emit(event="message", data=msg, namespace=self.namespace, room="local_room")
