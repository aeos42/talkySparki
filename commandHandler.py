'''
purpose: a two-way command handling layer that provides command encoding
and decoding for serial communicatin to sparki
'''


class serialLayer:

	def __init__(self, port):

		self.port = port

	def sendCommand(self, command):

		print("command")

