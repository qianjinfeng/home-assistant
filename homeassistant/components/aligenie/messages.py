"""Aligenie message models."""
import logging

from .const import API_DEVICE, API_HEADER, API_MESSAGEID, API_PAYLOAD
from .errors import AligenieInvalidDeviceError

_LOGGER = logging.getLogger(__name__)


class AligenieRequest:
    """An incoming Aligenie directive."""

    def __init__(self, request):
        """Initialize a directive."""
        self._directive = request
        self.namespace = self._directive[API_HEADER]["namespace"]
        self.name = self._directive[API_HEADER]["name"]
        self.messageid = self._directive[API_HEADER][API_MESSAGEID]
        self.payload = self._directive[API_PAYLOAD]
        self.has_device = API_DEVICE in self.payload

        self.entity = self.entity_id = None

    def load_entity(self, hass, config):
        """Load Home Assistant entity."""
        self.entity_id = self.payload[API_DEVICE]

        self.entity = hass.states.get(self.entity_id)
        if not self.entity:
            raise AligenieInvalidDeviceError(self.entity_id)

    def response(self, payload=None):
        """Create an API formatted response."""
        payload = payload or {"deviceId": self.entity_id}
        response = AligenieReponse(
            self.name + "Response", self.namespace, self.messageid, payload
        )

        return response

    def error(
        self, error_code="SERVICE_ERROR", error_message="", payload=None,
    ):
        """Create a API formatted error response."""
        payload = payload or {}
        payload["deviceId"] = self.entity_id
        payload["errorCode"] = error_code
        payload["message"] = error_message

        _LOGGER.info(
            "Request %s/%s error %s: %s",
            self._directive[API_HEADER]["namespace"],
            self._directive[API_HEADER]["name"],
            error_code,
            error_message,
        )

        return AligenieReponse("ErrorResponse", self.namespace, self.messageid, payload)


class AligenieReponse:
    """Class to hold a response."""

    def __init__(self, name, namespace, messageid, payload=None):
        """Initialize the response."""
        payload = payload or {}
        self._response = {
            API_HEADER: {
                "namespace": namespace,
                "name": name,
                "messageId": messageid,
                "payloadVersion": 1,
            },
            API_PAYLOAD: payload,
        }

    @property
    def name(self):
        """Return the name of this response."""
        return self._response[API_HEADER]["name"]

    @property
    def namespace(self):
        """Return the namespace of this response."""
        return self._response[API_HEADER]["namespace"]

    def _properties(self):
        return self._response.setdefault("properties", [])

    def merge_property(self, prop):
        """Add a property."""
        self._properties().append(prop)

    def merge_properties(self, props):
        """Add all properties if not already set."""
        properties = self._properties()
        already_set = {p["name"] for p in properties}

        for prop in props:
            if prop["name"] not in already_set:
                self._properties().append(prop)

    def serialize(self):
        """Return response as a JSON-able data structure."""
        return self._response
