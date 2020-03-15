"""Alexa message handlers."""
import logging

from homeassistant.util.decorator import Registry

from .entities import ENTITY_ADAPTERS, async_get_entities

_LOGGER = logging.getLogger(__name__)
HANDLERS = Registry()


@HANDLERS.register(("AliGenie.Iot.Device.Discovery", "DiscoveryDevices"))
async def async_api_discovery(hass, config, directive, context):
    """Process discovery request."""
    discovery_devices = []
    for aligenie_entity in async_get_entities(hass, config):
        discovery_devices.append(aligenie_entity.serialize_discovery())

    return directive.response(payload={"devices": discovery_devices},)


@HANDLERS.register(("AliGenie.Iot.Device.Control"))
async def async_api_control(hass, config, directive, context):
    """Process a control request."""
    entity = directive.entity
    aligenie_entity = ENTITY_ADAPTERS[entity.domain](hass, config, entity)

    operation = aligenie_entity.get_operation(directive.name)
    await operation.execute(directive.payload, context)

    response = directive.response()

    return response


@HANDLERS.register(("AliGenie.Iot.Device.Query", "Query"))
async def async_api_query(hass, config, directive, context):
    """Process a Query request."""
    entity = directive.entity

    response = directive.response()

    aligenie_entity = ENTITY_ADAPTERS[entity.domain](hass, config, entity)

    response.merge_properties(list(aligenie_entity.serialize_properties()))

    return response


@HANDLERS.register(("AliGenie.Iot.Device.Query"))
async def async_api_query_attribute(hass, config, directive, context):
    """Process a Specific Query request."""
    entity = directive.entity

    response = directive.response()

    aligenie_entity = ENTITY_ADAPTERS[entity.domain](hass, config, entity)

    operation_name = directive.name
    prop_name = operation_name[5:].lower()
    prop = aligenie_entity.serialize_property(prop_name)

    response.merge_property(prop)

    return response
