import logging
import time
import contextlib
import wave
import socketserver

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

class AsrServer(socketserver.BaseRequestHandler):

    def handle(self):
        _LOGGER.info('AsrServer handling*******************************')
        _buffer=b''
        while True:
            data=self.request.recv(20000)
            if data.strip():
                _buffer=_buffer+data
                _bufflen=len(_buffer)
                if _bufflen>=20000:
                    wavfile='asr%s.wav'%time.strftime('%Y%m%d%H%M%S', time.localtime())
                    _LOGGER.info(('AsrServer create file %s len %s*************************')%(wavfile, _bufflen))
                    with contextlib.closing(wave.open(wavfile, 'wb')) as wf
                        bytes16=audioop.lin2lin(_buffer[:20000], 1, 2)
                        bytes16k=audioop.ratecv(byte16, 2, 1, 10000, 16000, None)[0]
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(16000)
                        wf.writeframes(bytes16k)
                    _buffer=_buffer[20000:]
            
if __name__ == '__main__': 
    server = socketserver.ThreadingTCPServer(('hejie-ThinkPad-L450.local',8009),AsrServer)
    server.serve_forever()
