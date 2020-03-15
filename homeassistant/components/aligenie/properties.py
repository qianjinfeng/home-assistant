"""Aligenie capabilities."""
import logging

from homeassistant.components import climate, fan, light
from homeassistant.const import STATE_OFF, TEMP_CELSIUS
from homeassistant.util import temperature as temp_util

from .errors import UnsupportedProperty

_LOGGER = logging.getLogger(__name__)


class AligenieProperty:
    """Base class for Aligenie property."""

    def __init__(self, hass, entity):
        """Initialize an Aligenie property."""
        self.hass = hass
        self.entity = entity

    @staticmethod
    def property_supported():
        """Return what property this entity supports."""
        return {}

    @staticmethod
    def get_property(name):
        """Read value of this property."""
        raise UnsupportedProperty(name)

    def serialize_property(self):
        """Return property in a dict for an Query API response."""
        prop = self.property_supported()
        prop_name = prop["name"]
        # pylint: disable=assignment-from-no-return
        prop_value = self.get_property(prop_name)
        if prop_value is not None:
            result = {
                "name": prop_name,
                "value": prop_value,
            }

            return result


class AligeniePowerState(AligenieProperty):
    """Class for Aligenie PowerState."""

    def property_supported(self):
        """Return what property this entity supports."""
        return {"name": "powerstate"}

    def get_property(self, name):
        """Read and return a property."""
        if name != "powerstate":
            raise UnsupportedProperty(name)

        if self.entity.domain == climate.DOMAIN:
            is_on = self.entity.state != climate.HVAC_MODE_OFF

        else:
            is_on = self.entity.state != STATE_OFF

        return "on" if is_on else "off"


class AligenieBrightness(AligenieProperty):
    """Class for Aligenie Brightness."""

    def property_supported(self):
        """Return what property this entity supports."""
        return {"name": "brightness"}

    def get_property(self, name):
        """Read and return a property."""
        if name != "brightness":
            raise UnsupportedProperty(name)

        brightness = 0
        if "brightness" in self.entity.attributes:
            brightness = round(self.entity.attributes["brightness"] / 255.0 * 100)
        return str(brightness)


class AligenieColorTemperature(AligenieProperty):
    """Class for Aligenie ColorTemperature."""

    def property_supported(self):
        """Return what property this entity supports."""
        return {"name": "colortemperature"}

    def get_property(self, name):
        """Read and return a property."""
        if name != "colortemperature":
            raise UnsupportedProperty(name)

        color_temp = 0
        if light.ATTR_COLOR_TEMP in self.entity.attributes:
            color_temp = self.entity.attributes[light.ATTR_COLOR_TEMP]
        return str(color_temp)


class AligenieColor(AligenieProperty):
    """Class for Aligenie Color."""

    def property_supported(self):
        """Return what property this entity supports."""
        return {"name": "color"}

    def get_property(self, name):
        """Read and return a property."""
        if name != "color":
            raise UnsupportedProperty(name)

        color = self.entity.attributes.get(light.ATTR_COLOR_NAME)

        return color


class AligenieHumidity(AligenieProperty):
    """Class for Aligenie Humidity."""

    def property_supported(self):
        """Return what property this entity supports."""
        return {"name": "humidity"}

    def get_property(self, name):
        """Read and return a property."""
        if name != "humidity":
            raise UnsupportedProperty(name)

        humi = 0
        if self.entity.domain == climate.DOMAIN:
            humi = self.entity.attributes.get(climate.ATTR_CURRENT_HUMIDITY)

        return str(humi)


class AligenieTemperature(AligenieProperty):
    """Class for Aligenie Temperature."""

    def property_supported(self):
        """Return what property this entity supports."""
        return {"name": "temperature"}

    def get_property(self, name):
        """Read and return a property."""
        if name != "temperature":
            raise UnsupportedProperty(name)

        temp = 0
        unit = self.hass.config.units.temperature_unit
        if self.entity.domain == climate.DOMAIN:
            temp = self.entity.attributes.get(climate.ATTR_CURRENT_TEMPERATURE)
            if temp is not None:
                temp = round(temp_util.convert(temp, unit, TEMP_CELSIUS), 1)

        return str(temp)


class AligenieWindspeed(AligenieProperty):
    """Class for Aligenie Windspeed."""

    @staticmethod
    def ha_to_ali(mode):
        """Conversion to Fan speed number."""
        mode_dict = {
            "off": 0,
            "low": 1,
            "medium": 2,
            "high": 3,
        }
        return mode_dict[mode] if mode in mode_dict else 0

    def property_supported(self):
        """Return what property this entity supports."""
        return {"name": "windspeed"}

    def get_property(self, name):
        """Read and return a property."""
        if name != "windspeed":
            raise UnsupportedProperty(name)

        speed = 0
        if self.entity.domain == fan.DOMAIN:
            speed = AligenieWindspeed.ha_to_ali(
                self.entity.attributes.get(fan.ATTR_SPEED)
            )
        elif self.entity.domain == climate.DOMAIN:
            speed = AligenieWindspeed.ha_to_ali(
                self.entity.attributes.get(climate.ATTR_FAN_MODE)
            )

        return str(speed)
