import pdb
import torchvision
from torchvision.transforms import *
from transforms import *
import librosa
from datasets import *
import torch
from torch.autograd import Variable
from torch.nn.functional import softmax
#import transforms.librosa2 as lr

transform = Compose([FixAudioLength(time=2), ToMelSpectrogram(n_mels=40), ToTensor('mel_spectrogram', 'input')])

#samples, sample_rate = librosa.load('datasets/speech_commands_origin/train/no/a05a90c1_nohash_2.wav', None)
#samples, sample_rate = librosa.load('datasets/speech_commands_origin/train/yes/a05a90c1_nohash_0.wav', None)
#samples, sample_rate = librosa.load('hjwavkaikongtiao0.wav', None)
#samples, sample_rate = librosa.load('datasets/speech_commands/train/kaidianshi/01.wav', None)
samples, sample_rate = librosa.load('hjwavtest13.wav', None)
model = torch.load('1533806137984-vgg19_bn_sgd_plateau_bs100_lr1.0e-02_wd1.0e-02-best-acc.pth')
#model = torch.load('hj-best-acc.pth')
model.float()
count=0
if True:
    #samples, sample_rate=lr.loadfrombuff(None)
    data={}
    data['samples'] = samples
    data['sample_rate'] = sample_rate
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
    #lr.output.write_wav('hjwav'+_CLASS[torch.argmax(out)]+str(count)+'.wav', samples, sample_rate)
    count+=1
