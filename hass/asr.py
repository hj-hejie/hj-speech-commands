import logging

from homeassistant.components.light import Light

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([Asr(hass)])

class Asr(Light):

    def __init__(self, hass):
        self._name = 'hejieasr'
        self._state = False
        self.hass=hass

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        print('asr turn on ***********************************************')
        self.hass.services.call('light', 'turn_on', {'entity_id': 'light.hejielight1'})
        self._state=True

    def turn_off(self, **kwargs):
        print('asr trun off -----------------------------------------------')
        self.hass.services.call('light', 'turn_off', {'entity_id': 'light.hejielight1'})
        self._state=False
