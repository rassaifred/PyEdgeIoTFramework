"""
ToDo: extract scan ip functions to PyNetworkScan
ToDo: add PyNetworkScan based on test_ping.py
ToDo: add plug&play feature with rescan gateways
ToDo: add change photo number via PubSub
ToDo: add timeout for staying adding photo
"""

import os
import multiprocessing
import subprocess


from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyDSLRGateway import PyDSLRGateway
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyDSLR import PyDSLR


class PyDSLRMatrix(EdgeService):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.gateways_base_ip = "192" + '.' + "168" + '.10.'
        self.gateways_number = 1
        self.gateways_list = []
        self.gateways_ips_list = []
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
            callback=self.camera_added_callback,
            topic=PyDSLR.CAMERA_ADDED_TOPIC
        )

        self.subscribe_command(
            callback=self.camera_removed_callback,
            topic=PyDSLR.CAMERA_REMOVED_TOPIC
        )

        self.subscribe_command(
            callback=self.file_added_callback,
            topic=PyDSLR.FILE_ADDED_TOPIC
        )
        # ----
        self.gateways_ips_list = self.scan_dslr_gateways()
        # ----

    # ----------------------------------------------------
    #                   Methodes
    # ----------------------------------------------------

    def validate_gateway(self, tmp_ip):
        # ----
        print("validate gateway by ip: {}".format(tmp_ip))
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

    def scan_dslr_gateways(self):
        # ----
        print("scan_dslr_gateways")
        # ----
        return self.map_network()
        # ----

    def get_gateway_by_ip(self, tmp_ip) -> PyDSLRGateway:
        # ----
        tmp_gw = None
        # ----
        for g_way in self.gateways_list:
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
    #                   SCAN IPs
    # ----------------------------------------------------

    def pinger(self, job_q, results_q):
        # ----
        DEVNULL = open(os.devnull, 'w')
        # ----
        while True:
            # ----
            ip = job_q.get()
            # ----
            if ip is None:
                break
            # ----
            print("ip pinger: {} command: {}".format(ip,['ping', '-c1', ip]))
            # ----
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
        for i in range(66, 70):  # range(1, 256):
            jobs.put(self.gateways_base_ip + '{0}'.format(i))

        for p in pool:
            jobs.put(None)

        for p in pool:
            p.join()

        # collect he results
        while not results.empty():
            ip = results.get()
            # verify ip
            if self.validate_gateway(ip):
                ip_list.append(ip)
                return ip_list

    # ----------------------------------------------------
    #            TOPIC's
    # ------------------------------------

    # COMMMANS
    SET_CAMERA_ORDER_TOPIC = "SET_CAMERA_ORDER"
    SET_MATRIX_ORDERS_TOPIC = "SET_MATRIX_ORDERS"
    SET_MATRIX_CAMERAS_NUMBER_TOPIC = "SET_MATRIX_CAMERAS_NUMBER"

    # EVENTS
    MATRIX_EROOR_TOPIC = "MATRIX_EROOR"
