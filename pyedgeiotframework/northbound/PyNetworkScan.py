"""
ToDo: extract scan ip methodes to PyNetworkScan
ToDo: in PyNetworkScan dispatch an event whenever an ip is online to verify it
ToDo: scenario ->
        - first luanch scan and list live ips
        - dispatch scan finished
"""

import json
import os, multiprocessing, time, platform

from pubsub import pub


class PyNetworkScan:

    def __init__(self, target=None):
        # ----
        self.commad = ""
        self.live_ip_collector = multiprocessing.Queue()
        self.live_ip_list = []
        self.thread = 255
        self.timeout = 1
        self.target = target if target else "192:168:1:1-255"
        self.output = None
        self.timestarted = None
        self.timeclose = None
        self.start_scan()

    def start_scan(self):
        self.timestarted = time.time()
        self.set_os_command()
        self.scanning_boosters()
        # ----

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, target):
        self.__target = IP_extractor(target)

    # ----------------------------------------------------
    #                   Methodes
    # ----------------------------------------------------

    # Saving OUtput
    def save_output(self):
        f = open(self.output, 'a')
        for i in self.live_ip_collector:
            f.write(i + '\n')
        f.close()
        return

    # Function For Multi_processing
    def scanning_boosters(self):
        proces = []
        for ip in self.target:
            k = len(multiprocessing.active_children())
            if k == self.thread:
                time.sleep(3)
                self.thread = self.thread + 30
            mythread = multiprocessing.Process(
                target=self.checkping,
                args=(ip,)
            )
            mythread.start()
            proces.append(mythread)

        for mythread in proces:
            mythread.join()

        self.timeclose = time.time()

        # print("end")

        self.showing_results()

        return

    # Printing Function
    def showing_results(self):
        storeip = []
        x = 1
        while x == 1:
            try:
                storeip.append(self.live_ip_collector.get_nowait())
            except:
                x = x + 1

        self.live_ip_collector = storeip

        self.timeclose = time.time()

        print("\n" * 1)
        print("#" * 80)
        print("[+] Scan Started On \t\t:\t", time.ctime(self.timestarted))
        print("[+] Scan Closed On  \t\t:\t", time.ctime(self.timeclose))
        print("[+] Scan Total Duration \t:\t", self.timeclose - self.timestarted)
        print("[+] Total Live System Answered\t:\t", len(self.live_ip_collector))
        print("#" * 80, "\n" * 1)

        if self.output:
            self.save_output()

        # ----
        for i in self.live_ip_collector:
            self.live_ip_list.append(i)
        # ----
        pub.sendMessage(
            topicName=self.IP_LIVE_FINDED_TOPIC,
            payload=json.dumps(
                dict(
                    live_ip=self.live_ip_list
                )
            )
        )
        # ----

        return

    # Command Selecting Function
    def set_os_command(self):
        oper = platform.system()
        if oper == "Windows":
            ping = "ping -n {} {}"
        elif oper == "Linux":
            ping = "ping -c {} {}"
        else:
            ping = "ping -c {} {}"
        self.commad = ping
        return

    # Function for Checking IP Status
    def checkping(self, ip):
        # ----
        # print("[+]\t {}".format(ip))
        # ----
        ping = self.commad
        recv = os.popen(ping.format(self.timeout, ip)).read()
        recv = recv.upper()
        if recv.count('TTL'):
            # ----
            # print("[+]\t {} \t==> Live ".format(ip))
            # ----
            self.live_ip_collector.put(ip)
            # ----

        return

    # ----------------------------------------------------
    #            TOPIC's
    # ----------------------------------------------------

    IP_LIVE_FINDED_TOPIC = "IP_LIVE_FINDED"


# Extracting Number format
def extraction(port):
    storeport = []
    # Verifiying Port Value
    if port:
        # Verifying Port is in Range
        if "-" in port and "," not in port:
            x1, x2 = port.split('-')
            storeport = range(int(x1), int(x2))
        # Verifying Port is in Commas
        elif "," in port and "-" not in port:
            storeport = port.split(',')
        elif "," in port and "-" in port:
            x2 = []
            for i in port.split(','):
                if '-' in i:
                    y1, y2 = i.split('-')
                    x2 = x2 + range(int(y1), int(y2))
                else:
                    x2.append(i)
            storeport = x2
        else:
            storeport.append(port)
    else:
        pass
    return storeport


# Extracting Ip Address
def IP_extractor(ip):
    storeobj = []
    ip = ip.split(':')
    x1 = extraction(ip[0])
    x2 = extraction(ip[1])
    x3 = extraction(ip[2])
    x4 = extraction(ip[3])
    for i1 in x1:
        for i2 in x2:
            for i3 in x3:
                for i4 in x4:
                    storeobj.append("{}.{}.{}.{}".format(i1, i2, i3, i4))
    return storeobj
