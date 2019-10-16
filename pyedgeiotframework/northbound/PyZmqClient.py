#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
from pyedgeiotframework.core.EdgeService import EdgeService


class PyZmqClient(EdgeService):
    ZMQ_SERVER_ADRESS = "localhost"

    ZMQ_SERVER_PORT = 5555
    ZMQ_KEEPALIVE = 60

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

        #  Socket to talk to server
        print("Connecting to hello world server…")
        topicfilter = "10001"
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://{}:{}".format(self.ZMQ_SERVER_ADRESS, self.ZMQ_SERVER_PORT))
        self.socket.setsockopt(zmq.SUBSCRIBE, topicfilter.encode('utf-8'))

        # Process 5 updates
        total_value = 0

        # self.socket.send("%d %d".format(topicfilter, "ya allo").encode('utf-8'))
        self.socket.send_string("%s %s" % (topicfilter, "hello"))

        for update_nbr in range(5):
            string = self.socket.recv()
            topic, messagedata = string.split()
            total_value += int(messagedata)
            print(topic, messagedata)

        print("Average messagedata value for topic '%s' was %dF" % (topicfilter, total_value / update_nbr))