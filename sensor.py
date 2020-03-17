"""
Tracks prices of an item from amazon
Custom_component by Dion de Kleijn
https://github.com/diondk
Completly base on the custom component from @Reua
made it working on the latest release of HA and will try to update it with new features.
"""
import logging
import voluptuous as vol
from datetime import timedelta
from homeassistant.util import Throttle

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
import homeassistant.util.dt as dt_util
from homeassistant.const import (CONF_NAME)
REQUIREMENTS = ['lxml==4.1.1','requests==3.0']

_LOGGER = logging.getLogger(__name__)

CONF_ITEMS = 'items'
CONF_ASIN = "asin"
CONF_SITE = 'site'

ICON = 'mdi:amazon'

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=2*60*60)

_ITEM_SCHEMA = vol.All(
    vol.Schema({
        vol.Required(CONF_ASIN): cv.string,
        vol.Optional(CONF_SITE): cv.string,
        vol.Optional(CONF_NAME): cv.string
    })
)

_ITEMS_SCHEMA = vol.Schema([_ITEM_SCHEMA])

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ITEMS): _ITEMS_SCHEMA,
    vol.Required(CONF_SITE): cv.string
    })
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Initiate the Amazon Price Sensor/s."""
    domain = config.get(CONF_SITE)
    items = config.get(CONF_ITEMS)
    language = config.get(CONF_SITE)
    sensors = []

    for item in items:
        try:
            sensors.append(AmazonPriceSensor(item, domain))
        except ValueError as exc:
            _LOGGER.error(exc)

    add_devices(sensors, True)

class AmazonPriceSensor(Entity):
    """Implementation of a Amazon Price sensor."""

    def __init__(self, item, domain):
        """Get all the data stored for the sensor."""
        self._domain = domain
        self._name = item.get(CONF_NAME)
        self._updateitem = item

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name if self._name is not None else self._item[0]

    @property
    def icon(self):
        """Return the icon for the frontend."""
        return ICON

    @property
    def state(self):
        """Return the sale price of the item."""
        return self._item[1]
    
    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attrs = {'Name': self._item[0]}

        return attrs

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update all Data every 2h"""
        from lxml import html  
        import re
        import requests

        url = "https://www.amazon."+self._updateitem.get(CONF_SITE, self._domain)+"/dp/"+self._updateitem.get(CONF_ASIN)+"/"
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        page = requests.get(url,headers=headers)
        try:
            #Get all the data from Amazon webpage
            doc = html.fromstring(page.content)
            RAW_NAME = doc.xpath('//span[contains(@id,"productTitle") or contains(@id,"Title")]/text()')
            RAW_SALE_PRICE = doc.xpath('//span[contains(@id,"priceblock_ourprice") or contains(@id,"priceblock_ourprice")]/text()')


            #Parse everthing
            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_BPRC = ' '.join(''.join(RAW_SALE_PRICE).split()) if RAW_SALE_PRICE else None


            SALE_PRICE = SALE_BPRC

            if page.status_code!=200:
                raise ValueError('The requested item page returned: HTTP'+page.status_code+'please check asin and domain ending')

            #Write into variables
            self._item = [NAME, SALE_PRICE]

            if self._item is None:
                raise ValueError('asin or domain could not be resolved')

        except Exception as e:
            raise ValueError(e)