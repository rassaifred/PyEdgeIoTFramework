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
        EdgeService.run(self)
        self.serial_port = serial.Serial(self.serialport, self.baud, timeout=1)
        while True:
            self.read_serial_device()
            time.sleep(1)

    def read_serial_device(self):
        read_serial = self.serial_port.readline().rstrip()
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
