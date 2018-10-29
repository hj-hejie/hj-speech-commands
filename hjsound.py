import wave
from pyaudio import PyAudio,paInt16

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
    fms_byte=orign.readframes(orign.getnframes())
    orign.close()
    dest=wave.open('hjwavtest02.wav', 'wb')
    dest.setnchannels(channels)
    dest.setsampwidth(sampwidth)
    dest.setframerate(framerate)
    dest.writeframes(fms_byte)
    dest.close()

def mywrite():
    buf=[]
    for i in range(32000):
        buf.append(i%(2**8))
    fms_byte=bytes(buf)
    dest=wave.open('hjwavtest03.wav', 'wb')
    dest.setnchannels(channels)
    dest.setsampwidth(sampwidth)
    dest.setframerate(framerate)
    dest.writeframes(fms_byte)
    dest.close()

if __name__ == '__main__':
    #my_record()
    #rewrite()
    mywrite()
    print('Over!') 
