import pdb
import logging
import os
import sys
import time
import numpy as np
import collections
import socketserver
import audioop
import torch
from torch.autograd import Variable
from torchvision.transforms import *
from torch.nn.functional import softmax
from torch.autograd import Variable
from homeassistant.const import EVENT_HOMEASSISTANT_START
sys.path.append(os.getcwd())
import transforms.librosa2 as lr
from transforms import *
import hjvad
import hjtorch

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'pytorchasr'

vad = hjvad.Nnvad()

async def async_setup(hass, config):
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, pytorchasrstart)
    return True 

def pytorchasrstart(self):
    _LOGGER.info('pytorch asr start***********************************')
    print('pytorch asr starting***********************************')
    server = socketserver.ThreadingTCPServer(('hejie-ThinkPad-L450.local',8009),AsrServer)
    server.serve_forever()
    print('pytorch asr started********************************')

class AsrServer(socketserver.BaseRequestHandler):

    def handle(self):
        _LOGGER.info('AsrServer handling*******************************')
        frames = hjvad.socket_frame_generator(self.request)
        segments = hjvad.vad_collector(vad, frames)
        for i, segment in enumerate(segments):
            print('--end')
            #path = 'chunk-%002d.wav' % (i,)
            #hjvad.write_wave(path, segment.bytes, 1, 10000)
            #hjtorch.predict(segment.bytes, 10000, 1)

if __name__ == '__main__':
    pytorchasrstart(None)
