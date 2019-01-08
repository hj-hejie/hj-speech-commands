import pdb
import logging
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
from datasets import CLASSES2 as _CLASS
import hjlog

DEF_SAMPLE_RATE = 10000
DEF_SAMPLE_WIDTH = 1
DEF_DURATION = 0.02
DEF_PADDING = 0.2
DEF_N_REQ = int(10000 * 2)
DEF_N_DURATION = int(DEF_N_REQ / ( DEF_DURATION * DEF_SAMPLE_RATE))

LOG = logging.getLogger(__name__)

class Nnvad(object):
    def __init__(self, sample_time = 0.02, n_mels = 32, n_fft=80, hop_length=10):
        self.transform = Compose([FixAudioLength(time = sample_time),
                                  ToMelSpectrogram(n_mels = n_mels, n_fft=n_fft, hop_length=hop_length),
                                  ToTensor('mel_spectrogram', 'input')])
        self.model = torch.load('torch_vad.model')
        self.model.float()

    def is_speech(self, bytes, sample_rate = DEF_SAMPLE_RATE, sample_width = DEF_SAMPLE_WIDTH):
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

def read_wave_queue(path):
    from queue import Queue
    queues = [Queue()]
    data, rate = read_wave(path)
    l_data = len(data)
    for i in range(0, l_data, 200):
        if i+200 <= l_data:
            frame_data = data[i: i+200];
            isspeech = vad.is_speech(frame_data)
            frame = Frame(frame_data, isspeech = isspeech)
            queues[0].put(frame)
    LOG.debug('read_wave_queue end***********')
    return queues
 
def write_wave(path, audio, sample_width = DEF_SAMPLE_WIDTH, sample_rate = DEF_SAMPLE_RATE):
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)
 
 
class Frame(object):
    def __init__(self, bytes, timestamp=None, duration=None, isspeech=None):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration
        self.isspeech = isspeech
 
def frame_generator(audio, frame_duration_ms = DEF_DURATION,
                    sample_rate = DEF_SAMPLE_RATE, sample_width = DEF_SAMPLE_WIDTH):
    n = int(sample_rate * frame_duration_ms * sample_width)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate)/sample_width
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n * sample_width
 
def socket_frame_generator(request, n_request = DEF_N_REQ, frame_duration_ms = DEF_DURATION,
                    sample_rate = DEF_SAMPLE_RATE, sample_width = DEF_SAMPLE_WIDTH):
    n_duration_bytes = int(sample_rate * frame_duration_ms * sample_width)
    timestamp = 0.0
    duration = (float(n_duration_bytes) / sample_rate)/sample_width
    n_remain = 0
    count_ = 0
    while True:
        if n_remain <= 0:
            count_+=1
            request.sendall(b'1')
            n_remain = n_request
            buffer = b''
        bytes_recv = request.recv(n_remain)
        if bytes_recv.strip():
            n_remain = n_remain - len(bytes_recv)
            buffer += bytes_recv
            while len(buffer) >= n_duration_bytes:
                yield Frame(buffer[ : n_duration_bytes], timestamp, duration)
                buffer = buffer[n_duration_bytes : ]
                timestamp += duration
                
def queue_frame_generator(queues, frame_duration_ms = DEF_DURATION,
                    sample_rate = DEF_SAMPLE_RATE, sample_width = DEF_SAMPLE_WIDTH):
    n_queue = len(queues)
    n_duration_bytes = int(sample_rate * frame_duration_ms  * sample_width)
    timestamp = 0.0
    duration = (float(n_duration_bytes) / sample_rate)/sample_width
    i_proc = 0
    #while True:
    while not queues[i_proc].empty():
        frame =  queues[i_proc].get()
        frame.timestamp, frame.duration = timestamp, duration
        #LOG.debug('queue_frame_generate %s yield %s*************************' % (i_proc, len(frame.bytes)))
        yield frame
        timestamp += duration
        i_proc = (i_proc + 1) % n_queue
                
