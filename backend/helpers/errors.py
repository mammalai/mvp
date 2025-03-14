import json

class MVPError(Exception):
    """Base class for all MVP errors."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        if self.__cause__:
            return f"{self.message} (Caused by: {self.__cause__})"
            # return self.message
        else:
            return self.message

class PaypalError(Exception):
    def __init__(self, name, message, status_code, debug_id):
        super().__init__(message)
        self.name = name
        self.message = message
        self.status_code = status_code
        self.debug_id = debug_id

    def __str__(self):
        return f"{self.name}: {self.message} ({self.status_code}) - Details: (Debug ID: {self.debug_id})"
