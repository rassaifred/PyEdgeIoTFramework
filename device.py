# ToDo: add mqtt local
# ToDo: add PubSub

from threading import Thread
from modules.PyOled import PyOled


class DeviceEdge(Thread):

    def __init__(self):
        Thread.__init__(self)
        # ----
        print(self.__class__.__name__ + ":init")
        # ----
        self.display = PyOled()
        self.display.start()

    def run(self):
        # ----
        print(self.__class__.__name__ + ":run")
        # ----
        print("welcome to device")
        # ----

        self.display.line_one = "hello"
        self.display.display_lines()


        while True:
            pass




if __name__ == '__main__':
    serviceMain = DeviceEdge()
    serviceMain.start()
