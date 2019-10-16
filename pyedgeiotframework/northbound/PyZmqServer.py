#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
from pyedgeiotframework.core.EdgeService import EdgeService


class PyZmqServer(EdgeService):

    context = None
    socket = None

    def __init__(self):
        # ---
        EdgeService.__init__(self)
        # ---
        # explode_topic_to_namespace(tmp_topic="/device/rpi_03/get_event")

    def run(self) -> None:
        # ---
        EdgeService.run(self)
        # ---
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.bind("tcp://*:5555")

        while True:
            #  Wait for next request from client
            message = self.socket.recv()
            print("Received request: %s" % message)

            #  Do some 'work'
            time.sleep(1)

            #  Send reply back to client
            self.socket.send(b"World")