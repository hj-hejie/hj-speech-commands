import pdb
import logging
import time
import socketserver
import hjvad
import hjlog

LOG = logging.getLogger(__name__)

class AsrServer(socketserver.BaseRequestHandler):

    def handle(self):
        LOG.debug('AsrServer handling*******************************')
        buffer = b''
        n_recv = 20000
        while True:
            data=self.request.recv(n_recv)
            LOG.debug('asr server recv %s' % len(data))
            if data.strip():
                buffer = buffer+data
                while len(buffer) >= n_recv:
                    #wavfile='silence/%s.wav'%time.strftime('%Y%m%d%H%M%S', time.localtime())
                    wavfile='chunk01.wav'
                    LOG.debug('AsrServer create file %s len %s*************************'%(wavfile, len(buffer)))
                    hjvad.write_wave(wavfile, buffer[ : n_recv])
                    buffer = buffer[n_recv : ]
            
if __name__ == '__main__': 
    server = socketserver.ThreadingTCPServer(('hejie-ThinkPad-L450.local',8009),AsrServer)
    server.serve_forever()
