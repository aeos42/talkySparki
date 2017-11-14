import serial
import time

ser = serial.Serial("/dev/cu.ArcBotics-DevB", 9600)

print(ser.name) 

if (ser.is_open):
	print("yeah port is open")


while True:
    bytesToRead = ser.inWaiting()
    data = ser.read(bytesToRead)
    print(data)
    time.sleep(1)

