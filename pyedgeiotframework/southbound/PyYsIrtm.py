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
        # ---- 067B:2303
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
        target_vid = "0x067B"
        target_pid = "0x2303"
        # ---
        tmp_comp = comports(include_links=None)
        for item in tmp_comp:
            tmp_item: ListPortInfo = item
            print("IR_module: {:20} desc: {} hwid: {}".format(tmp_item.device, tmp_item.description, tmp_item.hwid))
            if tmp_item.vid and tmp_item.pid and not self.serial_port:
                print(hex(tmp_item.vid), tmp_item.vid == int(target_vid, 16))
                print(hex(tmp_item.pid), tmp_item.pid == int(target_pid, 16))
                # --- 1A86:7523
                if tmp_item.vid == int(target_vid, 16) and tmp_item.pid == int(target_pid, 16):
                    print("-----> IR_module add port {}".format(tmp_item))
                    self.serialport = tmp_item.device
                    try:
                        self.serial_port = serial.Serial(self.serialport, self.baud, timeout=1)
                        self.subscribe_command(
                            callback=self.send_command,
                            topic=self.SEND_IR_TOPIC
                        )
                        # self.send_command([0x32, 0xcd, 0x81])
                    except:
                        self.serial_port = None
        # -----------------------------------------------
        # ----
        while self.serial_port:
            self.read_from_port()
            pass

    def read_from_port(self):
        while not self.connected:
            print('reading from port', self.serialport)
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
