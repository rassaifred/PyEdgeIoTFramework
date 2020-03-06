"""
ToDo:

photo path:
    filename + "." + extension
    -> order + "_" + photo number + "_" + day + "_" + month " "_" + year + "." + extension
e.g:
    1_350_12_05_20.JPG
    -> filename = 1_350_12_05_20
    -> extension = JPG
"""

import re
from datetime import date


class PyDSLR:

    def __init__(self):
        # ----
        self.cameramodel = ""
        self.deviceversion = ""
        self.eosserialnumber = ""
        self.serialnumber = ""
        # ----
        self.order = 0
        self.photo_number = 0
        self.photo_date_str = date.today().strftime("%d_%m_%y")
        self.local_photo_folder_path = "assets/photos"
        # ----
        # print("init camera")
        # ----

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

    def save_photo_loadded_from_camera(self, tmp_num_photo=None, tmp_photo_data=None):
        # ----
        self.photo_date_str = date.today().strftime("%d_%m_%y")
        # ----
        self.photo_number = tmp_num_photo if tmp_num_photo else self.photo_number + 1
        # ----
        save_path = self.PHOTO_NAME_PATH_TEMPLATE.format(
            self.local_photo_folder_path,
            self.order,
            self.photo_number,
            self.photo_date_str
        )
        # ----
        if tmp_photo_data:
            # ----
            print("start saving file {}".format(save_path))
            # ----
            # ---- dispatch camera photo loaded
        # ----

    # ----------------------------------------------------
    #            TEMPLATES
    # ----------------------------------------------------

    PHOTO_NAME_PATH_TEMPLATE = "{}/{}_{}_{}.JPG"

    # ----------------------------------------------------
    #            TOPIC's
    # ----------------------------------------------------

    CAMERA_ADDED_TOPIC = "CAMERA_ADDED"
    CAMERA_REMOVED_TOPIC = "CAMERA_REMOVED"
    PHOTO_LOADDED_FROM_CAMERA_TOPIC = "PHOTO_LOADDED_FROM_CAMERA"
    PHOTO_NUMBER_CHANGED_TOPIC = "PHOTO_NUMBER_CHANGED"
    FILE_ADDED_TOPIC = "FILE_ADDED"
    CAMERA_ERROR_TOPIC = "CAMERA_ERROR"