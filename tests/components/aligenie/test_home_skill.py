"""Test Home Skill HTTP endpoints."""
import json

from homeassistant.components.aligenie import DOMAIN, home_skill
from homeassistant.setup import async_setup_component

from . import get_new_discovery_request, get_new_request

from tests.common import async_mock_service


async def test_http_api_discovery(hass, hass_client):
    """Discovery."""
    hass.states.async_set(
        "light.test",
        "off",
        {"friendly_name": "Test light", "supported_features": 1, "brightness": 77},
    )
    hass.states.async_set("climate.cool", "cool")
    hass.states.async_set("fan.fan1", "on")

    await async_setup_component(
        hass,
        DOMAIN,
        {"aligenie": {"home_skill": {"filter": {"exclude_entities": ["fan.fan1"]}}}},
    )

    http_client = await hass_client()
    request = get_new_discovery_request(
        "AliGenie.Iot.Device.Discovery", "DiscoveryDevices"
    )
    response = await http_client.post(
        home_skill.HOME_SKILL_HTTP_ENDPOINT,
        data=json.dumps(request),
        headers={"content-type": "application/json"},
    )
    response_data = await response.json()

    assert response_data["header"]["name"] == "DiscoveryDevicesResponse"
    assert len(response_data["payload"]["devices"]) == 2


async def test_http_api_control(hass, hass_client):
    """Test Control."""
    hass.states.async_set(
        "light.test",
        "off",
        {"friendly_name": "Test light", "supported_features": 1, "brightness": 77},
    )
    call_light = async_mock_service(hass, "light", "turn_on")

    await async_setup_component(hass, DOMAIN, {"aligenie": {"home_skill": None}})

    http_client = await hass_client()
    request = get_new_request("AliGenie.Iot.Device.Control", "TurnOn", "light.test")
    response = await http_client.post(
        home_skill.HOME_SKILL_HTTP_ENDPOINT,
        data=json.dumps(request),
        headers={"content-type": "application/json"},
    )
    response_data = await response.json()

    assert len(call_light) == 1
    assert response_data["header"]["name"] == "TurnOnResponse"


async def test_http_api_query(hass, hass_client):
    """Test Query."""
    hass.states.async_set(
        "light.test",
        "off",
        {"friendly_name": "Test light", "supported_features": 1, "brightness": 77},
    )

    await async_setup_component(hass, DOMAIN, {"aligenie": {"home_skill": None}})

    http_client = await hass_client()
    request = get_new_request("AliGenie.Iot.Device.Query", "Query", "light.test")
    response = await http_client.post(
        home_skill.HOME_SKILL_HTTP_ENDPOINT,
        data=json.dumps(request),
        headers={"content-type": "application/json"},
    )
    response_data = await response.json()

    assert response_data["header"]["name"] == "QueryResponse"
    assert len(response_data["properties"]) == 2
