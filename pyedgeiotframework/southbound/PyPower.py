import os
from pyedgeiotframework.core.EdgeService import EdgeService
from gpiozero import Button

pwrBtnGpio = 22


def power_off():
    # ---------
    try:
        os.environ['DBUS_SESSION_BUS_ADDRESS'] = "unix:path=/host/run/dbus/system_bus_socket"
        print("--> dbus adress: ", os.environ['DBUS_SESSION_BUS_ADDRESS'])
    except:
        print("impossible de charger DBUS_SESSION_BUS_ADDRESS")
    # ---------
    cmd_str = 'dbus-send --system --print-reply --dest=org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager.PowerOff'
    print("-->", cmd_str)
    # ---------
    try:
        dbus_run = os.popen(cmd_str).read().rstrip()
        print("-->", dbus_run)
    except:
        print("impossible d'executer dbus-send poweroff")


def reboot():
    # ---------
    try:
        os.environ['DBUS_SESSION_BUS_ADDRESS'] = "unix:path=/host/run/dbus/system_bus_socket"
        print("--> dbus adress: ", os.environ['DBUS_SESSION_BUS_ADDRESS'])
    except:
        print("impossible de charger DBUS_SESSION_BUS_ADDRESS")
    # ---------
    cmd_str = 'dbus-send --system --print-reply --dest=org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager.Reboot'
    print("-->", cmd_str)
    # ---------
    try:
        dbus_run = os.popen(cmd_str).read().rstrip()
        print("-->", dbus_run)
    except:
        print("impossible d'executer dbus-send reboot")


class PyPower(EdgeService):

    def __init__(self):
        EdgeService.__init__(self)
        # ----
        self.myButton = Button(pwrBtnGpio)
        # ----

    def run(self):
        # ----
        EdgeService.run(self)
        # ----
        self.myButton.when_released = self.btn_release
        # ----

    def btn_release(self):
        power_off()

