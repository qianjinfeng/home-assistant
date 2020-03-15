"""Aligenie HTTP interface."""
import logging

from homeassistant.components.http.view import HomeAssistantView
import homeassistant.core as ha

from .const import API_HEADER
from .errors import AligenieError, AligenieInvalidDirectiveError
from .handlers import HANDLERS
from .messages import AligenieRequest

_LOGGER = logging.getLogger(__name__)
HOME_SKILL_HTTP_ENDPOINT = "/api/aligenie/home_skill"


async def async_handle_message(hass, config, request, context=None):
    """Handle incoming API messages."""
    assert request[API_HEADER]["payloadVersion"] == 1

    if context is None:
        context = ha.Context()

    directive = AligenieRequest(request)

    try:
        if directive.has_device:
            directive.load_entity(hass, config)

        funct_ref = HANDLERS.get((directive.namespace, directive.name))
        if funct_ref:
            response = await funct_ref(hass, config, directive, context)
        else:
            funct_ref = HANDLERS.get((directive.namespace))
            if funct_ref:
                response = await funct_ref(hass, config, directive, context)
            else:
                raise AligenieInvalidDirectiveError(directive.name)
    except AligenieError as err:
        response = directive.error(
            error_code=err.error_code, error_message=err.error_message
        )
    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.error("handle message exception %s", err)
        response = directive.error()

    return response.serialize()


async def async_setup(hass, config):
    """Activate Home Skill functionality of Aligenie component.

    This is optional, triggered by having a `home_skill:` sub-section in the
    aligenie configuration.
    """
    hass.http.register_view(HomeSkillView(hass, config))


class HomeSkillView(HomeAssistantView):
    """Expose Home Skill v1 payload interface via HTTP POST."""

    url = HOME_SKILL_HTTP_ENDPOINT
    name = "api:aligenie:home_skill"

    def __init__(self, hass, home_skill_config):
        """Initialize."""
        self.home_skill_config = home_skill_config
        self.hass = hass

    async def post(self, request):
        """Handle Aligenie Home Skill requests."""
        message = await request.json()

        _LOGGER.debug("Received Aligenie Home Skill request: %s", message)

        response = await async_handle_message(
            self.hass, self.home_skill_config, message
        )
        _LOGGER.debug("Sending Aligenie Home Skill response: %s", response)
        return b"" if response is None else self.json(response)
