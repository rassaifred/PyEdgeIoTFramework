"""
It requires only 3 wires to connect it to the Pi.
One is +5V which can be grabbed directly from pin 2 of the Raspberry Pi,
one is Ground, which is provided on pin 4,
and the third is pin 11
ToDo: catch error discontinued mesurment

"""

from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService
import time
from pubsub import pub
import RPi.GPIO as GPIO


RADAR_DISTANCE_TOPIC = "radar_distance_topic"


# Use board based pin numbering
# GPIO.setmode(GPIO.BOARD)

sigGpio = 17
sigInterval = .2
maxTime = 0.04


def read_distance(pin):

    # print("read")

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

    time.sleep(0.000002)

    # send trigger signal
    GPIO.output(pin, 1)

    time.sleep(0.000005)

    GPIO.output(pin, 0)

    GPIO.setup(pin, GPIO.IN)

    starttime = time.time()
    timeout = starttime + maxTime

    # while GPIO.input(pin) == 0:
    while GPIO.input(pin) == 0 and starttime < timeout:
        starttime = time.time()

    endtime = time.time()
    timeout = endtime + maxTime
    # while GPIO.input(pin) == 1:
    while GPIO.input(pin) == 1 and endtime < timeout:
        endtime = time.time()

    duration = endtime - starttime
    # Distance is defined as time/2 (there and back) * speed of sound 34000 cm/s
    distance = duration * 34000 / 2
    return distance


distance = -1


class PyPing(EdgeService):

    def __init__(self):
        EdgeService.__init__(self)
        # ----
        # ----

    def run(self):
        # ----
        EdgeService.run(self)
        # ----
        while True:
            try:
                self.distance = read_distance(sigGpio)
            except:
                print("error to ping")
            # print("Distance to object is ", distance, " cm or ", distance * .3937, " inches")
            # ----
            self.dispatch_event(
                topic=RADAR_DISTANCE_TOPIC,
                payload=str(self.distance)
            )
            # ----

            time.sleep(sigInterval)

