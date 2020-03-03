"""
ToDo:
"""
import re


class PyDSLR:

    def __init__(self):

        self.cameramodel = ""
        self.deviceversion = ""
        self.eosserialnumber = ""
        self.serialnumber = ""
        self.order = 0

        # ---
        # print("init camera")
        # ---

    def set_camera_order_from_config_name(self, config_name=None):
        """
        Camera details from artist/author menu config
        Author: order={order}
        e.g:
        Author
        order=n

        * value in menu camera can take 63 characters

        * The serial number for your EOS camera will generally be 12 digits long,
        however for some older models the serial number may be 6 or 10 digits long.
        """

        if config_name and config_name != "":
            reg_query = '(?<=order=)([^&]*)(?=&)?'
            self.order = int(re.findall(reg_query, config_name)[0])
