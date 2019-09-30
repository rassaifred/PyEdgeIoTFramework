from pyedgeiotframework.core.EdgeService import EdgeService


class PyHost(EdgeService):

    POWER_OFF_HOST_TOPIC = "power_off_host_topic"

    def __int__(self):
        # ---
        EdgeService.__init__(self)
        # ---

    def run(self) -> None:
        # ---
        EdgeService.run(self)
        # ---
        self.subscribe_command(
            callback=self.power_off_host_callback,
            topic=self.POWER_OFF_HOST_TOPIC
        )
        # ---
        while True:
            pass

    def power_off_host_callback(self, payload=None):
        print("Host power off")