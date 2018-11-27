from audioread import *
from audioread.rawread import *
import audioop

class RawAudioBuff(RawAudioFile):

	def __init__(self, buff):
		self.buff=buff

	def read_data(self):
		for count in range(2):
			print ('.'+str(count))
			yield self.buff[count]

	def close(self):
		pass

	@property
	def channels(self):
		return 1

	@property
	def samplerate(self):
		return 10000
	
