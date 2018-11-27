from audioread import *
from audioread.rawread import *
import audioop
from pyaudio import PyAudio,paInt16

class RawAudioMic(RawAudioFile):

	def __init__(self):
		pass

	def read_data(self):
		pa=PyAudio()
		stream=pa.open(format = paInt16,channels=1,rate=16000,input=True,frames_per_buffer=1)
		count=0
		while True:
			if count>=2:
				break
			print ('.'+str(count))
			data = stream.read(16000)
			count+=1
			data = audioop.lin2lin(data, pa.get_sample_size(paInt16), TARGET_WIDTH)
			yield data

	def close(self):
		pass

	@property
	def channels(self):
		return 1

	@property
	def samplerate(self):
		return 16000
