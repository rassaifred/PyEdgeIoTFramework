from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService
import serial
import time


class PyArduino(EdgeService):
    ARDUINO_UNO_REV3_PORT = '/dev/ttyUSB0'
    ARDUINO_NANO_REV3_PORT = '/dev/cu.wchusbserial14230'
    serialport = ARDUINO_NANO_REV3_PORT
    baud = 115200
    serial_port = None

    def __int__(self):
        EdgeService.__init__(self)

    def run(self) -> None:
        # ---
        EdgeService.run(self)
        # ---
        # --------------------------------------------- SERIAL
        import sys
        import os
        if os.name == 'nt' or sys.platform == 'win32':
            from serial.tools.list_ports_windows import comports
        elif os.name == 'posix':
            from serial.tools.list_ports_posix import comports
        else:
            raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))
        # ----
        hits = 0
        tmp_comp = comports(include_links=None)
        iterator = sorted(tmp_comp)
        for n, (port, desc, hwid) in enumerate(iterator, 1):
            # print("{:20}\n".format(port))
            """print("{:20}".format(port))
            print(" desc: {}".format(desc))
            print(" hwid: {}".format(hwid))"""
            # ---
            # print('# ----> {}'.format(tmp_comp[hits].hwid))
            # ---
            if "067B" in str(tmp_comp[hits].hwid) and "2303" in str(tmp_comp[hits].hwid):
                print("-----> arduino add port {}".format(port))
                self.serialport = port

            # ---
            hits += 1
        # -----------------------------------------------
        # ---
        self.serial_port = serial.Serial(self.serialport, self.baud, timeout=1)
        # ---
        while self.serial_port:
            self.read_serial_device()
            time.sleep(1)

    def read_serial_device(self):
        # ---
        read_serial = self.serial_port.readline().rstrip()
        # ---
        print("arduino read serial {}".format(read_serial))
        # ---
        tmp_str = read_serial.decode("utf-8").replace(" ", "")
        if tmp_str:
            # ---
            print("ARDUINO:", tmp_str)
            # ---
            self.dispatch_event(
                topic=str(tmp_str),
                payload=str(tmp_str)
            )
            # ---
