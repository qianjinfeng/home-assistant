"""Support for Aligenie skill service end point."""
import logging

import voluptuous as vol

from homeassistant.const import CONF_NAME
from homeassistant.helpers import config_validation as cv, entityfilter

from . import home_skill
from .const import (
    CONF_BAICHUANKEY,
    CONF_BAICHUANSECRET,
    CONF_FILTER,
    CONF_SKILLID,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

CONF_HOME_SKILL = "home_skill"

ALIGENIE_ENTITY_SCHEMA = vol.Schema({vol.Optional(CONF_NAME): cv.string})

HOME_SKILL_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_BAICHUANKEY): cv.string,
        vol.Optional(CONF_BAICHUANSECRET): cv.string,
        vol.Optional(CONF_SKILLID): cv.string,
        vol.Optional(CONF_FILTER, default={}): entityfilter.FILTER_SCHEMA,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: {
            # home_skill: and none at all.
            CONF_HOME_SKILL: vol.Any(HOME_SKILL_SCHEMA, None),
        }
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Activate the Aligenie component."""
    config = config.get(DOMAIN, {})

    try:
        home_skill_config = config[CONF_HOME_SKILL]
    except KeyError:
        pass
    else:
        home_skill_config = home_skill_config or HOME_SKILL_SCHEMA({})
        await home_skill.async_setup(hass, home_skill_config)

    return True
