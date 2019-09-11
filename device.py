# ToDo: add mqtt local
# ToDo: add PubSub

from threading import Thread
from gpiozero import Button, Buzzer


class DeviceEdge(Thread):

    btnGpio = 17
    buzzGpio = 27

    def __init__(self):
        Thread.__init__(self)
        # ----
        print(self.__class__.__name__ + ":init")
        # ----
        self.bz = Buzzer(self.buzzGpio)

    def run(self):
        # ----
        print(self.__class__.__name__ + ":run")
        # ----
        print("welcome to device")
        # ----
        self.bz.beep(0.2,1,10)

        while True:
            pass


if __name__ == '__main__':
    serviceMain = DeviceEdge()
    serviceMain.start()
