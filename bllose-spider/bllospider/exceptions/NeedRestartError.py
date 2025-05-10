class NeedRestartError(Exception):
    def __init__(self, message="需要重新启动"):
        self.message = message
        super().__init__(self.message)