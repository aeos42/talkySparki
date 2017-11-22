from sparkiConnection import sparkiConnection

import time




sparkiOne = sparkiConnection("/dev/tty.usbserial-DN02PLI7", 57600)

while True:


	if (sparkiOne.checkBuffer() > 0):

		print(sparkiOne.recieveCommand())

