from threading import Thread


class DeviceEdge(Thread):
    def __init__(self):
        Thread.__init__(self)
        # ----
        print(self.__class__.__name__ + ":init")
        # ----

    def run(self):
        # ----
        print(self.__class__.__name__ + ":run")
        # ----
        print("welcome to device")
        # ----
        while True:
            pass


if __name__ == '__main__':
    serviceMain = DeviceEdge()
    serviceMain.start()
