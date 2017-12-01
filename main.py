from sparkiConnection import *

import time
from math import cos, sin
from scanParser import scanParser

resolution = 100
pi = 3.14159

testScans = [ 	[0.0, 10.0, 0.0, 35.0, 73.0],
				[0.0, 10.0, 0.0, 50.0, 89.0],
				[0.0, 10.0, 0.0, 65.0, 88.0],
				[0.0, 10.0, 0.0, 80.0, 15.0],
				[0.0, 20.0, 0.0, -85.0, 59.0],
				[0.0, 20.0, 0.0, -70.0, 15.0],
				[0.0, 20.0, 0.0, -55.0, 19.0],
				[0.0, 20.0, 0.0, -40.0, 78.0],
				[0.0, 20.0, 0.0, -25.0, 66.0],
				[0.0, 20.0, 0.0, -10.0, 59.0],
				[0.0, 20.0, 0.0, 5.0, 57.0],
				[0.0, 20.0, 0.0, 20.0, 223.0],
				[0.0, 20.0, 0.0, 35.0, -1.0],
				[0.0, 20.0, 0.0, 50.0, 70.0],
				[0.0, 20.0, 0.0, 65.0, 71.0],
				[0.0, 20.0, 0.0, 80.0, 82.0],
				[0.0, 30.0, 0.0, -85.0, 49.0],
				[0.0, 30.0, 0.0, -70.0, 15.0],
				[0.0, 30.0, 0.0, -55.0, 78.0],
				[0.0, 30.0, 0.0, -40.0, 81.0],
				[0.0, 30.0, 0.0, -25.0, 338.0],
				[0.0, 30.0, 0.0, -10.0, 50.0],
				[0.0, 30.0, 0.0, 5.0, 49.0],
				[0.0, 30.0, 0.0, 20.0, 46.0],
				[0.0, 30.0, 0.0, 35.0, 243.0],
				[0.0, 30.0, 0.0, 50.0, 240.0],
				[0.0, 30.0, 0.0, 65.0, 212.0],
				[0.0, 30.0, 0.0, 80.0, 75.0],
				[0.0, 40.0, 0.0, -85.0, 39.0],
				[0.0, 40.0, 0.0, -70.0, 16.0],
				[0.0, 40.0, 0.0, -55.0, 48.0],
				[0.0, 40.0, 0.0, -40.0, 85.0],
				[0.0, 40.0, 0.0, -25.0, 49.0],
				[0.0, 40.0, 0.0, -10.0, 40.0],
				[0.0, 40.0, 0.0, 5.0, 40.0],
				[0.0, 40.0, 0.0, 20.0, 38.0],
				[0.0, 40.0, 0.0, 35.0, 42.0],
				[0.0, 40.0, 0.0, 50.0, 43.0],
				[0.0, 40.0, 0.0, 65.0, 45.0],
				[0.0, 40.0, 0.0, 80.0, 19.0],
				[0.0, 50.0, 0.0, -85.0, -1.0],
				[0.0, 50.0, 0.0, -70.0, 17.0]
			]


#should read data in as: [X,Y,theta, alpha, range]
#test data:
exScans = [	[0,0,90,-30, 10], #90 degrees from north aligns with the positive x axis
			[0,0,90,-20, 10],
			[0,0,90,-10, 10],
			[0,0,90,-00, 10],
			[0,0,90,10, 10],
			[0,0,90,20, 10],
			[0,0,90,30, 10],
			
			[0,0,15,-30, 5],
			[0,0,15,-20, 5],
			[0,0,15,-10, 5],
			[0,0,15,00, 5],
			[0,0,15,10, 5],
			[0,0,15,20, 5],
			[0,0,15,30, 5],
			
			[0,5,-15,-30, 5],
			[0,5,-15,-20, 5],
			[0,5,-15,-10, 5],
			[0,5,-15,00, 5],
			[0,5,-15,10, 5],
			[0,5,-15,20, 5],
			[0,5,-15,30, 5],
			]




#TODO read from sparki
#scans=[]
# scans += scanParser(BTtoString)




#convert scans into real world XY
def scansToMap(scans):
	realPoints = []
	for [rx,ry,t,a,r] in scans:#grab each datapoint
		#convert to x and y
		t = t*pi/180
		a = 1*pi/180
		x = rx + r*cos(t+a)
		y = ry+ r*sin(t+a)
		realPoints.append([int(x+.5),int(y+.5)])
	return realPoints


#r1 = scansToMap(scans[0:7])
#r2 = scansToMap(scans[8:])



def exploreEnv(exploreMap, res, scans):
	obs = []
	exploredMap = exploreMap[:][:]

		

	
	for [rx,ry,t,a,r] in scans:#grab each datapoint
		# convert the sensed obstacle to x and y
		# x values should range from -r to r
		# y values should range from 0 to 2r
		
		r = int(r)

		x = rx + r*cos(t+a)
		y = ry+ r*sin(t+a)
		obs.append([res+x,y])
		
		for d in range(0,r): # 0<= d <r 
			
			x = rx + d*cos(t+a)
			y = ry + d*sin(t+a)
			
			
			
			exploredMap[int(y)][int(res+x)] = 1
	return obs, exploredMap
		


def showMap(explored):
	print("="*2*resolution+'==')
	for row in [explored[len(explored)-1-i] for i in range(0, len(explored))]: 
		r='|'
		for char in row:
			if char == 0:
				r += '0'
			if char == 1:
				r += '.'
		r+='|'
		print(r)
	print("="*2*resolution+'==')










#======================================================================#
# MAIN CODE STARTS HERE
#======================================================================#
resolution = 40

explored = [[0 for x in range(-resolution, resolution)] for y in range(0,2*resolution)] #2r * 2r map of what we have explored

finished = False
scans = []

allBots = []
port = "/dev/cu.ArcBotics-DevB" 
baudrate = 9600 



s1 = sparkiConnection(port, baudrate)
allBots.append(s1)


count=0
while not finished:
	
	idle = True
	command = "No Command Read"
	for bot in allBots:
		if (bot.checkBuffer() > 0):
			idle = False
			
	if not idle:
		for bot in allBots:
			if bot.checkBuffer() != 0:
				command = bot.receiveCommand() #this will wait until it has recieved a full command, then parse it and return it
				print(command)
				
				#depending on what the command is, do something
				#scans.append(command)
				#
		
		
		#since something changed, we are going to do something with the information
		o, explored = exploreEnv(explored, resolution, scans)
		
		#showMap(explored)
		#print(str(count) + ": COMMAND NAME GOES HERE" )
		count+=1
	
	time.sleep(1)
	








#TODO
#2 maps, obstacles & fog of war


#dijk
#integrate scanning code

#Planning
	#look at unexplored areas and try to path robots into them
	#dijk only through explored


















