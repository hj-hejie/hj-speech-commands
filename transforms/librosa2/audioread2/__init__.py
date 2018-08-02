from audioread import *
from audioread.rawread import *
import wave
import audioop

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

		while True:
			data = self._file.readframes(block_samples)
			if not data:
				break
	
			data = audioop.lin2lin(data, old_width, TARGET_WIDTH)
			if self._needs_byteswap and self._file.getcomptype() != 'sowt':
				data = byteswap(data)
			yield data
	
def mic_open():
	return RawAudioMic()
