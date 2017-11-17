from commandHandler import serialLayer
import serial
import time



ser = serial.Serial("/dev/tty.usbserial-DN02PLI7", 57600)

if (ser.is_open):
	print("port is open at " + ser.name)


while True:

	command = input('enter command: ')

	sampleCommand = command.encode('utf-8')

	ret = ser.write(sampleCommand)

	print(str(ret) + " bytes sent")

	#time.sleep(1)

	howMuch = ser.in_waiting
	print(str(howMuch) + " bytes in incoming buffer")


	bytesBack = ser.read(ser.in_waiting)
	print(bytesBack.decode('utf-8'))

'''
while True:
    bytesToRead = ser.inWaiting()
    data = ser.read(bytesToRead)
    print(data)
    time.sleep(1)

'''