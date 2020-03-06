"""
ToDo: ok - add DSLR_Gateway class as parent of every gateway, e.g: PyCamFi
ToDo: ok - verify if camfi-adress
ToDo: extract scan ip methodes to PyNetworkScan
ToDo: add Dispatch Camera Added Event
ToDo: subscribe to listen trigger Set_Order send from front
ToDo: subscribe to set_camera mqtt
ToDo: subscribe to set_matrix_order mqtt
ToDo: add Environment VAR for matrix_cameras_number
ToDo: add camera order
ToDo: add loading file_added
ToDo: add Dispatch photo downloaded event
ToDo: add fail scenarios
"""

import json
import os
import multiprocessing
import subprocess

from PyEdgeIoTFramework.pyedgeiotframework.northbound.PyDSLRMatrix import PyDSLRMatrix
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyDSLRCamFi import PyCamFi


class PyCamFiMatrix(PyDSLRMatrix):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.matrix_len = 1
        self.matrix_orders = {}
        self.matrix_root_path = ""
        self.matrix_sequences_date = ""
        self.matrix_sequences_iteration = 0
        # ----
        self.matrix_base_ip = "192" + '.' + "168" + '.9.'
        # ----
        self.ips_list = []

    def run(self) -> None:
        # ----
        super().run()
        # ----
        self.ips_list = self.map_network()
        # ----
        # print(ips_list)
        # ----
        itt = 1
        # ----
        for c_ip in self.ips_list:
            # ---
            # for x in range(0, 29):
            # ---
            camfi = PyCamFi()
            camfi.camera.order = itt
            camfi.ip_adress = c_ip
            camfi.start()
            # ---
            self.gatways_list.append(camfi)
            # ---
            itt += 1
            # ---

    def camera_added_callback(self, payload=None):
        # ----
        super().camera_added_callback(payload=payload)
        # ----

    def camera_removed_callback(self, payload=None):
        # ----
        super().camera_removed_callback(payload=payload)
        # ----

    def file_added_callback(self, payload=None):
        # ----
        super().file_added_callback(payload=payload)
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

    def set_matrix_camera_order(self, tmp_id=None, tmp_order=None):
        super().set_matrix_camera_order(tmp_id=tmp_id, tmp_order=tmp_order)

    def set_matrix_orders(self, data=None):
        super().set_matrix_orders(data=data)

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
