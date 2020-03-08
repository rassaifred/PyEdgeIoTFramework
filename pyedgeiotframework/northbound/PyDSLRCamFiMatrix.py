"""

ToDo: ok - add DSLR_Gateway class as parent of every gateway, e.g: PyDSLRCamFiGateway
ToDo: ok - verify if camfi-adress
ToDo: ok - add camera order
ToDo: ok - add Dispatch Camera Added Event
ToDo: ok - add loading photo file_added
ToDo: ok - add Dispatch photo downloaded event
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
        self.gateways_base_ip = "192:168:9:1-255"
        # ----

    def run(self) -> None:
        # ----
        super().run()
        # ----

    def get_dslr_gateways(self):
        super().get_dslr_gateways()
        # ----
        self.network_scan_dslr_gateways()
        # ----

    def validate_gateway(self, payload=None):
        # ----
        super().validate_gateway(payload=payload)
        # ----
        # verify ip
        # ----
        # print("verify ip: {}".format(payload))
        # ----
        tmp_dct = json.loads(payload)
        # ----
        if tmp_dct["gateway_ip"]:
            tmp_gatway_ip = tmp_dct["gateway_ip"]
            # ----
            try:
                tmp_dict = PyDSLRCamFiGateway.get_camfi_info(None, tmp_ip=tmp_gatway_ip)
                # ----
                if tmp_dict["version"]:
                    return True
                else:
                    return False
            except:
                pass

    def create_gateway(self, payload=None):
        # ----
        super().create_gateway(payload=payload)
        # ----
        camfi = PyDSLRCamFiGateway()
        # ----
        tmp_dct = json.loads(payload)
        # ----
        if tmp_dct["camera_order"]:
            camfi.camera.camera_order = tmp_dct["camera_order"]

        if tmp_dct["gateway_ip"]:
            camfi.gateway_ip = tmp_dct["gateway_ip"]

        camfi.start()
        # ---
        self.gateways_list.append(camfi)
