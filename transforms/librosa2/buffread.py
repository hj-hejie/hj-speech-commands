from audioread import *
from audioread.rawread import *
import audioop

class RawAudioBuff(RawAudioFile):

	def __init__(self, buff):
		self.buff=buff

	def read_data(self):
		yield self.buff

	def close(self):
		pass

	@property
	def channels(self):
		return 1

	@property
	def samplerate(self):
		return 10000
	
