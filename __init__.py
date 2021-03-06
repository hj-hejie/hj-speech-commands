import pdb
import logging
import os
import sys
import time
import multiprocessing
from multiprocessing import Process, Queue, Pool
import socketserver
from homeassistant.const import EVENT_HOMEASSISTANT_START
sys.path.append(os.getcwd())
import hjtorch
import hjvad
import hjlog

LOG = logging.getLogger(__name__)

DOMAIN = 'pytorchasr'

N_PROC = 30

async def async_setup(hass, config):
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, pytorchasrstart)
    return True

class AsrServer(socketserver.BaseRequestHandler):

    def handle(self):
        LOG.debug('AsrServer handling*******************************')
        global byte_queues
        buffer = b''
        l_queues = len(byte_queues)
        i_queues = 0
        dur_samples = int(hjvad.DEF_DURATION * hjvad.DEF_SAMPLE_RATE)
        while True:
            data=self.request.recv(dur_samples)
            #LOG.debug('socket recv data len %s' % len(data))
            if data.strip():
                buffer = buffer+data
                while len(buffer) >= dur_samples:
                    #LOG.debug('socket %s put msg' % i_queues)
                    byte_queues[i_queues].put(buffer[ : dur_samples])
                    i_queues = (i_queues + 1) % l_queues
                    buffer = buffer[dur_samples : ]

def asrserverstart():
    try:
        server = socketserver.ThreadingTCPServer(('hejie-ThinkPad-L450.local',8009),AsrServer)
        server.serve_forever()
    except Exception as e:
        LOG.exception(e)

def byte2frame(byte_queue, frame_queue):
    try:
        while True:
            byte = byte_queue.get()
            #LOG.debug('byte2frame %s**************' % len(byte))
            isspeech = hjvad.vad.is_speech(byte)
            frame = hjvad.Frame(byte, isspeech = isspeech)
            frame_queue.put(frame)
    except Exception as e:
        LOG.exception(e)

def queuesbuild():
    LOG.debug('queues building*******************')
    global byte_queues
    byte_queues = []
    frame_queues = []
    procs = []
    for i in range(N_PROC):
        byte_queues.append(Queue())
        frame_queues.append(Queue())
        procs.append(Process(target=byte2frame, args=(byte_queues[i], frame_queues[i])))
        procs[i].start()

    Process(target = asrserverstart).start()
    return frame_queues

def pytorchasrstart():
    LOG.debug('pytorchasrstart*******************')
    frame_queues = queuesbuild()
    pool = Pool(multiprocessing.cpu_count()-1)
    for segment in iter(hjvad.vad_split(frame_queues)):
        LOG.debug('end--------------')
        #pool.apply_async(hjtorch.predict, args=(segment, ))  

if __name__ == '__main__':
    pytorchasrstart()
