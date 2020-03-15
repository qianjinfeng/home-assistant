"""Test Home Skill Entities."""
from . import (
    assert_devices_actions,
    assert_property,
    assert_request_calls_service,
    discovery_test,
)


async def test_switch(hass):
    """Test switch."""
    device = ("switch.test", "on", {"friendly_name": "Test switch"})
    appliance = await discovery_test(device, hass)

    assert appliance["deviceId"] == "switch.test"
    assert appliance["deviceName"] == "Test switch"
    assert_devices_actions(appliance, "TurnOn", "TurnOff")

    await assert_request_calls_service(
        "AliGenie.Iot.Device.Control", "TurnOn", "switch.test", "switch.turn_on", hass
    )

    await assert_property(hass, "switch.test", "QueryPowerstate", "powerstate", "on")


async def test_light(hass):
    """Test light."""
    device = (
        "light.test",
        "off",
        {
            "friendly_name": "Test light",
            "supported_features": 19,
            "brightness": 127.5,
            "color_name": "red",
            "color_temp": 27,
        },
    )

    appliance = await discovery_test(device, hass)
    assert appliance["deviceId"] == "light.test"
    assert appliance["deviceName"] == "Test light"
    assert_devices_actions(
        appliance,
        "TurnOn",
        "TurnOff",
        "SetBrightness",
        "AdjustUpBrightness",
        "AdjustDownBrightness",
        "SetColorTemperature",
        "AdjustUpColorTemperature",
        "AdjustDownColorTemperature",
        "SetColor",
    )

    await assert_property(hass, "light.test", "QueryPowerstate", "powerstate", "off")
    await assert_property(hass, "light.test", "QueryBrightness", "brightness", "50")
    await assert_property(
        hass, "light.test", "QueryColorTemperature", "colortemperature", "27"
    )
    await assert_property(hass, "light.test", "QueryColor", "color", "red")

    await assert_request_calls_service(
        "AliGenie.Iot.Device.Control",
        "AdjustUpBrightness",
        "light.test",
        "light.turn_on",
        hass,
        "brightnessStep",
        "5",
        "brightness_pct",
        55.0,
    )

    await assert_request_calls_service(
        "AliGenie.Iot.Device.Control",
        "AdjustDownBrightness",
        "light.test",
        "light.turn_on",
        hass,
        "brightnessStep",
        "5",
        "brightness_pct",
        45.0,
    )

    await assert_request_calls_service(
        "AliGenie.Iot.Device.Control",
        "SetBrightness",
        "light.test",
        "light.turn_on",
        hass,
        "brightness",
        "50",
        "brightness_pct",
        50,
    )

    await assert_request_calls_service(
        "AliGenie.Iot.Device.Control",
        "SetBrightness",
        "light.test",
        "light.turn_on",
        hass,
        "brightness",
        "max",
        "brightness_pct",
        100,
    )

    await assert_request_calls_service(
        "AliGenie.Iot.Device.Control",
        "SetBrightness",
        "light.test",
        "light.turn_on",
        hass,
        "brightness",
        "min",
        "brightness_pct",
        1,
    )

    await assert_request_calls_service(
        "AliGenie.Iot.Device.Control",
        "AdjustUpColorTemperature",
        "light.test",
        "light.turn_on",
        hass,
        "colorTemperatureStep",
        "5",
        "color_temp",
        32,
    )

    await assert_request_calls_service(
        "AliGenie.Iot.Device.Control",
        "AdjustDownColorTemperature",
        "light.test",
        "light.turn_on",
        hass,
        "colorTemperatureStep",
        "5",
        "color_temp",
        22,
    )

    await assert_request_calls_service(
        "AliGenie.Iot.Device.Control",
        "SetColorTemperature",
        "light.test",
        "light.turn_on",
        hass,
        "colorTemperature",
        "45",
        "color_temp",
        45,
    )

    await assert_request_calls_service(
        "AliGenie.Iot.Device.Control",
        "SetColor",
        "light.test",
        "light.turn_on",
        hass,
        "color",
        "green",
        "color_name",
        "green",
    )


async def test_climate(hass):
    """Test Climate."""
    device = (
        "climate.test",
        "auto",
        {
            "friendly_name": "Climate Room",
            "supported_features": 91,
            "current_temperature": 34,
            "unit_of_measurement": "°C",
        },
    )
    appliance = await discovery_test(device, hass)
    assert appliance["deviceId"] == "climate.test"
    assert appliance["deviceName"] == "Climate Room"
