class ControllerNotInstantiatedException(Exception):
    def __init__(self):
        self.message = "This controller has not been instantiated yet."
        super().__init__(self.message)
        