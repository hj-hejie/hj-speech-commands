import pdb
import torchvision
from torchvision.transforms import *
from transforms import *
import librosa
from datasets import *
import torch
from torch.autograd import Variable

data_aug_transform = Compose([ChangeAmplitude(), ChangeSpeedAndPitchAudio(), FixAudioLength(), ToSTFT(), StretchAudioOnSTFT(), TimeshiftAudioOnSTFT(), FixSTFTDimension()])
bg_dataset = BackgroundNoiseDataset('datasets/speech_commands/train/_background_noise_', data_aug_transform)
add_bg_noise = AddBackgroundNoiseOnSTFT(bg_dataset)
train_feature_transform = Compose([ToMelSpectrogramFromSTFT(n_mels=32), DeleteSTFT(), ToTensor('mel_spectrogram', 'input')])
#transform=Compose([data_aug_transform,add_bg_noise,train_feature_transform])
transform=Compose([data_aug_transform,train_feature_transform])
samples, sample_rate = librosa.load('datasets/speech_commands/train/bed/a045368c_nohash_0.wav', None)
data={}
data['samples'] = samples
data['sample_rate'] = sample_rate
rs=transform(data)
model = torch.load('1532663566279-vgg19_bn_sgd_plateau_bs96_lr1.0e-02_wd1.0e-02-best-acc.pth')
model.float()
_in=torch.unsqueeze(rs['input'], 1)
_in= Variable(_in)
pdb.set_trace()
out=model(_in)
pdb.set_trace()
print 'hejie'
