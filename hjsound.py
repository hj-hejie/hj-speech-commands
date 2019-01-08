import random
import sys
import numpy as np
import wave
from pyaudio import PyAudio,paInt16
import audioop
import librosa
import pdb
import pylab as pl

framerate=8000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2
def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while count<8:
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1
        print('.')
    save_wave_file('hjwavtest01.wav',my_buf)
    stream.close()

def rewrite():
    orign=wave.open('hass/asr20181208231910.wav')
    fms_byte=orign.readframes(orign.getnframes())
    orign.close()
    dest=wave.open('hjwavtest12.wav', 'wb')
    rebyte = audioop.lin2lin(fms_byte, 1, 2)
    cvbyte=audioop.ratecv(rebyte, 2, 1, 8000, 16000, None)[0]
    pdb.set_trace()
    dest.setnchannels(1)
    dest.setsampwidth(2)
    dest.setframerate(16000)
    dest.writeframes(cvbyte)
    dest.close()

def rewrite2():
    orign=wave.open('hjwavtest11.wav')
    fms_byte=orign.readframes(orign.getnframes())
    orign.close()
    rebyte=librosa.util.buf_to_float(fms_byte, 1)
    resamp = librosa.resample(np.concatenate([rebyte]), 10000, 16000, res_type='kaiser_best')
    if sys.version_info[0] >= 4:
        _bytes=resamp.ravel().view('b').data
    else:
        _bytes=resamp.tostring()
    writed=audioop.lin2lin(_bytes, 4, 2)
    pdb.set_trace()
    wf=wave.open('hjwavtest13.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)
    wf.writeframes(writed)
    wf.close()

def mywrite():
    buf=[]
    for i in range(20000):
        #buf.append((random.randint(0,2**10-1)*64).to_bytes(2, byteorder='little'))
        #buf.append(random.randint(0,2**16-1).to_bytes(2, byteorder='little'))
        buf.append(random.randint(0,2**8-1))
    fms_byte=bytes(buf)
    #fms_byte=b''.join(buf)
    dest=wave.open('hjwavtest03.wav', 'wb')
    dest.setnchannels(1)
    dest.setsampwidth(2)
    dest.setframerate(10000)
    dest.writeframes(fms_byte)
    dest.close()

def conv():
    s_read = wave.open('datasets/speech_commands/train/kaidianshi/01.wav', 'r')
    s_write = wave.open('hjwavtest11.wav', 'w')
    n_frames = s_read.getnframes()
    data = s_read.readframes(n_frames)
    in_channels=1
    in_width=2
    in_rate=16000
    out_channels=1
    out_width=1
    out_rate=10000
    rebyte = audioop.lin2lin(data, in_width, out_width)
    rerate = audioop.ratecv(rebyte, out_width, in_channels, in_rate, out_rate, None)
    pdb.set_trace()
    s_write.setparams((out_channels, out_width, out_rate, 0, 'NONE', 'Uncompressed'))
    s_write.writeframes(rerate[0])
    s_read.close()
    s_write.close()

def conv2():
    filename = 'hjwavtest03.wav'
    newFilename = 'hjwavtest04.wav'
    y, sr = librosa.load(filename, sr=10000)
    y_8k = librosa.resample(y,sr,16000)
    pdb.set_trace()
    librosa.output.write_wav(newFilename, y_8k, 16000)


def resample(input_signal,src_fs,tar_fs):
    '''

    :param input_signal:输入信号
    :param src_fs:输入信号采样率
    :param tar_fs:输出信号采样率
    :return:输出信号
    '''

    dtype = input_signal.dtype
    audio_len = len(input_signal)
    audio_time_max = 1.0*(audio_len-1) / src_fs
    src_time = 1.0 * np.linspace(0,audio_len,audio_len) / src_fs
    tar_time = 1.0 * np.linspace(0,np.int(audio_time_max*tar_fs),np.int(audio_time_max*tar_fs)) / tar_fs
    output_signal = np.interp(tar_time,src_time,input_signal).astype(dtype)

    return output_signal

def plot():
    wavs = [
        #r"datasets/speech_commands_esp/kaideng/20190106150628.wav",
        #r"datasets/speech_commands_esp/guandeng/20181209192315.wav",
        #r"datasets/speech_commands_esp/_background_noise_/20190106144856.wav",
        #r"datasets/speech_commands_esp/_background_noise_/20181209190241.wav",
        r"datasets/speech_commands_origin/train/cat/012c8314_nohash_0.wav",
        r"datasets/speech_commands_origin/train/_background_noise_/white_noise.wav"
    ]

    for i, wav in enumerate(wavs):
        f = wave.open(wav, "rb")
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        str_data = f.readframes(nframes)
        f.close()
        wave_data = np.fromstring(str_data, dtype=np.short)
        time = np.arange(0, nframes) * (1.0 / framerate)
        df = 1 
        freq = [df*n for n in range(0,len(wave_data))]
        fft = abs(np.fft.fft(wave_data)) / len(wave_data)
        pl.subplot(len(wavs)*100 + 11 + i)
        #pl.plot(time, wave_data)
        #pl.xlabel("time (seconds)")
        pl.plot(freq, fft)
    pl.show()

if __name__ == '__main__':
    #my_record()
    #rewrite()
    #rewrite2()
    #mywrite()
    #conv()
    #conv2()
    plot()
    print('Over!') 
