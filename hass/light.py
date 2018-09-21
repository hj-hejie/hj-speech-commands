import logging

from websocket import create_connection
from homeassistant.components.light import Light

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([HjLight()])

class HjLight(Light):

    def __init__(self):
        self._name = 'hejielight1'
        self._state = False
        self.ws = create_connection("ws://192.168.0.120:8266/")
        _LOGGER.info(self.ws.recv())
        self.ws.send('passw0rd\r\n')
        _LOGGER.info(self.ws.recv())
        self.ws.send('from machine import Pin\r\n')
        self.ws.send('p0=Pin(0, Pin.OUT)\r\n')
        _LOGGER.info('light inited +++++++++++++++++++++++++++++++++++++++++++')

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        _LOGGER.info('light turn on ***************************************')
        self.ws.send('p0.off()\r\n')
        self._state=True

    def turn_off(self, **kwargs):
        _LOGGER.info('light turn off---------------------------------------')
        self.ws.send('p0.on()\r\n')
        self._state=False

    def __del__(self):
        self.ws.close()
        _LOGGER.info('light deled +++++++++++++++++++++++++++++++++++++++++')
