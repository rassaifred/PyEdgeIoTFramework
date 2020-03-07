"""
ToDo: extract scan ip methodes to PyNetworkScan
ToDo: in PyNetworkScan dispatch an event whenever an ip is online to verify it
ToDo: scenario ->
        - first luanch scan and list on line ip
        - dispatch ip findded
        - contious scan network every interval
"""

# Importing Modules
import os, multiprocessing, time, platform

from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PyNetworkScan(EdgeService):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.base_ip = "192:168:1:1-255"
        # ----
        self.thread = 100
        self.timeout = 1
        # ----
        self.ips_list = []
        # ----

    def run(self) -> None:
        # ----
        super().run()
        # ----
        Pinger(
            target=IP_extractor(self.base_ip),
            thread=self.thread,
            timeout=self.timeout
        )
        # ----

    # ----------------------------------------------------
    #            TOPIC's
    # ----------------------------------------------------

    IP_LIVE_FIND_TOPIC = "IP_LIVE_FIND"

# Main Engine
class Pinger:
    def __init__(self, target=None, thread=None, output=None, timeout=None):
        self.commad = ""
        self.timestarted = time.time()
        self.live_ip_collector = multiprocessing.Queue()
        self.target = target
        self.thread = thread
        self.output = output
        self.timeout = timeout
        self.set_os_command()
        # self.checkping()
        self.scanning_boosters()

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
            mythread = multiprocessing.Process(target=self.checkping, args=(ip,))
            mythread.start()
            proces.append(mythread)

        for mythread in proces:
            mythread.join()

        self.timeclose = time.time()

        print("end")

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

        print("\n" * 3, "#" * 80)
        print("[+] Scan Started On \t\t:\t", time.ctime(self.timestarted))
        print("[+] Scan Closed On  \t\t:\t", time.ctime(self.timeclose))
        print("[+] Scan Total Duration \t:\t", self.timeclose - self.timestarted)
        print("[+] Total Live System Answered\t:\t", len(self.live_ip_collector))

        if self.output:
            self.save_output()

        print("\n[+] Thanks For Using My Program. By S.S.B")

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
        print("[+]\t {}".format(ip))
        ping = self.commad
        recv = os.popen(ping.format(self.timeout, ip)).read()
        recv = recv.upper()
        if recv.count('TTL'):
            print("[+]\t {} \t==> Live ".format(ip))
            self.live_ip_collector.put(ip)
        return


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

