# ToDo: add mqtt local
# ToDo: add PubSub

import os
from threading import Thread
import time
import sentry_sdk
from sentry_sdk import configure_scope
from modules.power.PyPower import PyPower
from modules.radar.PyPing import PyPing
from modules.oled.PyOled import PyOled
from gpiozero import Buzzer


buzzGpio = 27
nbrConfirmPresense = 2


class DeviceEdge(Thread):

    def __init__(self):
        Thread.__init__(self)
        # ----
        print(self.__class__.__name__ + ":init")
        # ----
        self.DEVICE_ID = "virtual_dev_{0}".format(os.name)
        # ---
        if os.getenv('CUSTOM_DEVICE_ID'):
            self.DEVICE_ID = os.getenv('CUSTOM_DEVICE_ID')
        # ---
        print("DEVICE_ID: " + self.DEVICE_ID)
        sentry_sdk.init("https://dc448482f0154329a104fff05357d008@sentry.io/1551410")
        # ---
        with configure_scope() as scope:
            scope.user = {"id": self.DEVICE_ID}
        # ----
        self.power_py = PyPower()
        # ----
        self.radar_py = PyPing()
        # ----
        self.oled_disp = PyOled()
        # ----
        self.bz = Buzzer(buzzGpio)
        # ----
        self.presence_itt = 0
        self.presence_no_itt = 0
        self.presence = False

    def run(self):
        # ----
        print(self.__class__.__name__ + ":run")
        # ----
        self.power_py.start()
        # ----
        self.radar_py.start()
        # ----
        self.oled_disp.start()
        # ----

        while True:
            if self.radar_py.distance:
                self.oled_disp.line_one = "dist {} cm".format(int(self.radar_py.distance))
                if int(self.radar_py.distance) > 0:
                    if int(self.radar_py.distance) < int(80):
                        self.presence_itt += 1
                        if self.presence_itt >= nbrConfirmPresense:
                            self.presence_itt = 0
                            self.presence = True
                            # ----
                            self.presence_no_itt = 0
                            # ----
                    else:
                        self.presence_no_itt += 1
                        if self.presence_no_itt >= nbrConfirmPresense:
                            self.presence_no_itt = 0
                            self.presence = False
                            # ----
                            self.presence_itt = 0
                            # ----
            # ----
            if self.presence:
                self.bz.beep(.1, .1, 1)
            time.sleep(.5)


if __name__ == '__main__':
    serviceMain = DeviceEdge()
    serviceMain.start()
