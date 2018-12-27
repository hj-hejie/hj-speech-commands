import pdb
import logging
import torchvision
from torchvision.transforms import *
from transforms import *
import librosa
from datasets import *
import torch
from torch.autograd import Variable
from torch.nn.functional import softmax
import transforms.librosa2 as lr
import hjlog

LOG = logging.getLogger(__name__)

transform = Compose([FixAudioLength(time=2), ToMelSpectrogram(n_mels=40), ToTensor('mel_spectrogram', 'input')])
model = torch.load('torch_predict.model')
model.float()

def predict(frames, frame_rate = 10000, frame_width = 1):
    try:
        LOG.debug('hjtorch precdict ************')
        #samples, sample_rate = librosa.load('datasets/speech_commands/train/guankongtiao/s020181209193112.wav', None)
        samples, sample_rate=lr.loadfrombuff(frames, frame_rate, frame_width)
        data={
            'samples' : samples,
            'sample_rate' : sample_rate
        }
        rs=transform(data)
        _in=rs['input'].unsqueeze(0)
        _in=torch.unsqueeze(_in, 1)
        _in= Variable(_in)
        out=model(_in)
        out=softmax(out, dim=1)
        LOG.debug(out)
        LOG.debug(torch.argmax(out))
        from datasets import CLASSES as _CLASS
        LOG.debug(torch.max(out))
        LOG.debug(_CLASS[torch.argmax(out)])
    except Exception as e:
        LOG.exception(e)

if __name__ == '__main__':
   predict(None, None, None) 
