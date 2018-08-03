__author__ = 'hejie'

import os
import numpy as np

import librosa

from torch.utils.data import Dataset

__all__ = [ 'MicCommandsDataset']

class MicCommandsDataset(Dataset):

    def __init__(self):
        data_aug_transform = Compose([ChangeAmplitude(), ChangeSpeedAndPitchAudio(), FixAudioLength(), ToSTFT(), StretchAudioOnSTFT(), TimeshiftAudioOnSTFT(), FixSTFTDimension()])
        bg_dataset = BackgroundNoiseDataset('datasets/speech_commands/train/_background_noise_', data_aug_transform)
        add_bg_noise = AddBackgroundNoiseOnSTFT(bg_dataset)
        train_feature_transform = Compose([ToMelSpectrogramFromSTFT(n_mels=32), DeleteSTFT(), ToTensor('mel_spectrogram', 'input')])
        self.transform=Compose([data_aug_transform,add_bg_noise,train_feature_transform])
        samples, sample_rate = librosa.load('datasets/speech_commands/train/bed/a045368c_nohash_0.wav', None)
        self.data={}
        self.data['samples'] = samples 
        self.data['sample_rate'] = sample_rate

    def __len__(self):
        return 1

    def __getitem__(self, index):
        return self.transform(self.data)
