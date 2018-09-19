import logging

from homeassistant.components.light import Light

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([HjLight()])

class HjLight(Light):

    def __init__(self):
        self._name = 'hejielight1'
        self._state = False
        self.ws = create_connection("ws://esp8266ip:8266/")
        _LOGGER.info(self.ws.recv())
	self.ws.send('username\n\r')
        _LOGGER.info(self.ws.recv())
	self.ws.send('password\n\r')
        _LOGGER.info(self.ws.recv())
        self.ws.send('from machine import Pin\n\r')
        self.ws.send('p0=Pin(0)\n\r')

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
	self.ws.send('p0.on()\n\r')
        self._state=True

    def turn_off(self, **kwargs):
        self.ws.send('p0.off()\n\r')
        self._state=False
