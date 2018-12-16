import logging
import sys
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
import pdb
from torchvision.transforms import *
from transforms import *
from torch.nn.functional import softmax
from torch.autograd import Variable
from homeassistant.components.light import Light
import hjvad

_LOGGER = logging.getLogger(__name__)

transform = Compose([FixAudioLength(time=2), ToMelSpectrogram(n_mels=40), ToTensor('mel_spectrogram', 'input')])
model = torch.load('1533806137984-vgg19_bn_sgd_plateau_bs100_lr1.0e-02_wd1.0e-02-best-acc.pth')
model.float()
vad = hjvad.Nnvad()

def setup_platform(hass, config, add_devices, discovery_info=None):
    add_devices([Asr(hass)])

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
    print('hejiestart')
    server = socketserver.ThreadingTCPServer(('hejie-ThinkPad-L450.local',8009),AsrServer)
    server.serve_forever()
    print('hejieok')
