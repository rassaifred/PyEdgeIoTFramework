"""
ToDo: add listen camera config chnage over PubSub from camera_id topic
ToDo: add listen photo number chnage over PubSub

* every gateway have exslusivly single camera

"""

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
        self.photo_number = 0
        # ----

    def run(self):
        # ----
        super().run()
        # ----

    def set_camera_order(self, tmp_order=None):
        # ---
        print("set Cmaera Order: {}".format(tmp_order))
        # ---
        if tmp_order:
            # ---
            self.camera.order = int(tmp_order)
            # ---

    def get_photo_from_camera(self, payload=None):
        # ----
        print("get photo: {}".format(payload))
        # ----

    def save_photo_from_camera(self, tmp_data=None):
        # ----
        print("save photo from camera")
        # ----
        self.camera.save_photo_loadded_from_camera(
            tmp_num_photo=self.photo_number,
            tmp_photo_data=tmp_data
        )
        # ----

    # ----------------------------------------------------
    #            TOPIC's
    # ----------------------------------------------------

    DSLR_GATEWAY_ERROR_TOPIC = "DSLR_GATEWAY_ERROR"
