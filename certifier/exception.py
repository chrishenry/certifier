
class CertifierException(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, host, message):
        self.host = host
        self.message = message

class CertifierWarningException(CertifierException):
    """Base class for exceptions in this module."""

    def __init__(self, host, message):
        self.host = host
        self.message = message
