'''
purpose: a two-way command handling layer that provides command encoding
and decoding for serial communicatin to sparki
'''
import serial


class sparkiConnection:

	def __init__(self, port, baudrate):

		self.port = port
		self.baudrate = baudrate
		self.ser = serial.Serial(port, baudrate)
		
		if (self.ser.is_open):
			print("port is open at " + self.ser.name)

		else:
			print("error: port not opened")	


	#input: command in packet form (list)
	#output: serial send to Sparki
	def sendCommand(self, command):

		print("sendCommand stub")

		
	def checkBuffer(self):

		return (self.ser.in_waiting)

	#input: serial buffer
	#output: parsed
	def receiveCommand(self):
		
		print(str(self.ser.in_waiting) + " bytes in incoming buffer")
		received = self.ser.read(self.ser.in_waiting)

		toParse = received.decode('utf-8')

		print(toParse)


	def closeConnection(self):

		self.ser.close()








