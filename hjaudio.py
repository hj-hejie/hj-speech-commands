import wave
import numpy as np
import matplotlib.pyplot as plt
from pyaudio import PyAudio,paInt16
import pdb

#file = 'datasets/speech_commands/train/bird/a045368c_nohash_0.wav'
file = '01.wav'

def audio():
	
	wav=wave.open(file, 'r')
	frames=wav.readframes(-1)
	wav.close()
	frames=np.fromstring(frames, np.short)
	nchs=wav.getnchannels()
	chs=[[] for nch in range(nchs)]
	for i, frame in enumerate(frames):
		chs[i%len(chs)].append(frame)
	
	fs=wav.getframerate()
	times=np.linspace(0, len(frames)/len(chs)/fs, num=len(frames)/len(chs))
	
	c=['green', 'blue']
	plt.title(nchs)
	for i, ch in enumerate(chs):
		plt.plot(times, ch, color=c[i])
	plt.show()

def save_wave_file(filename,data):
    wf=wave.open(filename,'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)
    wf.writeframes(b"".join(data))
    wf.close()

def record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=16000,input=True,
                   frames_per_buffer=1)
    my_buf=[]
    count=0
    while count<5:
        string_audio_data = stream.read(16000)
        my_buf.append(string_audio_data)
        count+=1
        print('.')
    save_wave_file(file,my_buf)
    stream.close()

def play():
    wf=wave.open(file,'r')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
    wf.getnchannels(),rate=wf.getframerate(),output=True)
    data=wf.readframes(8000)
    while len(data)>0:
        stream.write(data)
        data=wf.readframes(8000)
    stream.close()
    p.terminate()


def replay():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=16000,input=True,output=True,
                   frames_per_buffer=1)
    my_buf=[]
    count=0
    while count<5:
        string_audio_data = stream.read(16000)
        my_buf.append(string_audio_data)
        count+=1
        print('.')
    print('ok')

    for buf in my_buf:
	stream.write(buf)

    stream.close()
    pa.terminate()

#record()
#audio()
#play()
replay()
