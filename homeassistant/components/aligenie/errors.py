"""Aligenie related errors."""
from homeassistant.exceptions import HomeAssistantError


class UnsupportedProperty(HomeAssistantError):
    """This entity does not support the requested Smart Home API property."""


class AligenieError(Exception):
    """Base class for errors that can be serialized for the Aligenie API.

    A handler can raise subclasses of this to return an error to the request.
    """

    error_code = None

    def __init__(self, error_message):
        """Initialize an Aligenie error."""
        Exception.__init__(self)
        self.error_message = error_message


class AligenieInvalidDeviceError(AligenieError):
    """The device in the request does not exist."""

    error_code = "DEVICE_IS_NOT_EXIST"

    def __init__(self, device_id):
        """Initialize invalid device error."""
        msg = f"The device {device_id} does not exist"
        AligenieError.__init__(self, msg)
        self.device_id = device_id


class AligenieInvalidDirectiveError(AligenieError):
    """Class to represent InvalidDirective errors."""

    error_code = "INVALIDATE_CONTROL_ORDER"

    def __init__(self, directive_name):
        """Initialize invalid device error."""
        msg = f"The device {directive_name} does not exist"
        AligenieError.__init__(self, msg)
        self.directive_name = directive_name


class AligenieUnsupportedFunctionError(AligenieError):
    """Class to represent UnsupportedFunction errors."""

    error_code = "DEVICE_NOT_SUPPORT_FUNCTION"

    def __init__(self):
        """Initialize invalid function error."""
        AligenieError.__init__(self, "function not support")
