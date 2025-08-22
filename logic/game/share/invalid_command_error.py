class InvalidCommandError(Exception):
    def __init__(self, message):
        if not message:
            raise ValueError("A message is required for InvalidOperationError")
        super().__init__(message)
