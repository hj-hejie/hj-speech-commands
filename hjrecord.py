import pdb
import logging
import time
import __init__
import hjvad
import hjlog

LOG = logging.getLogger(__name__)

if __name__ == '__main__': 
    frame_queues = __init__.queuesbuild()
    frame_gen = hjvad.queue_frame_generator(frame_queues)
    buff = b''
    for i, frame in enumerate(frame_gen):
        LOG.debug('frame %s*********' % i)
        buff += frame.bytes
        if i%100 == 99:
            LOG.debug('create file len %s*************************' % len(buff))
            hjvad.write_wave('chunck01.wav', buff)
            buff = b''
