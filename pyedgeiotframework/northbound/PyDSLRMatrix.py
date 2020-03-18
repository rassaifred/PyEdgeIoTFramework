"""

ToDo: ok - extract scan ip functions to PyNetworkScan
ToDo: ok - add PyNetworkScan based on test_ping.py
ToDo: add plug&play feature with rescan gateways
ToDo: add change photo number via PubSub
ToDo: add timeout for staying adding photo

"""

import json

from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyDSLRGateway import PyDSLRGateway
from PyEdgeIoTFramework.pyedgeiotframework.northbound.PyNetworkScan import PyNetworkScan


class PyDSLRMatrix(EdgeService):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.scanner = None
        # ----
        self.camera_number = 1
        # ----
        self.gateways_base_ip = "192:168:1:1-255"
        self.gateways_create_iterator = 0
        self.gateways_list = []
        # ----
        self.local_photo_folder_path = ""
        # ----
        self.sequence_photos = []
        # ----

    def run(self) -> None:
        # ----
        super().run()
        # ----
        self.subscribe_command(
            callback=self.gateway_ready_callback,
            topic=PyDSLRGateway.DSLR_GATEWAY_READY_TOPIC
        )
        # ----
        self.get_dslr_gateways()
        # ----

    # ----------------------------------------------------
    #                   Methodes
    # ----------------------------------------------------

    def get_dslr_gateways(self):
        # ----
        # print("scan_dslr_gateways")
        # ----
        pass

    def network_scan_dslr_gateways(self):
        # ----
        # print("network_scan_dslr_gateways")
        # ----
        # add network scan callbacks
        # ----
        self.subscribe_command(
            callback=self.ip_live_finded_callback,
            topic=PyNetworkScan.IP_LIVE_FINDED_TOPIC
        )
        # ----
        self.scanner = PyNetworkScan(target=self.gateways_base_ip)
        # ----

    def create_gateway(self, payload=None):
        # ----
        # print("create gateway payload: {}".format(payload))
        # ----
        pass
        # ----

    def validate_gateway(self, payload=None):
        # ----
        # print("validate gateway by payload: {}".format(payload))
        # ----
        pass

    def get_gateway_by_ip(self, tmp_ip) -> PyDSLRGateway:
        # ----
        tmp_gw = None
        # ----
        """
        for g_way  in self.gateways_list:
            # ----
            if g_way.ip_adress == tmp_ip:
                # ----
                tmp_gw = g_way
                # ----
        # ----
        """
        return tmp_gw
        # ----

    # ----------------------------------------------------
    #                   Callbacks
    # ----------------------------------------------------

    def ip_live_finded_callback(self, payload=None):
        # ----
        # print("ip_live_finded_callback payload:{}".format(payload))
        # ----
        tmp_list = json.loads(payload)["live_ip"]
        for item in tmp_list:
            # ----
            tmp_dict_item = dict(
                gateway_ip=item
            )
            # ----
            if self.validate_gateway(payload=json.dumps(tmp_dict_item)):
                # ----
                self.gateways_create_iterator += 1
                # ----
                tmp_dict_item["camera_order"] = self.gateways_create_iterator
                # ----
                self.create_gateway(payload=json.dumps(tmp_dict_item))
                # ----

    def gateway_ready_callback(self, payload=None):
        # ----
        tmp_gw_dict = json.loads(payload)
        # ----
        if tmp_gw_dict:
            self.gateways_list.append(tmp_gw_dict)
        # ----

    # ----------------------------------------------------
    #            TOPIC's
    # ------------------------------------

    # COMMMANS
    SET_MATRIX_ORDERS_TOPIC = "SET_MATRIX_ORDERS"
    SET_MATRIX_CAMERAS_NUMBER_TOPIC = "SET_MATRIX_CAMERAS_NUMBER"

    # EVENTS
    DSLR_MATRIX_READY_TOPIC = "DSLR_MATRIX_READY"
    DSLR_MATRIX_EROOR_TOPIC = "DSLR_MATRIX_EROOR"
