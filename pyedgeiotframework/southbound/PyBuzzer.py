from pyedgeiotframework.core.EdgeService import EdgeService
from gpiozero import Buzzer

buzzGpio = 27


def buzzer_beep():
    bz = Buzzer(buzzGpio)
    bz.beep(.1, .1, 1)


class PyBuzzer(EdgeService):

    BUZZER_BEEP_TOPIC = "buzzer_beep_topic"

    def __int__(self):
        # ----
        EdgeService.__init__(self)
        # ----

    def run(self) -> None:
        # ----
        EdgeService.run(self)
        # ----

