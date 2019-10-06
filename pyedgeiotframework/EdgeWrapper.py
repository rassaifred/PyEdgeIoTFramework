"""
ToDo: add services manager, to control stating and kill services (threads)

Description:

    EdgeWrapper ==> MicroService:
        mode:
            - solo mode (single device no distributed system)
            - network mode (multiple devices, as distributed system)
        context: Local Network
        Components:
            - software services tree
            - Web server
            - API (end points for every PyService)
            - Dashboard
            - Admin (for every PyService)

    EdgeService ==> SoftwareService:
        context: Host
        Components:
            - API registry to EdgeWrapper (using Flask & Blueprint)

"""

import os
import sentry_sdk
from sentry_sdk import configure_scope
import importlib
import sys
import signal


class EdgeWrapper:

    SENTRY_URL = None
    DEVICE_ID = None

    def __int__(self):
        # ----
        print(self.__class__.__name__ + ":init")
        # ----
        if os.getenv('SENTRY_URL'):
            self.SENTRY_URL = os.getenv('SENTRY_URL')
        # ----
        self.DEVICE_ID = "virtual_dev_{0}".format(os.name)
        # ----
        if os.getenv('CUSTOM_DEVICE_ID'):
            self.DEVICE_ID = os.getenv('CUSTOM_DEVICE_ID')
        # ----
        # ToDo: add default services
        # ----

    def startup_wrapper(self):
        # ----
        print(self.__class__.__name__ + ":startup_wrapper")
        # ----
        signal.signal(signal.SIGINT, self.interupt_sig_handler)
        # ----
        if self.SENTRY_URL:
            sentry_sdk.init(self.SENTRY_URL)
            # ---
            with configure_scope() as scope:
                scope.user = {"id": self.DEVICE_ID}
            # ----
        # ----
        # start load services
        # ----

    def interupt_sig_handler(self, sig, frame):
        print('Received interrupt signal')
        sys.exit(0)

    def modules_loading(self, module_package_name, module_name_arr):
        # help(__import__)
        # help(importlib.import_module)
        for item in module_name_arr:
            print("module_loading... " + item)
            module_object = importlib.import_module(module_package_name + "." + str(item))
            target_class = getattr(module_object, item)
            instance = target_class()
            instance.start()


"""
if __name__ == '__main__':
    mainWrapper = EdgeWrapper()
    mainWrapper.startup_wrapper()
"""
