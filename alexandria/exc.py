class AlexandriaException(Exception):
    """Base class for all Alexandria exceptions"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class DocumentNotFound(AlexandriaException):
    """Exception raised when no CouchDB document exists for a given ID"""

    pass


class EditConflict(AlexandriaException):
    """Exception raised when a document update/creation conflicts with an
    earlier update (or the document already exists)"""

    pass


class HostNotFound(AlexandriaException):
    """Exception raised when a host is not found on the network"""

    pass
