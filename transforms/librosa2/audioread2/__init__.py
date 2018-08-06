from audioread import *
from audioread.rawread import *
import wave
import audioop
from pyaudio import PyAudio,paInt16

filename='/home/hejie/workspace/python/pytorch-speech-commands/datasets/speech_commands/train/bird/a045368c_nohash_0.wav'

class RawAudioMic(RawAudioFile):
	def __init__(self):
		try:
			self._fh = open(filename, 'rb')
			self._file = wave.open(self._fh)
		except wave.Error:
			self._fh.seek(0)
			pass
		else:
			self._needs_byteswap = False
			self._check()
			return
		# None of the three libraries could open the file.
		self._fh.close()
		raise UnsupportedError()

	def read_data(self, block_samples=1024):
		old_width = self._file.getsampwidth()
		pa=PyAudio()
		stream=pa.open(format = paInt16,channels=1,rate=16000,input=True,frames_per_buffer=1)
		count=0
		while True:
			if count>=1:
				break
			print '.'+str(count)
			data = stream.read(16000)
			count+=1
			data = audioop.lin2lin(data, old_width, TARGET_WIDTH)
			if self._needs_byteswap and self._file.getcomptype() != 'sowt':
				data = byteswap(data)
			yield data
	
def mic_open():
	return RawAudioMic()
