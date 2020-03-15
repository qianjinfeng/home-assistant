"""Test Home Skill Errors."""
import json

from homeassistant.components.aligenie import DOMAIN, home_skill
from homeassistant.setup import async_setup_component

from . import get_new_discovery_request, get_new_request


async def test_api_not_exist(hass, hass_client):
    """Test error response."""
    await async_setup_component(hass, DOMAIN, {"aligenie": {"home_skill": None}})

    http_client = await hass_client()
    request = get_new_discovery_request("AliGenie.Iot.Device.Discovery", "Discovery")

    response = await http_client.post(
        home_skill.HOME_SKILL_HTTP_ENDPOINT,
        data=json.dumps(request),
        headers={"content-type": "application/json"},
    )
    response_data = await response.json()

    assert response_data["header"]["name"] == "ErrorResponse"
    assert response_data["payload"]["errorCode"] == "INVALIDATE_CONTROL_ORDER"


async def test_entity_not_exist(hass, hass_client):
    """Test not entity."""
    await async_setup_component(hass, DOMAIN, {"aligenie": {"home_skill": None}})

    http_client = await hass_client()
    request = get_new_request(
        "AliGenie.Iot.Device.Query", "QueryBrightness", "light.test"
    )
    response = await http_client.post(
        home_skill.HOME_SKILL_HTTP_ENDPOINT,
        data=json.dumps(request),
        headers={"content-type": "application/json"},
    )
    response_data = await response.json()

    assert response_data["header"]["name"] == "ErrorResponse"
    assert response_data["payload"]["errorCode"] == "DEVICE_IS_NOT_EXIST"


async def test_opereation_not_exist(hass, hass_client):
    """Test not operation."""
    hass.states.async_set("climate.cool", "cool")

    await async_setup_component(hass, DOMAIN, {"aligenie": {"home_skill": None}})

    http_client = await hass_client()
    request = get_new_request(
        "AliGenie.Iot.Device.Control", "WronOperation", "climate.cool"
    )
    response = await http_client.post(
        home_skill.HOME_SKILL_HTTP_ENDPOINT,
        data=json.dumps(request),
        headers={"content-type": "application/json"},
    )
    response_data = await response.json()

    assert response_data["header"]["name"] == "ErrorResponse"
    assert response_data["payload"]["errorCode"] == "DEVICE_NOT_SUPPORT_FUNCTION"


async def test_property_not_exist(hass, hass_client):
    """Test not property."""
    hass.states.async_set("climate.cool", "cool")

    await async_setup_component(hass, DOMAIN, {"aligenie": {"home_skill": None}})

    http_client = await hass_client()
    request = get_new_request(
        "AliGenie.Iot.Device.Query", "wrongproperty", "climate.cool"
    )
    response = await http_client.post(
        home_skill.HOME_SKILL_HTTP_ENDPOINT,
        data=json.dumps(request),
        headers={"content-type": "application/json"},
    )
    response_data = await response.json()

    assert response_data["header"]["name"] == "ErrorResponse"
    assert response_data["payload"]["errorCode"] == "DEVICE_NOT_SUPPORT_FUNCTION"
