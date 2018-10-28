import logging
import socketserver

from homeassistant.components.light import Light

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([Asr(hass)])

class AsrServer(socketserver.BaseRequestHandler):

    def handle(self):
        _LOGGER.info('AsrServer handling*******************************')
        self.request.sendall(b'hejieserver')
        while True:
            data=self.request.recv(1)
            if data.decode().strip():
                print('hejieserver:'+data.decode())

class Asr(Light):

    def __init__(self, hass):
        self._name = 'hejieasr'
        self._state = False
        self.hass=hass
        server = socketserver.ThreadingTCPServer(('192.168.1.4',8009),AsrServer)
        server.serve_forever()

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

if __name__ == '__main__': 
    server = socketserver.ThreadingTCPServer(('192.168.1.4',8009),AsrServer)
    server.serve_forever()