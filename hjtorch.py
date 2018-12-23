import pdb
import torchvision
from torchvision.transforms import *
from transforms import *
import librosa
from datasets import *
import torch
from torch.autograd import Variable
from torch.nn.functional import softmax
import transforms.librosa2 as lr

transform = Compose([FixAudioLength(time=2), ToMelSpectrogram(n_mels=40), ToTensor('mel_spectrogram', 'input')])
model = torch.load('torch_predict.model')
model.float()

def predict(frames, frame_rate = 10000, frame_width = 1):
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
    print(out)
    print(torch.argmax(out))
    from datasets import CLASSES as _CLASS
    print(torch.max(out))
    print(_CLASS[torch.argmax(out)])

if __name__ == '__main__':
   predict(None, None, None) 
