import pdb
import torchvision
from torchvision.transforms import *
from transforms import *
import librosa
from datasets import *
import torch
from torch.autograd import Variable
import transforms.librosa2 as lr

data_aug_transform = Compose([ChangeAmplitude(), ChangeSpeedAndPitchAudio(), FixAudioLength(), ToSTFT(), StretchAudioOnSTFT(), TimeshiftAudioOnSTFT(), FixSTFTDimension()])
bg_dataset = BackgroundNoiseDataset('datasets/speech_commands/train/_background_noise_', data_aug_transform)
add_bg_noise = AddBackgroundNoiseOnSTFT(bg_dataset)
train_feature_transform = Compose([ToMelSpectrogramFromSTFT(n_mels=32), DeleteSTFT(), ToTensor('mel_spectrogram', 'input')])
#transform=Compose([data_aug_transform,add_bg_noise,train_feature_transform])
transform=Compose([data_aug_transform,train_feature_transform])
#samples, sample_rate = librosa.load('datasets/speech_commands/train/no/a05a90c1_nohash_2.wav', None)
#samples, sample_rate = librosa.load('hjlibrosa2.wav', None)
model = torch.load('1532663566279-vgg19_bn_sgd_plateau_bs96_lr1.0e-02_wd1.0e-02-best-acc.pth')
model.float()
while True:
    samples, sample_rate=lr.loadfrommic()
    data={}
    data['samples'] = samples
    data['sample_rate'] = sample_rate
    rs=transform(data)
    _in=rs['input'].reshape(1, 32, 32)
    _in=torch.unsqueeze(_in, 1)
    _in= Variable(_in)
    out=model(_in)
    print out
    print torch.argmax(out)
    from datasets import CLASSES as _CLASS
    print _CLASS[torch.argmax(out)]
