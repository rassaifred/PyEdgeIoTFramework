from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PyArduino(EdgeService):

    def __int__(self):
        EdgeService.__init__(self)

    def run(self) -> None:
        EdgeService.run(self)
