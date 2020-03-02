import os
import multiprocessing
import subprocess
import socket
import pycurl
from io import BytesIO


from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyCamFi import PyCamFi


class PyCamFiMatrix(EdgeService):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.cafmi_list = []
        # ----

    def run(self) -> None:
        # ----
        super().run()
        # ----
        self.cafmi_list = self.map_network()
        # ----
        # print(cafmi_list)
        # ----
        for c_ip in self.cafmi_list:
            #for x in range(0, 29):
            camfi = PyCamFi()
            camfi.ip_adress = c_ip
            camfi.start()

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

    def map_network(self, pool_size=255):  # (pool_size=255):
        """
        Maps the network
        :param pool_size: amount of parallel ping processes
        :return: list of valid ip addresses
        """

        ip_list = list()

        # compose a base like 192.168.1.xxx
        base_ip = "192" + '.' + "168" + '.9.'

        # prepare the jobs queue
        jobs = multiprocessing.Queue()
        results = multiprocessing.Queue()

        pool = [multiprocessing.Process(target=self.pinger, args=(jobs, results)) for i in range(pool_size)]

        for p in pool:
            p.start()

        # cue hte ping processes
        for i in range(1, 256):  # range(1, 256):
            jobs.put(base_ip + '{0}'.format(i))

        for p in pool:
            jobs.put(None)

        for p in pool:
            p.join()

        # collect he results
        while not results.empty():
            ip = results.get()
            # ip_list.append(ip)
            # ----
            # creates a new socket using the given address family.
            socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # setting up the default timeout in seconds for new socket object
            socket.setdefaulttimeout(.3)

            # returns 0 if connection succeeds else raises error
            result = socket_obj.connect_ex((ip, PyCamFi.SOCKET_CAMFI_PORT))  # address and port in the tuple format

            # print(ip, "-", result)

            # closes te object
            socket_obj.close()

            if result == 0:
                #
                url_str = "{}{}{}".format(PyCamFi.REST_API_CAMFI_PROTOCOL, ip, PyCamFi.REST_API_CAMFI_GET_INFO)
                # print(url_str)

                #
                b_obj = BytesIO()
                crl = pycurl.Curl()

                # Set URL value
                crl.setopt(crl.URL, url_str)

                # Write bytes that are utf-8 encoded
                crl.setopt(crl.WRITEDATA, b_obj)

                # Perform a file transfer
                crl.perform()

                # End curl session
                crl.close()

                # Get the content stored in the BytesIO object (in byte characters)
                get_body = b_obj.getvalue()

                # Decode the bytes stored in get_body to HTML and print the result
                # print('Output of GET request:\n%s' % get_body.decode('utf8'))

                #
                if get_body:
                    #
                    ip_list.append(ip)

        return ip_list