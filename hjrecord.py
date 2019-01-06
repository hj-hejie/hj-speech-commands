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
            wavfile = 'datasets/speech_commands_esp/_background_noise_/%s.wav' % time.strftime('%Y%m%d%H%M%S', time.localtime())
            #wavfile = 'datasets/speech_commands_esp/kaideng/%s.wav' % time.strftime('%Y%m%d%H%M%S', time.localtime())
            #wavfile = 'datasets/speech_commands_esp/guandeng/%s.wav' % time.strftime('%Y%m%d%H%M%S', time.localtime())
            #wavfile = 'datasets/speech_commands_esp/kaikongtiao/%s.wav' % time.strftime('%Y%m%d%H%M%S', time.localtime())
            #wavfile = 'datasets/speech_commands_esp/guankongtiao/%s.wav' % time.strftime('%Y%m%d%H%M%S', time.localtime())
            #wavfile = 'datasets/speech_commands_esp/kaidianshi/%s.wav' % time.strftime('%Y%m%d%H%M%S', time.localtime())
            #wavfile = 'datasets/speech_commands_esp/guandianshi/%s.wav' % time.strftime('%Y%m%d%H%M%S', time.localtime())
            LOG.debug('create file %s len %s*************************' % (wavfile, len(buff)))
            hjvad.write_wave(wavfile, buff)
            buff = b''
