"""Aligenie capabilities."""
import logging

from homeassistant.components import climate, fan, light, media_player, vacuum
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_SUPPORTED_FEATURES,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
)

from .const import ALI_THERMOSTAT_MODES
from .errors import AligenieUnsupportedFunctionError

_LOGGER = logging.getLogger(__name__)


class AligenieOperation:
    """Base class for Aligenie capability interfaces."""

    def __init__(self, hass, entity):
        """Initialize an Aligenie capability."""
        self.hass = hass
        self.entity = entity

    def name(self):
        """Return the Aligenie API name of this interface."""
        raise NotImplementedError

    async def execute(self, payload, context):
        """Execute such operation."""
        raise NotImplementedError


class AligenieTurnOn(AligenieOperation):
    """Implements TurnOn."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "TurnOn"

    async def execute(self, payload, context):
        """Execute such operation."""
        domain = self.entity.domain
        service = SERVICE_TURN_ON
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == media_player.DOMAIN:
            supported = self.entity.attributes.get(ATTR_SUPPORTED_FEATURES, 0)
            power_features = (
                media_player.SUPPORT_TURN_ON | media_player.SUPPORT_TURN_OFF
            )
            if not supported & power_features:
                service = media_player.SERVICE_MEDIA_PLAY
        elif domain == vacuum.DOMAIN:
            service = vacuum.SERVICE_START

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieTurnOff(AligenieOperation):
    """Implements TurnOff."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "TurnOff"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_OFF
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == media_player.DOMAIN:
            supported = self.entity.attributes.get(ATTR_SUPPORTED_FEATURES, 0)
            power_features = (
                media_player.SUPPORT_TURN_ON | media_player.SUPPORT_TURN_OFF
            )
            if not supported & power_features:
                service = media_player.SERVICE_MEDIA_STOP
        elif domain == vacuum.DOMAIN:
            service = vacuum.SERVICE_RETURN_TO_BASE

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieSelectChannel(AligenieOperation):
    """Implements SelectChannel."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "SelectChannel"

    async def execute(self, payload, context):
        """Execute such operation."""
        raise AligenieUnsupportedFunctionError()


class AligeniePlay(AligenieOperation):
    """Implements Play."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "Play"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_OFF
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == media_player.DOMAIN:
            service = media_player.SERVICE_MEDIA_PLAY

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligeniePause(AligenieOperation):
    """Implements Pause."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "Pause"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_OFF
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == media_player.DOMAIN:
            service = media_player.SERVICE_MEDIA_PLAY_PAUSE

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieNext(AligenieOperation):
    """Implements Next."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "Next"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_OFF
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == media_player.DOMAIN:
            service = media_player.SERVICE_MEDIA_NEXT_TRACK

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligeniePrevious(AligenieOperation):
    """Implements Previous."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "Previous"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_OFF
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == media_player.DOMAIN:
            service = media_player.SERVICE_MEDIA_PREVIOUS_TRACK

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieAdjustUpVolume(AligenieOperation):
    """Implements AdjustUpVolume."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "AdjustUpVolume"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_OFF
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == media_player.DOMAIN:
            service = media_player.SERVICE_VOLUME_UP

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieAdjustDownVolume(AligenieOperation):
    """Implements AdjustDownVolume."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "AdjustDownVolume"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_OFF
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == media_player.DOMAIN:
            service = media_player.SERVICE_VOLUME_DOWN

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieSetBrightness(AligenieOperation):
    """Implements SetBrightness."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "SetBrightness"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == light.DOMAIN:
            brightness = payload["value"]
            if brightness == "max":
                data.update({"brightness_pct": 100})
            elif brightness == "min":
                data.update({"brightness_pct": 1})
            else:
                data.update({"brightness_pct": int(brightness)})

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieAdjustUpBrightness(AligenieOperation):
    """Implements AdjustUpColorTemperature."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "AdjustUpBrightness"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == light.DOMAIN:
            brightness = self.entity.attributes["brightness"] * 100 / 255
            data.update(
                {"brightness_pct": min(brightness + int(payload["value"]), 100)}
            )

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieAdjustDownBrightness(AligenieOperation):
    """Implements AdjustDownBrightness."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "AdjustDownBrightness"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == light.DOMAIN:
            brightness = self.entity.attributes["brightness"] * 100 / 255
            data.update({"brightness_pct": max(brightness - int(payload["value"]), 0)})

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieSetColorTemperature(AligenieOperation):
    """Implements SetColorTemperature."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "SetColorTemperature"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == light.DOMAIN:
            data.update({light.ATTR_COLOR_TEMP: int(payload["value"])})

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieAdjustUpColorTemperature(AligenieOperation):
    """Implements AdjustUpColorTemperature."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "AdjustUpColorTemperature"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == light.DOMAIN:
            color_temp = self.entity.attributes[light.ATTR_COLOR_TEMP]
            data.update({light.ATTR_COLOR_TEMP: color_temp + int(payload["value"])})

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieAdjustDownColorTemperature(AligenieOperation):
    """Implements AdjustDownColorTemperature."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "AdjustDownColorTemperature"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == light.DOMAIN:
            color_temp = self.entity.attributes[light.ATTR_COLOR_TEMP]
            data.update(
                {light.ATTR_COLOR_TEMP: max(color_temp - int(payload["value"]), 1)}
            )

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieSetColor(AligenieOperation):
    """Implements SetColor."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "SetColor"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == light.DOMAIN:
            data.update({"color_name": payload["value"]})

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieAdjustUpHumidity(AligenieOperation):
    """Implements AdjustUpHumidity."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "AdjustUpHumidity"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == climate.DOMAIN:
            service = climate.SERVICE_SET_HUMIDITY
            humidity = self.entity.attributes[climate.ATTR_HUMIDITY]
            max_humi = self.entity.attributes[climate.ATTR_MAX_HUMIDITY]
            data.update(
                {climate.ATTR_HUMIDITY: min(humidity + int(payload["value"]), max_humi)}
            )

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieAdjustDownHumidity(AligenieOperation):
    """Implements AdjustDownHumidity."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "AdjustDownHumidity"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == climate.DOMAIN:
            service = climate.SERVICE_SET_HUMIDITY
            humidity = self.entity.attributes[climate.ATTR_HUMIDITY]
            min_humi = self.entity.attributes[climate.ATTR_MIN_HUMIDITY]
            data.update(
                {climate.ATTR_HUMIDITY: min(humidity - int(payload["value"]), min_humi)}
            )

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieSetHumidity(AligenieOperation):
    """Implements SetHumidity."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "SetHumidity"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == climate.DOMAIN:
            service = climate.SERVICE_SET_HUMIDITY
            humi = payload["value"]
            if humi == "max":
                data.update({climate.ATTR_HUMIDITY: climate.DEFAULT_MAX_HUMIDITY})
            elif humi == "min":
                data.update({climate.ATTR_HUMIDITY: climate.DEFAULT_MIN_HUMIDITY})
            else:
                data.update({climate.ATTR_HUMIDITY: int(humi)})

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieAdjustUpTemperature(AligenieOperation):
    """Implements AdjustUpTemperature."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "AdjustUpTemperature"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == climate.DOMAIN:
            service = climate.SERVICE_SET_TEMPERATURE
            temperature = self.entity.attributes[climate.ATTR_TEMPERATURE]
            max_temp = self.entity.attributes[climate.ATTR_MAX_TEMP]
            data.update(
                {
                    climate.ATTR_TEMPERATURE: min(
                        temperature + int(payload["value"]), max_temp
                    )
                }
            )

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieAdjustDownTemperature(AligenieOperation):
    """Implements AdjustDownTemperature."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "AdjustDownTemperature"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == climate.DOMAIN:
            service = climate.SERVICE_SET_TEMPERATURE
            temperature = self.entity.attributes[climate.ATTR_TEMPERATURE]
            min_temp = self.entity.attributes[climate.ATTR_MIN_TEMP]
            data.update(
                {
                    climate.ATTR_TEMPERATURE: min(
                        temperature - int(payload["value"]), min_temp
                    )
                }
            )

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieSetTemperature(AligenieOperation):
    """Implements SetTemperature."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "SetTemperature"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == climate.DOMAIN:
            service = climate.SERVICE_SET_TEMPERATURE
            temp = payload["value"]
            if temp == "max":
                data.update({climate.ATTR_TEMPERATURE: climate.DEFAULT_MAX_TEMP})
            elif temp == "min":
                data.update({climate.ATTR_TEMPERATURE: climate.DEFAULT_MIN_TEMP})
            else:
                data.update({climate.ATTR_TEMPERATURE: int(temp)})

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieSetMode(AligenieOperation):
    """Implements SetMode."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "SetMode"

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == climate.DOMAIN:
            mode = payload["value"]
            if mode in ALI_THERMOSTAT_MODES:
                service = climate.SERVICE_SET_HVAC_MODE
                data[climate.ATTR_HVAC_MODE] = mode
            else:
                raise AligenieUnsupportedFunctionError()

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieSetWindSpeed(AligenieOperation):
    """Implements SetWindSpeed."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "SetWindSpeed"

    @staticmethod
    def ali_to_ha(mode):
        """Conversion to Fan speed term."""
        mode_list = ["off", "low", "medium", "high"]
        return mode_list[mode]

    async def execute(self, payload, context):
        """Execute such operation."""
        service = SERVICE_TURN_ON
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == climate.DOMAIN:
            service = climate.SERVICE_SET_FAN_MODE
            data.update({"fan_mode": payload["value"]})
        elif domain == fan.DOMAIN:
            service = fan.SERVICE_SET_SPEED
            data.update(
                {"speed": AligenieSetWindSpeed.ali_to_ha(int(payload["value"]))}
            )

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieOpenSwing(AligenieOperation):
    """Implements OpenSwing."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "OpenSwing"

    async def execute(self, payload, context):
        """Execute such operation."""
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == fan.DOMAIN:
            service = fan.SERVICE_OSCILLATE
            data.update({"oscillating": "True"})

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )


class AligenieCloseSwing(AligenieOperation):
    """Implements CloseSwing."""

    def name(self):
        """Return the Aligenie API name of this operation."""
        return "CloseSwing"

    async def execute(self, payload, context):
        """Execute such operation."""
        domain = self.entity.domain
        data = {ATTR_ENTITY_ID: self.entity.entity_id}

        if domain == fan.DOMAIN:
            service = fan.SERVICE_OSCILLATE
            data.update({"oscillating": "False"})

        await self.hass.services.async_call(
            domain, service, data, blocking=False, context=context
        )
