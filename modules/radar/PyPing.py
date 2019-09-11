"""
It requires only 3 wires to connect it to the Pi.
One is +5V which can be grabbed directly from pin 2 of the Raspberry Pi,
one is Ground, which is provided on pin 4,
and the third is pin 11

"""
from threading import Thread
import time
import RPi.GPIO as GPIO


# Use board based pin numbering
# GPIO.setmode(GPIO.BOARD)

sigGpio = 17


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

    while GPIO.input(pin) == 0:
        starttime = time.time()

    while GPIO.input(pin) == 1:
        endtime = time.time()

    duration = endtime - starttime
    # Distance is defined as time/2 (there and back) * speed of sound 34000 cm/s
    distance = duration * 34000 / 2
    return distance


class PyPing(Thread):

    def __init__(self):
        Thread.__init__(self)
        # ----
        print(self.__class__.__name__ + ":init")
        # ----
        self.distance = -1

    def run(self):
        # ----
        print(self.__class__.__name__ + ":run")
        # ----
        while True:
            self.distance = read_distance(sigGpio)
            # print("Distance to object is ", distance, " cm or ", distance * .3937, " inches")
            time.sleep(.5)

