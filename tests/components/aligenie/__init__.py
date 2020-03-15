"""Tests for the Aligenie integration."""
from uuid import uuid4

from homeassistant.components.aligenie import home_skill
from homeassistant.core import Context

from tests.common import async_mock_service


def get_new_request(namespace, name, device=None):
    """Generate a new API message."""
    raw_msg = {
        "header": {
            "namespace": namespace,
            "name": name,
            "messageId": str(uuid4()),
            "payloadVersion": 1,
        },
        "payload": {
            "accessToken": "access token",
            "deviceId": device,
            "deviceType": "XXX",
            "extensions": {"extension1": "", "extension2": ""},
        },
    }

    return raw_msg


def get_new_discovery_request(namespace, name):
    """Generate a new API message."""
    raw_msg = {
        "header": {
            "namespace": namespace,
            "name": name,
            "messageId": str(uuid4()),
            "payloadVersion": 1,
        },
        "payload": {"accessToken": "access token"},
    }

    return raw_msg


def assert_devices_actions(appliance, *actions):
    """Assert the operations supports the given interfaces."""
    supported = set(appliance["actions"])
    assert supported == set(actions)


async def discovery_test(device, hass, expected_devices=1):
    """Test alexa discovery request."""
    request = get_new_discovery_request(
        "AliGenie.Iot.Device.Discovery", "DiscoveryDevices"
    )

    hass.states.async_set(*device)

    msg = await home_skill.async_handle_message(hass, {}, request)

    assert msg["header"]["name"] == "DiscoveryDevicesResponse"
    assert msg["header"]["namespace"] == "AliGenie.Iot.Device.Discovery"
    devices = msg["payload"]["devices"]
    assert len(devices) == expected_devices

    if expected_devices == 1:
        return devices[0]
    if expected_devices > 1:
        return devices
    return None


async def assert_request_calls_service(
    namespace,
    name,
    device,
    service,
    hass,
    attribute=None,
    value=None,
    output_attr=None,
    output_value=None,
):
    """Assert an API request calls a hass service."""
    context = Context()
    request = get_new_request(namespace, name, device)
    if attribute:
        request["payload"]["attribute"] = attribute
    if value:
        request["payload"]["value"] = value

    domain, service_name = service.split(".")
    calls = async_mock_service(hass, domain, service_name)

    msg = await home_skill.async_handle_message(hass, {}, request, context)
    await hass.async_block_till_done()

    assert len(calls) == 1
    call = calls[0]
    assert call.data["entity_id"] == device
    if output_attr is not None:
        assert call.data[output_attr] == output_value
    assert msg["header"]["name"] == name + "Response"
    assert call.context == context

    return call, msg


async def assert_property(hass, device, query, prop_name, prop_value):
    """Use ReportState to get properties and return them.

    The result is a ReportedProperties instance, which has methods to make
    assertions about the properties.
    """
    request = get_new_request("AliGenie.Iot.Device.Query", query, device)
    msg = await home_skill.async_handle_message(hass, {}, request)
    await hass.async_block_till_done()

    assert len(msg["properties"]) == 1
    prop = msg["properties"][0]
    assert prop["name"] == prop_name
    assert prop["value"] == prop_value
