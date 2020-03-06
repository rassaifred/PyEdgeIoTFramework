"""
ToDo: ok - add DSLR_Gateway class as parent of every gateway, e.g: PyDSLRCamFiGateway
ToDo: ok - verify if camfi-adress
ToDo: ok - add camera order
ToDo: add Dispatch Camera Added Event
ToDo: add loading photo file_added
ToDo: add Dispatch photo downloaded event
ToDo: add fail scenarios
"""

import json

from PyEdgeIoTFramework.pyedgeiotframework.northbound.PyDSLRMatrix import PyDSLRMatrix
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyDSLRCamFiGateway import PyDSLRCamFiGateway


class PyCamFiMatrix(PyDSLRMatrix):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.gateways_base_ip = "192" + '.' + "168" + '.9.'
        # ----

    def run(self) -> None:
        # ----
        super().run()
        # ----
        # print(gateways_ips_list)
        # ----
        if self.gateways_ips_list:
            # ----
            itt = 1
            # ----
            for c_ip in self.gateways_ips_list:
                # ---
                # for x in range(0, 29):
                # ---
                camfi = PyDSLRCamFiGateway()
                camfi.camera.order = itt
                camfi.ip_adress = c_ip
                camfi.start()
                # ---
                self.gateways_list.append(camfi)
                # ---
                itt += 1
                # ---

    def validate_gateway(self, tmp_ip):
        # ----
        super().validate_gateway(tmp_ip)
        # ----
        # verify ip
        # ----
        # print("verify ip: {}".format(tmp_ip))
        # ----
        data = json.dumps(PyDSLRCamFiGateway.get_camfi_info(None, tmp_ip=tmp_ip))
        tmp_dect = json.loads(data)
        if tmp_dect["version"]:
            return True
        else:
            return False
