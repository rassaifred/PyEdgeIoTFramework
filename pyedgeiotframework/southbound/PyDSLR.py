"""
ToDo: Make order and cameras numbers in config DSLR

-----------------------
order=6/14
6 is order
14 is count of cameras
-----------------------


camera payload json:
{
    "camera_id": "",
    "gateway_ip":"",
    "camera_order":""
}

photo path:
    filename + "." + extension
    -> order + "_" + photo number + "_" + day + "_" + month " "_" + year + "." + extension
e.g:
    1_350_12_05_20.JPG
    -> filename = 1_350_12_05_20
    -> extension = JPG

"""
import json
import re
from datetime import date
from pubsub import pub


class PyDSLR:

    def __init__(self):
        # ----
        self.camera_id = ""
        self.cameramodel = ""
        self.deviceversion = ""
        self.eosserialnumber = ""
        self.serialnumber = ""
        # ----
        self.camera_order = 0
        self.photo_number = 0
        self.photo_date_str = date.today().strftime("%d_%m_%y")
        self.local_photo_folder_path = "assets/photos"
        # ----
        # print("init camera")
        # ----

    @property
    def eosserialnumber(self):
        return self.__eosserialnumber

    @eosserialnumber.setter
    def eosserialnumber(self, eosserialnumber):
        self.__eosserialnumber = eosserialnumber
        self.camera_id = eosserialnumber

    # ----------------------------------------------------
    #                   Methodes
    # ----------------------------------------------------

    def set_camera_order_from_config_name(self, config_name=None) -> bool:
        result = False
        if config_name and config_name != "":
            self.camera_order = self.get_camera_order_from_config_name(config_name=config_name)
            result = True
        return result

    def get_camera_order_from_config_name(self, config_name=None) -> int:

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

        reg_query = '(?<=order=)([^&]*)(?=&)?'

        tmp_order = None

        if config_name and config_name != "":
            result = re.findall(reg_query, config_name)
            if len(result) > 0:
                tmp_str = result[0]
                tmp_order = int(tmp_str)

        return tmp_order

    def save_photo_loadded_from_camera(self, tmp_num_photo=None, tmp_photo_data=None):

        # ----
        self.photo_date_str = date.today().strftime("%d_%m_%y")
        # ----
        self.photo_number = tmp_num_photo if tmp_num_photo else self.photo_number + 1
        # ----
        save_path = self.PHOTO_NAME_PATH_TEMPLATE.format(
            self.local_photo_folder_path,
            self.camera_order,
            self.photo_number,
            self.photo_date_str
        )
        # ----
        if tmp_photo_data:
            # ----
            # print("start saving file {}".format(save_path))
            # ----
            with open(save_path, 'wb') as f:
                f.write(tmp_photo_data.content)
                # ---
                # Dispatch photo downloaded event
                # ---
                pub.sendMessage(
                    topicName=self.PHOTO_LOADDED_FROM_CAMERA_TOPIC,
                    payload=json.dumps(
                        dict(
                            camera_id=self.camera_id,
                            camera_order=self.camera_order,
                            photo_number=self.photo_number,
                            photo_date_str=self.photo_date_str,
                            photo_path=save_path
                        )
                    )
                )

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

    SET_CAMERA_ORDER_TOPIC = "SET_CAMERA_ORDER"