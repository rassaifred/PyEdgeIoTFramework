"""
ToDo: ok - verify if camfi-adress
ToDo: extract scan ip methodes to PyNetworkScan
ToDo: add Dispatch Camera Added Event to trigger Order send form front
ToDo: add camera order
ToDo: add loading file_added
ToDo: add Dispatch photo downloaded event
"""

import json
import os
import multiprocessing
import subprocess

from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyCamFi import PyCamFi


class PyCamFiMatrix(EdgeService):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.matrix_len = 1
        self.matrix_root_path = ""
        self.matrix_sequences_date = ""
        self.matrix_sequences_iteration = 0
        # ----
        self.matrix_base_ip = "192" + '.' + "168" + '.9.'
        # ----
        self.cafmi_list = []
        # ----

    def run(self) -> None:
        # ----
        super().run()
        # ----
        self.subscribe_command(
            callback=self.camera_added_callback,
            topic=PyCamFi.CAMFI_CAMERA_ADDED_TOPIC
        )

        self.subscribe_command(
            callback=self.camera_removed_callback,
            topic=PyCamFi.CAMFI_CAMERA_REMOVED_TOPIC
        )

        self.subscribe_command(
            callback=self.file_added_callback,
            topic=PyCamFi.CAMFI_FILE_ADDED_TOPIC
        )
        # ----
        self.cafmi_list = self.map_network()
        # ----
        # print(cafmi_list)
        # ----
        itt = 1
        # ----
        for c_ip in self.cafmi_list:
            # ---
            # for x in range(0, 29):
            # ---
            camfi = PyCamFi()
            camfi.camera.order = itt
            camfi.ip_adress = c_ip
            camfi.start()
            # ---
            itt += 1
            # ---

    def camera_added_callback(self, payload=None):
        pass

    def camera_removed_callback(self, payload=None):
        pass

    def file_added_callback(self, payload=None):
        # ----
        tmp_dct = json.loads(payload)
        # ----
        gateway = tmp_dct["gateway"]
        file_added = tmp_dct["file_added"]
        camera_order = tmp_dct["camera_order"]
        # ----
        response = PyCamFi.get_photo_by_path(None, tmp_ip=gateway, path=file_added)
        # ----
        if response.status_code == 200:
            # ----
            file_save_url = "{}/{}/{}_{}.JPG".format(
                self.matrix_root_path,
                self.matrix_sequences_date,
                camera_order,
                self.matrix_sequences_iteration
            )
            # ----
            pass
            with open(file_save_url, 'wb') as f:
                f.write(response.content)
                # ---
                # Dispatch photo downloaded event
                # ---

    @staticmethod
    def validate_camfi_ip(tmp_ip):
        # verify ip
        data = json.dumps(PyCamFi.get_camfi_info(None, tmp_ip=tmp_ip))
        tmp_dect = json.loads(data)
        if tmp_dect["version"]:
            return True
        else:
            return False

    # ----------------------------------------------------
    #                   SCAN IPs
    # ----------------------------------------------------

    def pinger(self, job_q, results_q):
        DEVNULL = open(os.devnull, 'w')
        while True:
            ip = job_q.get()
            if ip is None:
                break
            try:
                subprocess.check_call(['ping', '-c1', ip], stdout=DEVNULL)
                results_q.put(ip)
            except:
                pass

    def map_network(self, pool_size=4):  # (pool_size=255):
        """
        Maps the network
        :param pool_size: amount of parallel ping processes
        :return: list of valid ip addresses
        """

        ip_list = list()

        # compose a base like 192.168.1.xxx
        # base_ip = "192" + '.' + "168" + '.9.'

        # prepare the jobs queue
        jobs = multiprocessing.Queue()
        results = multiprocessing.Queue()

        pool = [multiprocessing.Process(target=self.pinger, args=(jobs, results)) for i in range(pool_size)]

        for p in pool:
            p.start()

        # cue hte ping processes
        for i in range(66, 69):  # range(1, 256):
            jobs.put(self.matrix_base_ip + '{0}'.format(i))

        for p in pool:
            jobs.put(None)

        for p in pool:
            p.join()

        # collect he results
        while not results.empty():
            ip = results.get()
            # verify ip
            if self.validate_camfi_ip(ip):
                ip_list.append(ip)
                return ip_list
