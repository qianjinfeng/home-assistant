"""Aligenie entity adapters."""
from typing import List

from homeassistant.components import climate, fan, light, media_player, switch, vacuum
from homeassistant.const import ATTR_SUPPORTED_FEATURES, CLOUD_NEVER_EXPOSED_ENTITIES
from homeassistant.core import callback
from homeassistant.util.decorator import Registry

from .const import CONF_FILTER
from .errors import AligenieUnsupportedFunctionError
from .operations import (
    AligenieAdjustDownBrightness,
    AligenieAdjustDownColorTemperature,
    AligenieAdjustDownHumidity,
    AligenieAdjustDownTemperature,
    AligenieAdjustDownVolume,
    AligenieAdjustUpBrightness,
    AligenieAdjustUpColorTemperature,
    AligenieAdjustUpHumidity,
    AligenieAdjustUpTemperature,
    AligenieAdjustUpVolume,
    AligenieCloseSwing,
    AligenieNext,
    AligenieOpenSwing,
    AligeniePause,
    AligeniePlay,
    AligeniePrevious,
    AligenieSetBrightness,
    AligenieSetColor,
    AligenieSetColorTemperature,
    AligenieSetHumidity,
    AligenieSetTemperature,
    AligenieSetWindSpeed,
    AligenieTurnOff,
    AligenieTurnOn,
)
from .properties import (
    AligenieBrightness,
    AligenieColor,
    AligenieColorTemperature,
    AligenieHumidity,
    AligeniePowerState,
    AligenieTemperature,
    AligenieWindspeed,
)

ENTITY_ADAPTERS = Registry()


class AligenieEntity:
    """An adaptation of an entity, expressed in Aligenie's terms."""

    def __init__(self, hass, config, entity):
        """Initialize Alexa Entity."""
        self.hass = hass
        self.config = config
        self.entity = entity

    @property
    def device_id(self):
        """Return the Entity ID."""
        return self.entity.entity_id

    def device_name(self):
        """Return the Aligenie API friendly name."""
        return self.entity.attributes.get("friendly_name")

    def device_type(self):
        """Return Aligenie device type."""
        return self.entity.domain

    def get_operation(self, op_name):
        """Return the given AligenieOperation."""
        for operation in self.operations():
            if op_name == operation.name():
                return operation

        raise AligenieUnsupportedFunctionError()

    def operations(self):
        """Return a list of supported operations.

        Used for discovery. The list should contain AligenieOperation instances.
        If the list is empty, this entity will not be discovered.
        """
        raise NotImplementedError

    def properties(self):
        """Return a list of supported properties.

        Used for discovery. The list should contain AligenieProperty instances.
        If the list is empty, this entity will not be discovered.
        """
        raise NotImplementedError

    def serialize_properties(self):
        """Yield each supported property in API format."""
        for prop in self.properties():
            yield prop.serialize_property()

    def serialize_property(self, pro_name):
        """Return a property given the property name."""
        for prop in self.properties():
            result = prop.property_supported()
            if pro_name == result["name"]:
                return prop.serialize_property()

        raise AligenieUnsupportedFunctionError()

    def serialize_discovery(self):
        """Serialize the entity for discovery."""
        result = {
            "deviceId": self.device_id,
            "deviceType": self.device_type(),
            "deviceName": self.device_name(),
            "brand": "Home Assistant",
            "model": "test",
            "zone": "te",
            "icon": "https://home-assistant.io/images/favicon-192x192.png",
        }

        actions = []
        for i in self.operations():
            actions.append(i.name())
        result["actions"] = actions

        result["properties"] = list(self.serialize_properties())

        return result


@callback
def async_get_entities(hass, config) -> List[AligenieEntity]:
    """Return all entities that are supported by Aligenie."""
    entities = []
    for state in hass.states.async_all():
        if state.entity_id in CLOUD_NEVER_EXPOSED_ENTITIES:
            continue

        if state.domain not in ENTITY_ADAPTERS:
            continue

        if CONF_FILTER in config:
            entities_filter = config[CONF_FILTER]
            if not entities_filter(state.entity_id):
                continue

        aligenie_entity = ENTITY_ADAPTERS[state.domain](hass, config, state)

        if not list(aligenie_entity.operations()):
            continue

        entities.append(aligenie_entity)

    return entities


@ENTITY_ADAPTERS.register(light.DOMAIN)
class AligenieLight(AligenieEntity):
    """Class to represent Light in Aligenie term."""

    def operations(self):
        """Yield the supported operations."""
        yield AligenieTurnOn(self.hass, self.entity)
        yield AligenieTurnOff(self.hass, self.entity)

        supported = self.entity.attributes.get(ATTR_SUPPORTED_FEATURES, 0)
        if supported & light.SUPPORT_BRIGHTNESS:
            yield AligenieSetBrightness(self.hass, self.entity)
            yield AligenieAdjustUpBrightness(self.hass, self.entity)
            yield AligenieAdjustDownBrightness(self.hass, self.entity)
        if supported & light.SUPPORT_COLOR:
            yield AligenieSetColor(self.hass, self.entity)
        if supported & light.SUPPORT_COLOR_TEMP:
            yield AligenieSetColorTemperature(self.hass, self.entity)
            yield AligenieAdjustUpColorTemperature(self.hass, self.entity)
            yield AligenieAdjustDownColorTemperature(self.hass, self.entity)

    def properties(self):
        """Yield the supported properties."""
        yield AligeniePowerState(self.hass, self.entity)

        supported = self.entity.attributes.get(ATTR_SUPPORTED_FEATURES, 0)
        if supported & light.SUPPORT_BRIGHTNESS:
            yield AligenieBrightness(self.hass, self.entity)
        if supported & light.SUPPORT_COLOR:
            yield AligenieColor(self.hass, self.entity)
        if supported & light.SUPPORT_COLOR_TEMP:
            yield AligenieColorTemperature(self.hass, self.entity)


