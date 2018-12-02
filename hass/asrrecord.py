import logging
import time
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
                    dest=wave.open(wavfile, 'wb')
                    dest.setnchannels(1)
                    dest.setsampwidth(1)
                    dest.setframerate(10000)
                    dest.writeframes(_buffer[:20000])
                    dest.close()
                    _buffer=_buffer[20000:]
            
if __name__ == '__main__': 
    server = socketserver.ThreadingTCPServer(('hejie-ThinkPad-L450.local',8009),AsrServer)
    server.serve_forever()