def vad_collector(vad, frames,
                  sample_rate = DEF_SAMPLE_RATE, sample_width = DEF_SAMPLE_WIDTH,
                  frame_duration_ms = DEF_DURATION,
                  padding_duration_ms = DEF_PADDING):
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    ring_buffer_vad_bool = collections.deque(maxlen=num_padding_frames)
    triggered = False
    voiced_frames = []
    for frame in iter(frames):
        isspeech='1' if vad.is_speech(frame.bytes, sample_rate, sample_width) else '0'
        ring_buffer_vad_bool.append(isspeech)
        #sys.stdout.write(isspeech)
        if not triggered:
            ring_buffer.append(frame)
            num_voiced = len([f for f in ring_buffer_vad_bool if f == '1'])
            if num_voiced > 0.9 * ring_buffer.maxlen:
                #sys.stdout.write('+(%s)' % (ring_buffer[0].timestamp,))
                triggered = True
                voiced_frames.extend(ring_buffer)
                ring_buffer.clear()
                ring_buffer_vad_bool.clear()
        else:
            voiced_frames.append(frame)
            ring_buffer.append(frame)
            num_unvoiced = len([f for f in ring_buffer_vad_bool if f == '0'])
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                #sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
                triggered = False
                LOG.debug('queue_vad_collect yield***********************')
                yield b''.join([f.bytes for f in voiced_frames])
                ring_buffer.clear()
                ring_buffer_vad_bool.clear()
                voiced_frames = []
    #if triggered:
        LOG.debug('queue_vad_collect end yield***********************')
        #sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
    #sys.stdout.write('\n')
    if voiced_frames:
        yield b''.join([f.bytes for f in voiced_frames])

def queue_vad_collector(frames,
                  sample_rate = DEF_SAMPLE_RATE, sample_width = DEF_SAMPLE_WIDTH,
                  frame_duration_ms = DEF_DURATION,
                  padding_duration_ms = DEF_PADDING, 
                  n_duration = DEF_N_DURATION, sense = 0.9):
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    ring_buffer = collections.deque(maxlen = num_padding_frames)
    ring_buffer_vad_bool = collections.deque(maxlen = num_padding_frames)
    voiced_frames = collections.deque(maxlen = n_duration)
    triggered = False
    for frame in iter(frames):
        ring_buffer_vad_bool.append(frame.isspeech)
        LOG.debug('Is speech : %s' % frame.isspeech)
        if not triggered:
            ring_buffer.append(frame)
            num_voiced = len([f for f in ring_buffer_vad_bool if f])
            #LOG.debug('hejie num_voiced=%s' % num_voiced)
            if num_voiced > sense * ring_buffer.maxlen:
                #sys.stdout.write('+(%s)' % (ring_buffer[0].timestamp,))
                triggered = True
                voiced_frames.extend(ring_buffer)
                ring_buffer.clear()
                ring_buffer_vad_bool.clear()
        else:
            voiced_frames.append(frame)
            ring_buffer.append(frame)
            num_unvoiced = len([f for f in ring_buffer_vad_bool if not f])
            #LOG.debug('hejie num_unvoiced=%s' % num_unvoiced)
            if num_unvoiced > sense * ring_buffer.maxlen:
                #sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
                triggered = False
                yield b''.join([f.bytes for f in voiced_frames])
                ring_buffer.clear()
                ring_buffer_vad_bool.clear()
                voiced_frames.clear()
    #if triggered:
        #sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
    #sys.stdout.write('\n')
    if voiced_frames:
        yield b''.join([f.bytes for f in voiced_frames])
 
vad = Nnvad()

def vad_split(queues):
    frames = queue_frame_generator(queues)
    segments = queue_vad_collector(frames)
    for segment in iter(segments):
        yield segment

if __name__ == '__main__':
    #queues = read_wave_queue('datasets/speech_commands_esp/guandeng/20181209192400.wav')
    #queues = read_wave_queue('datasets/speech_commands_esp/kaideng/20181209192108.wav')
    #queues = read_wave_queue('datasets/speech_commands_esp/_background_noise_/20181209190233.wav')
    #queues = read_wave_queue('datasets/speech_commands_esp/_background_noise_/20181209190241.wav')
    #queues = read_wave_queue('datasets/speech_commands_esp/guankongtiao/20190106152103.wav')
    #queues = read_wave_queue('datasets/speech_commands_esp/_background_noise_/20190106152632.wav')
    queues = read_wave_queue('datasets/speech_commands_esp/_background_noise_/20190106144805.wav')
    for segment in iter(vad_split(queues)):
        print('--end')
        #write_wave('chunck02.wav', segment)

if __name__ == '__main__2':
    #audio, _sample_rate = read_wave('datasets/speech_commands_esp/_background_noise_/20181209190151.wav')
    #audio, _sample_rate = read_wave('datasets/speech_commands_esp/_background_noise_/20181209190241.wav')
    #audio, _sample_rate = read_wave('datasets/speech_commands_esp_vad/train/_background_noise_/13chunk20181209190151.wav')
    audio, _sample_rate = read_wave('datasets/speech_commands_esp_vad/train/speech/13chunk20181209192108.wav')
    LOG.debug(vad.is_speech(audio))