@ENTITY_ADAPTERS.register(climate.DOMAIN)
class AligenieClimate(AligenieEntity):
    """Class to represent Climate in Aligenie term."""

    def device_type(self):
        """Aligenie recoginzed type."""
        return "aircondition"

    def operations(self):
        """Yield the supported operations."""
        yield AligenieTurnOn(self.hass, self.entity)
        yield AligenieTurnOff(self.hass, self.entity)

        supported = self.entity.attributes.get(ATTR_SUPPORTED_FEATURES, 0)
        if supported & climate.SUPPORT_TARGET_TEMPERATURE_RANGE:
            yield AligenieSetTemperature(self.hass, self.entity)
            yield AligenieAdjustUpTemperature(self.hass, self.entity)
            yield AligenieAdjustDownTemperature(self.hass, self.entity)
        if supported & climate.SUPPORT_FAN_MODE:
            yield AligenieSetWindSpeed(self.hass, self.entity)
        if supported & climate.SUPPORT_TARGET_HUMIDITY:
            yield AligenieSetHumidity(self.hass, self.entity)
            yield AligenieAdjustUpHumidity(self.hass, self.entity)
            yield AligenieAdjustDownHumidity(self.hass, self.entity)

    def properties(self):
        """Yield the supported properties."""
        yield AligeniePowerState(self.hass, self.entity)

        supported = self.entity.attributes.get(ATTR_SUPPORTED_FEATURES, 0)
        if supported & climate.SUPPORT_TARGET_TEMPERATURE_RANGE:
            yield AligenieTemperature(self.hass, self.entity)
        if supported & climate.SUPPORT_FAN_MODE:
            yield AligenieWindspeed(self.hass, self.entity)
        if supported & climate.SUPPORT_TARGET_HUMIDITY:
            yield AligenieHumidity(self.hass, self.entity)


@ENTITY_ADAPTERS.register(fan.DOMAIN)
class AligenieFan(AligenieEntity):
    """Class to represent Fan in Aligenie term."""

    def operations(self):
        """Yield the supported operations."""
        yield AligenieTurnOn(self.hass, self.entity)
        yield AligenieTurnOff(self.hass, self.entity)

        supported = self.entity.attributes.get(ATTR_SUPPORTED_FEATURES, 0)
        if supported & fan.SUPPORT_SET_SPEED:
            yield AligenieSetWindSpeed(self.hass, self.entity)
        if supported & fan.SUPPORT_OSCILLATE:
            yield AligenieOpenSwing(self.hass, self.entity)
            yield AligenieCloseSwing(self.hass, self.entity)

    def properties(self):
        """Yield the supported properties."""
        yield AligeniePowerState(self.hass, self.entity)

        supported = self.entity.attributes.get(ATTR_SUPPORTED_FEATURES, 0)
        if supported & fan.SUPPORT_SET_SPEED:
            yield AligenieWindspeed(self.hass, self.entity)


@ENTITY_ADAPTERS.register(switch.DOMAIN)
class AligenieSwitch(AligenieEntity):
    """Class to represent Fan in Aligenie term."""

    def operations(self):
        """Yield the supported operations."""
        yield AligenieTurnOn(self.hass, self.entity)
        yield AligenieTurnOff(self.hass, self.entity)

    def properties(self):
        """Yield the supported properties."""
        yield AligeniePowerState(self.hass, self.entity)


@ENTITY_ADAPTERS.register(vacuum.DOMAIN)
class AligenieVacuum(AligenieEntity):
    """Class to represent Vacuum in Aligenie term."""

    def device_type(self):
        """Aligenie recoginzed type."""
        return "roboticvacuum"

    def operations(self):
        """Yield the supported operations."""
        yield AligenieTurnOn(self.hass, self.entity)
        yield AligenieTurnOff(self.hass, self.entity)

    def properties(self):
        """Yield the supported properties."""
        yield AligeniePowerState(self.hass, self.entity)


@ENTITY_ADAPTERS.register(media_player.DOMAIN)
class AligenieMediaPlayer(AligenieEntity):
    """Class to represent Television in Aligenie term."""

    def device_type(self):
        """Aligenie recoginzed type."""
        return "television"

    def operations(self):
        """Yield the supported operations."""
        yield AligenieTurnOn(self.hass, self.entity)
        yield AligenieTurnOff(self.hass, self.entity)

        supported = self.entity.attributes.get(ATTR_SUPPORTED_FEATURES, 0)
        if supported & media_player.SUPPORT_PLAY:
            yield AligeniePlay(self.hass, self.entity)
            yield AligeniePause(self.hass, self.entity)
            yield AligenieNext(self.hass, self.entity)
            yield AligeniePrevious(self.hass, self.entity)
        if supported & media_player.SUPPORT_VOLUME_STEP:
            yield AligenieAdjustUpVolume(self.hass, self.entity)
            yield AligenieAdjustDownVolume(self.hass, self.entity)

    def properties(self):
        """Yield the supported properties."""
        yield AligeniePowerState(self.hass, self.entity)
