import pdb
import collections
import contextlib
import sys
import wave
import argparse
import torch
from torch.autograd import Variable
from torch.nn.functional import softmax
import transforms.librosa2 as lr
from torchvision.transforms import *
from transforms import *
#import webrtcvad
from datasets import CLASSES as _CLASS

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--sample-rate', type=int, default=10000)
parser.add_argument('--sample-width', type=int, default=1)
parser.add_argument('--sample-time', type=float, default=0.02)
parser.add_argument('--n-mels', type=int, default=32)
parser.add_argument('--n-fft', type=int, default=80)
parser.add_argument('--hop-length', type=int, default=10)
parser.add_argument('--model', type=str, default='1544897548406-vgg19_bn_sgd_plateau_bs96_lr1.0e-02_wd1.0e-02-best-acc.pth')
parser.add_argument('--frame-duration-ms', type=float, default=20)
parser.add_argument('--padding-duration-ms', type=float, default=200)
args = parser.parse_args()
 
class Nnvad(object):
    def __init__(self, sample_time = args.sample_time, n_mels = args.n_mels):
        self.transform = Compose([FixAudioLength(time = sample_time),
                                  ToMelSpectrogram(n_mels = n_mels, n_fft=args.n_fft, hop_length=args.hop_length),
                                  ToTensor('mel_spectrogram', 'input')])
        self.model = torch.load(args.model)
        self.model.float()

    def is_speech(self, bytes, sample_rate, sample_width):
        samples, _sample_rate= lr.loadfrombuff(bytes, sample_rate, sample_width)
        rs = self.transform({
            'samples' : samples,
            'sample_rate' : _sample_rate
        })
        input = Variable(torch.unsqueeze(rs['input'].unsqueeze(0), 1))
        output = self.model(input)
        out_softmax = softmax(output, dim=1)
        return _CLASS[torch.argmax(out_softmax)] == _CLASS[1]
 
def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_rate = wf.getframerate()
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate
 
 
def write_wave(path, audio):
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(args.sample_width)
        wf.setframerate(args.sample_rate)
        wf.writeframes(audio)
 
 
class Frame(object):
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration
 
 
def frame_generator(audio, frame_duration_ms = args.frame_duration_ms,
                    sample_rate = args.sample_rate, sample_width = args.sample_width):
    n = int(sample_rate * (frame_duration_ms / 1000.0) * sample_width)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate)/sample_width
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n
 
def socket_frame_generator(request, frame_duration_ms = args.frame_duration_ms,
                    sample_rate = args.sample_rate, sample_width = args.sample_width):
    n = int(sample_rate * (frame_duration_ms / 1000.0) * sample_width)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate)/sample_width
    buffer=b''
    while True:
        bytes=request.recv(n)
        if bytes.strip():
            print('Asr %s sounds getted********************'%len(bytes))
            buffer+=bytes
            if len(buffer) >= n:
                yield Frame(buffer[ : n], timestamp, duration)
                buffer=buffer[n : ]
                timestamp += duration
                offset += n * width
 
def vad_collector(vad, frames,
                  sample_rate = args.sample_rate, sample_width = args.sample_width,
                  frame_duration_ms = args.frame_duration_ms,
                  padding_duration_ms = args.padding_duration_ms):
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    triggered = False
    voiced_frames = []
    for i, frame in enumerate(frames):
        sys.stdout.write(
            '1' if vad.is_speech(frame.bytes, sample_rate, sample_width) else '0')
        if not triggered:
            ring_buffer.append(frame)
            num_voiced = len([f for f in ring_buffer
                              if vad.is_speech(f.bytes, sample_rate, sample_width)])
            if num_voiced > 0.9 * ring_buffer.maxlen:
                sys.stdout.write('+(%s)' % (ring_buffer[0].timestamp,))
                triggered = True
                voiced_frames.extend(ring_buffer)
                ring_buffer.clear()
        else:
            voiced_frames.append(frame)
            ring_buffer.append(frame)
            num_unvoiced = len([f for f in ring_buffer
                                if not vad.is_speech(f.bytes, sample_rate, sample_width)])
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
                triggered = False
                yield b''.join([f.bytes for f in voiced_frames])
                ring_buffer.clear()
                voiced_frames = []
    if triggered:
        sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
    sys.stdout.write('\n')
    if voiced_frames:
        yield b''.join([f.bytes for f in voiced_frames])
 
 
def main(args):
    '''
    if len(args) != 2:
        sys.stderr.write(
            'Usage: example.py <aggressiveness> <path to wav file>\n')
        sys.exit(1)
    audio, sample_rate = read_wave(args[1])
    vad = webrtcvad.Vad(int(args[0]))
    '''
    #audio, _sample_rate = read_wave('datasets/speech_commands_esp/_background_noise_/20181209190151.wav')
    audio, _sample_rate = read_wave('datasets/speech_commands_esp/kaideng/20181209192108.wav')
    #vad = webrtcvad.Vad(2)
    vad = Nnvad()
    frames = frame_generator(audio)
    segments = vad_collector(vad, frames)
    for i, segment in enumerate(segments):
        path = 'chunk-%002d.wav' % (i,)
        #print('--end')
        write_wave(path, segment)
 
 
if __name__ == '__main__':
    main(sys.argv[1:])
