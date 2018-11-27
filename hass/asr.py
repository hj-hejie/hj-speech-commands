import logging
import time
import wave
import socketserver

from homeassistant.components.light import Light

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([Asr(hass)])

class AsrServer(socketserver.BaseRequestHandler):

    def handle(self):
        _LOGGER.info('AsrServer handling*******************************')
        while True:
            data=self.request.recv(20000)
            if data.decode().strip():
                _LOGGER.info('AsrServer create file*************************')
                dest=wave.open('asr'+time.strftime('%H%M%S', time.localtime())+'.wav', 'wb')
                dest.setnchannels(1)
                dest.setsampwidth(1)
                dest.setframerate(10000)
                dest.writeframes(data)
                dest.close()
            
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
        _LOGGER.info('asr turn on ***********************************************')
        self.hass.services.call('light', 'turn_on', {'entity_id': 'light.hejielight1'})
        self._state=True

    def turn_off(self, **kwargs):
        _LOGGER.info('asr trun off -----------------------------------------------')
        self.hass.services.call('light', 'turn_off', {'entity_id': 'light.hejielight1'})
        self._state=False

if __name__ == '__main__': 
    server = socketserver.ThreadingTCPServer(('hejie-ThinkPad-L450.local',8009),AsrServer)
    server.serve_forever()
