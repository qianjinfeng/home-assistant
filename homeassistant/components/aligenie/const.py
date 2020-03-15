"""Aligenie Constants."""
from homeassistant.components.climate import const as climate

DOMAIN = "aligenie"
CONF_ENDPOINT = "endpoint"
CONF_BAICHUANKEY = "baichuan_key"
CONF_BAICHUANSECRET = "baichuan_secret"
CONF_SKILLID = "skill_id"
CONF_FILTER = "filter"
CONF_ENTITY_CONFIG = "entity_config"
API_HEADER = "header"
API_MESSAGEID = "messageId"
API_PAYLOAD = "payload"
API_DEVICE = "deviceId"

ALI_THERMOSTAT_MODES = {
    "heat": climate.HVAC_MODE_HEAT,
    "cool": climate.HVAC_MODE_COOL,
    "auto": climate.HVAC_MODE_AUTO,
    "off": climate.HVAC_MODE_OFF,
    "dehumidification": climate.HVAC_MODE_DRY,
    "airsupply": climate.HVAC_MODE_FAN_ONLY,
}


ALIGENIE_DEVICE_TYPES = [
    "television",  #: '电视',
    "light",  #: '灯',
    "aircondition",  #: '空调',
    "airpurifier",  #: '空气净化器',
    "outlet",  #: '插座',
    "switch",  #: '开关',
    "roboticvacuum",  #: '扫地机器人',
    "curtain",  #: '窗帘',
    "humidifier",  #: '加湿器',
    "fan",  #: '风扇',
    "bottlewarmer",  #: '暖奶器',
    "soymilkmaker",  #: '豆浆机',
    "kettle",  #: '电热水壶',
    "watercooler",  #: '饮水机',
    "cooker",  #: '电饭煲',
    "waterheater",  #: '热水器',
    "oven",  #: '烤箱',
    "waterpurifier",  #: '净水器',
    "fridge",  #: '冰箱',
    "STB",  #: '机顶盒',
    "sensor",  #: '传感器',
    "washmachine",  #: '洗衣机',
    "smartbed",  #: '智能床',
    "aromamachine",  #: '香薰机',
    "window",  #: '窗',
    "kitchenventilator",  #: '抽油烟机',
    "fingerprintlock",  #: '指纹锁'
    "telecontroller",  #: '万能遥控器'
    "dishwasher",  #: '洗碗机'
    "dehumidifier",  #: '除湿机'
]

INCLUDE_DOMAINS = {
    "climate": "aircondition",
    "fan": "fan",
    "light": "light",
    "media_player": "television",
    "remote": "telecontroller",
    "switch": "switch",
    "vacuum": "roboticvacuum",
}
