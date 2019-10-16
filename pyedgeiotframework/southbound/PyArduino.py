import serial
import time
from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


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
        # --- 1A86:7523
        # --------------------------------------------- SERIAL
        import sys
        import os
        from serial.tools.list_ports_common import ListPortInfo
        if os.name == 'nt' or sys.platform == 'win32':
            from serial.tools.list_ports_windows import comports
        elif os.name == 'posix':
            from serial.tools.list_ports_posix import comports
        else:
            raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))
        # ---
        target_vid = "0x1A86"
        target_pid = "0x7523"
        # ---
        tmp_comp = comports(include_links=None)
        for item in tmp_comp:
            tmp_item: ListPortInfo = item
            print("ARDUINO: {:20} desc: {} hwid: {}".format(tmp_item.device, tmp_item.description, tmp_item.hwid))
            if tmp_item.vid and tmp_item.pid and not self.serial_port:
                print(hex(tmp_item.vid), tmp_item.vid == int(target_vid, 16))
                print(hex(tmp_item.pid), tmp_item.pid == int(target_pid, 16))
                # --- 1A86:7523
                if tmp_item.vid == int(target_vid, 16) and tmp_item.pid == int(target_pid, 16):
                    print("-----> arduino add port {}".format(tmp_item))
                    self.serialport = tmp_item.device
                    try :
                        self.serial_port = serial.Serial(self.serialport, self.baud, timeout=1)
                    except :
                        self.serial_port = None
        # -----------------------------------------------
        # ---
        while self.serial_port:
                self.read_serial_device()
                time.sleep(1)

    def read_serial_device(self):
        # ---
        read_serial = self.serial_port.readline().rstrip()
        # ---
        # print("arduino read serial {}".format(read_serial))
        # ---
        tmp_str = read_serial.decode("utf-8").replace(" ", "")
        if tmp_str:
            # ---
            # print("ARDUINO:", tmp_str)
            # ---
            self.dispatch_event(
                topic=str(tmp_str),
                payload=str(tmp_str)
            )
            # ---
