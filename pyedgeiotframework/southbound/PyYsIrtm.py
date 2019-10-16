import sys
import serial
import binascii
from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PyYsIrtm(EdgeService):

    # PubSub TOPIC
    SEND_IR_TOPIC = "send_ir_topic"

    serialport = '/dev/cu.usbserial'
    connected = False
    baselist = [0xA1, 0xF1]
    baud = 9600
    # serial_port = serial.Serial(serialport, baud, timeout=1)
    serial_port = None
    runLoop = True

    def __int__(self):
        # ----
        EdgeService.__init__(self)
        # ----

    def run(self) -> None:
        # ----
        EdgeService.run(self)
        # ----
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
            if "1A86" in str(tmp_comp[hits].hwid) and "7523" in str(tmp_comp[hits].hwid):
                self.serialport = port
                print("-----> ir add port {}".format(port))
            # ---
            hits += 1
        # -----------------------------------------------
        # ----
        # self.send_command([0x32, 0xcd, 0x81])
        # ----
        try :
            self.serial_port = serial.Serial(self.serialport, self.baud, timeout=1)
            # ----
            self.subscribe_command(
                callback=self.send_command,
                topic=self.SEND_IR_TOPIC
            )
        except :
            print("IR port problem")
        # ----
        while True:
            pass

    def read_from_port(self):
        print('reading from port', self.serialport)
        while not self.connected:
            self.connected = True
            while self.runLoop:
                # try:
                data = bytearray(self.serial_port.read(3))
                if len(list(data)) > 0 and len(list(data)) >= 3:
                    print(list(data))

    def send_command(self, payload=None):
        print("send_ir_command")
        if payload:
            data = binascii.unhexlify(payload)
            sys.stdout.write('sending')
            # toujours ajouter 0xA1, 0xF1 au debut de la command IR
            if len(list(data)) > 0 and len(list(data)) >= 3:
                print(list(data))
                values = bytearray([* self.baselist, *data])
                self.serial_port.write(values)
