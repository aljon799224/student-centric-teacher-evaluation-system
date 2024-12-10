"""Exceptions."""


class CustomException(Exception):
    """Custom Exception."""

    def __init__(self, status_code: int, detail: str):
        """Initialize with status code and detail message."""
        self.status_code = status_code
        self.detail = detail


class DatabaseException(CustomException):
    """Database Exception."""

    pass


class APIException(CustomException):
    """API Exception."""

    pass
