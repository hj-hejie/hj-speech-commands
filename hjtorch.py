import pdb
import torchvision
from torchvision.transforms import *
from transforms import *
import librosa
from datasets import *
import torch
from torch.autograd import Variable
import transforms.librosa2 as lr

transform = Compose([FixAudioLength(), ToMelSpectrogram(n_mels=40), ToTensor('mel_spectrogram', 'input')])

#samples, sample_rate = librosa.load('datasets/speech_commands_origin/train/no/a05a90c1_nohash_2.wav', None)
#samples, sample_rate = librosa.load('datasets/speech_commands_origin/train/yes/a05a90c1_nohash_0.wav', None)
#samples, sample_rate = librosa.load('datasets/speech_commands/train/guandianshi/01.wav', None)
#samples, sample_rate = librosa.load('datasets/speech_commands/train/kaidianshi/s99901.wav', None)
model = torch.load('1533716526919-vgg19_bn_sgd_plateau_bs96_lr1.0e-02_wd1.0e-02-best-acc.pth')
#model = torch.load('hj-best-acc.pth')
model.float()
while True:
    samples, sample_rate=lr.loadfrommic()
    data={}
    data['samples'] = samples
    data['sample_rate'] = sample_rate
    rs=transform(data)
    _in=rs['input'].unsqueeze(0)
    _in=torch.unsqueeze(_in, 1)
    _in= Variable(_in)
    out=model(_in)
    #print out
    #print torch.argmax(out)
    from datasets import CLASSES as _CLASS
    print _CLASS[torch.argmax(out)]
