import random
import wave
from pyaudio import PyAudio,paInt16
import audioop
import librosa

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
    orign=wave.open('hjwavtest01.wav')
    fms_byte=orign.readframe(orign.getnframes())
    orign.close()
    dest=wave.open('hjwavtest02.wav', 'wb')
    dest.setnchannels(channels)
    dest.setsampwidth(sampwidth)
    dest.setframerate(framerate)
    dest.writeframes(fms_byte)
    dest.close()

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
    s_read = wave.open('hjwavtest03.wav', 'r')
    s_write = wave.open('hjwavtest04.wav', 'w')
    n_frames = s_read.getnframes()
    data = s_read.readframes(n_frames)
    in_channels=1
    in_width=1
    in_rate=10000
    out_channels=1
    out_width=1
    out_rate=16000
    converted = audioop.ratecv(data, in_width, in_channels, in_rate, out_rate, None)
    s_write.setparams((out_channels, out_width, out_rate, 0, 'NONE', 'Uncompressed'))
    s_write.writeframes(converted[0])
    s_read.close()
    s_write.close()

def conv2():
    filename = 'hjwavtest03.wav'
    newFilename = 'hjwavtest04.wav'
    y, sr = librosa.load(filename, sr=10000)
    y_8k = librosa.resample(y,sr,16000)
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

if __name__ == '__main__':
    #my_record()
    #rewrite()
    mywrite()
    #conv()
    #conv2()
    print('Over!') 
