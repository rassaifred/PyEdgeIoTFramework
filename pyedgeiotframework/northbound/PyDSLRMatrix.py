from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyDSLRGateway import PyDSLRGateway


class PyDSLRMatrix(EdgeService):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.gatways_list = []
        # ----

    def run(self) -> None:
        # ----
        super().run()
        # ----
        self.subscribe_command(
            callback=self.camera_added_callback,
            topic=PyDSLRGateway.CAMERA_ADDED_TOPIC
        )

        self.subscribe_command(
            callback=self.camera_removed_callback,
            topic=PyDSLRGateway.CAMERA_REMOVED_TOPIC
        )

        self.subscribe_command(
            callback=self.file_added_callback,
            topic=PyDSLRGateway.FILE_ADDED_TOPIC
        )
        # ----

    def camera_added_callback(self, payload=None):
        # ----
        print("camera added payload:{}".format(payload))
        # ----

    def camera_removed_callback(self, payload=None):
        # ----
        print("camera removed payload:{}".format(payload))
        # ----

    def file_added_callback(self, payload=None):
        # ----
        print("file added payload:{}".format(payload))
        # ----

    def gat_gateway_by_ip(self, tmp_ip) -> PyDSLRGateway:
        # ----
        tmp_gw = None
        # ----
        for g_way in self.gatways_list:
            # ----
            if g_way.ip_adress == tmp_ip:
                # ----
                tmp_gw = g_way
                # ----
        # ----
        return tmp_gw
        # ----

    def set_matrix_camera_order(self, tmp_id=None, tmp_order=None):
        pass

    def set_matrix_orders(self, data=None):
        pass
    # ----------------------------------------------------
    #            TOPIC's
    # ------------------------------------

    # COMMMANS
    SET_CAMERA_ORDER_TOPIC = "SET_CAMERA_ORDER"
    SET_MATRIX_ORDERS_TOPIC = "SET_MATRIX_ORDERS"
    SET_MATRIX_CAMERAS_NUMBER_TOPIC = "SET_MATRIX_CAMERAS_NUMBER"

    # EVENTS
    MATRIX_EROOR_TOPIC = "MATRIX_EROOR"