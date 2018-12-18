import pdb
import logging
import os
import sys
sys.path.append(os.getcwd())
import time
import numpy as np
import collections
import socketserver
#import webrtcvad
import audioop
import torch
from torch.autograd import Variable
import transforms.librosa2 as lr
#import wave
#import contextlib
from torchvision.transforms import *
from transforms import *
from torch.nn.functional import softmax
from torch.autograd import Variable
import hjvad
from homeassistant.const import EVENT_HOMEASSISTANT_START

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'pytorchasr'

transform = Compose([FixAudioLength(time=2), ToMelSpectrogram(n_mels=40), ToTensor('mel_spectrogram', 'input')])
model = torch.load('1533806137984-vgg19_bn_sgd_plateau_bs100_lr1.0e-02_wd1.0e-02-best-acc.pth')
model.float()
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
            '''
            print('Asr segment getted**********************')
            samples, sample_rate=lr.loadfrombuff(segment.bytes, 10000, 1)
            data={
                'samples' : samples
                'sample_rate' : sample_rate
            }
            rs=transform(data)
            _in=rs['input'].unsqueeze(0)
            _in=torch.unsqueeze(_in, 1)
            _in= Variable(_in)
            out=model(_in)
            out=softmax(out, dim=1)
            print(out)
            print(torch.argmax(out))
            from datasets import CLASSES as _CLASS
            print(torch.max(out))
            print(_CLASS[torch.argmax(out)])
            '''

if __name__ == '__main__':
    pytorchasrstart(None)
