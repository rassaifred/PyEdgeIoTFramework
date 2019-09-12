from gpiozero import Buzzer

buzzGpio = 27


def buzzer_beep():
    bz = Buzzer(buzzGpio)
    bz.beep(.1, .1, 1)
