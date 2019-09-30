"""
ToDo: make static ip e.g: 192.168.1.255 next time use local.orbitip.server with security param in Global Env Var
ToDo: make endpoint to control Orbite IP devices
ToDo: make bridge Orbite IP <=> PyPubSub
"""

from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PyOrbiteip(EdgeService):

    def __int__(self):
        # ----
        EdgeService.__init__(self)
        # ----

    def run(self) -> None:
        # ----
        EdgeService.run(self)
        # ----
