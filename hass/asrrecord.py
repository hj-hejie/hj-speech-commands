import logging
import time
import contextlib
import wave
import socketserver
import audioop

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

class AsrServer(socketserver.BaseRequestHandler):

    def handle(self):
        _LOGGER.info('AsrServer handling*******************************')
        _buffer=b''
        sample_rate=10000
        sample_width=1
        target_rate=10000
        target_width=1
        _len=sample_rate*2
        while True:
            data=self.request.recv(_len)
            if data.strip():
                _buffer=_buffer+data
                _bufflen=len(_buffer)
                if _bufflen>=_len:
                    wavfile='silence/%s.wav'%time.strftime('%Y%m%d%H%M%S', time.localtime())
                    _LOGGER.info(('AsrServer create file %s len %s*************************')%(wavfile, _bufflen))
                    with contextlib.closing(wave.open(wavfile, 'wb')) as wf:
                        #bytes16=audioop.lin2lin(_buffer[:_len], sample_width, target_width)
                        #bytes16k=audioop.ratecv(bytes16, target_width, 1, sample_rate, target_rate, None)[0]
                        wf.setnchannels(1)
                        wf.setsampwidth(target_width)
                        wf.setframerate(target_rate)
                        wf.writeframes(_buffer[:_len])
                    _buffer=_buffer[_len:]
            
if __name__ == '__main__': 
    server = socketserver.ThreadingTCPServer(('hejie-ThinkPad-L450.local',8009),AsrServer)
    server.serve_forever()
