import logging
import time
import collections
import socketserver
import webrtcvad
import audioop

from homeassistant.components.light import Light

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([Asr(hass)])

class Frame(object):
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration

class AsrServer(socketserver.BaseRequestHandler):

    def handle(self):
        _LOGGER.info('AsrServer handling*******************************')
        vad = webrtcvad.Vad(3)
        frames = frame_generator(30, 16000)
        segments = vad_collector(16000, 30, 300, vad, frames)
        for i, segment in enumerate(segments):
            print('--end')

    def frame_generator(frame_duration_ms, sample_rate):
        n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
        offset = 0
        timestamp = 0.0
        duration = (float(n) / sample_rate) / 2.0
        #buffer=b''
        while True:
            bytes=self.request.recv(n/2)
            if bytes.strip():
                bytes16=audioop.lin2lin(bytes, 1, 2)
                bytes16k=audioop.ratecv(byte16, 2, 1, 10000, 16000, None)[0]
                #buffer+=data
                #if len(_buffer)>=n:
                yield Frame(byte16k, timestamp, duration)
                #buffer=buffer[n:]
                timestamp += duration
                offset += n

    def vad_collector(sample_rate, frame_duration_ms,
                  padding_duration_ms, vad, frames):
        num_padding_frames = int(padding_duration_ms / frame_duration_ms)
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        triggered = False
        voiced_frames = []
        for i, frame in enumerate(frames):
            print(
                '1' if vad.is_speech(frame.bytes, sample_rate) else '0')
            if not triggered:
                ring_buffer.append(frame)
                num_voiced = len([f for f in ring_buffer
                                  if vad.is_speech(f.bytes, sample_rate)])
                if num_voiced > 0.9 * ring_buffer.maxlen:
                    print('+(%s)' % (ring_buffer[0].timestamp,))
                    triggered = True
                    voiced_frames.extend(ring_buffer)
                    ring_buffer.clear()
            else:
                voiced_frames.append(frame)
                ring_buffer.append(frame)
                num_unvoiced = len([f for f in ring_buffer
                                    if not vad.is_speech(f.bytes, sample_rate)])
                if num_unvoiced > 0.9 * ring_buffer.maxlen:
                    print('-(%s)' % (frame.timestamp + frame.duration))
                    triggered = False
                    yield b''.join([f.bytes for f in voiced_frames])
                    ring_buffer.clear()
                    voiced_frames = []
        if triggered:
            print('-(%s)' % (frame.timestamp + frame.duration))
        print('\n')
        if voiced_frames:
            yield b''.join([f.bytes for f in voiced_frames])
            
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
