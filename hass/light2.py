import logging
import requests
from homeassistant.components.light import Light

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([HjLight()])

class HjLight(Light):

    def __init__(self):
        self._name = 'hejielight1'
        self._state = False
        _LOGGER.info('light inited +++++++++++++++++++++++++++++++++++++++++++')

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        _LOGGER.info('light turn on ***************************************')
        _LOGGER.info(requests.get('http://esp8266light.local/on'))
        self._state=True

    def turn_off(self, **kwargs):
        _LOGGER.info('light turn off---------------------------------------')
        _LOGGER.info(requests.get('http://esp8266light.local/off'))
        self._state=False
