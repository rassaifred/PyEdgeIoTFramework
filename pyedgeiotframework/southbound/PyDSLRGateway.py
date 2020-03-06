from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyDSLR import PyDSLR


class PyDSLRGateway(EdgeService):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.camera = PyDSLR()
        # ----
        self.ip_adress = "0.0.0.0"
        self.mac = "-"
        # ----

    def run(self):
        # ----
        super().run()
        # ----

    def set_camera_order(self, tmp_order=None):
        # ---
        print("set Cmaera Order: {}".format(tmp_order))
        # ---

    # ----------------------------------------------------
    #            TOPIC's
    # ----------------------------------------------------

    CAMERA_ADDED_TOPIC = "CAMERA_ADDED"
    CAMERA_REMOVED_TOPIC = "CAMERA_REMOVED"
    FILE_ADDED_TOPIC = "FILE_ADDED"
    CAMERA_ERROR_TOPIC = "CAMERA_ERROR"
    DSLR_GATEWAY_ERROR_TOPIC = "DSLR_GATEWAY_ERROR"
