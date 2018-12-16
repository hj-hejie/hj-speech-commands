from audioread import *
from audioread.rawread import *
import audioop

class RawAudioBuff(RawAudioFile):

    def __init__(self, buff, sample_rate, sample_width = 2):
        self.buff = buff
        self.sample_rate = sample_rate
        self.sample_width = sample_width

    def read_data(self):
        data = audioop.lin2lin(self.buff, self.sample_width, TARGET_WIDTH)
        yield data

    def close(self):
        pass

    @property
    def channels(self):
        return 1

    @property
    def samplerate(self):
        return self.sample_rate
    
