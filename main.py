from sparkiConnection import *

import time
from math import cos, sin
from scanParser import scanParser

resolution = 40
pi = 3.14159




#should read data in as: [X,Y,theta, alpha, range]
#test data:
exScans = [	[0,0,90*pi/180,-30*pi/180, 10], #90 degrees from north aligns with the positive x axis
			[0,0,90*pi/180,-20*pi/180, 10],
			[0,0,90*pi/180,-10*pi/180, 10],
			[0,0,90*pi/180,-00*pi/180, 10],
			[0,0,90*pi/180,10*pi/180, 10],
			[0,0,90*pi/180,20*pi/180, 10],
			[0,0,90*pi/180,30*pi/180, 10],
			
			[0,0,15*pi/180,-30*pi/180, 5],
			[0,0,15*pi/180,-20*pi/180, 5],
			[0,0,15*pi/180,-10*pi/180, 5],
			[0,0,15*pi/180,00*pi/180, 5],
			[0,0,15*pi/180,10*pi/180, 5],
			[0,0,15*pi/180,20*pi/180, 5],
			[0,0,15*pi/180,30*pi/180, 5],
			
			[0,5,-15*pi/180,-30*pi/180, 5],
			[0,5,-15*pi/180,-20*pi/180, 5],
			[0,5,-15*pi/180,-10*pi/180, 5],
			[0,5,-15*pi/180,00*pi/180, 5],
			[0,5,-15*pi/180,10*pi/180, 5],
			[0,5,-15*pi/180,20*pi/180, 5],
			[0,5,-15*pi/180,30*pi/180, 5],
			]




#TODO read from sparki
#scans=[]
# scans += scanParser(BTtoString)




#convert scans into real world XY
def scansToMap(scans):
	realPoints = []
	for [rx,ry,t,a,r] in scans:#grab each datapoint
		#convert to x and y
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

		if (r == -1) or (r > 2*res): # infinity cases
			r = 2*res

		#convert to radians for math
		t = (90+t)*pi/180 #our world is defined in bearing from north, this corrects cos and sin for that calculation
		a = a*pi/180

		x = rx + r*cos(t+a)
		y = ry+ r*sin(t+a)
		# this keeps track of where the walls are for later use
		obs.append([res+x,y])

		#this updates our map with free space we have found.
		for d in range(0,r): # 0<= d <r 
			
			x = rx + d*cos(t+a)
			y = ry + d*sin(t+a)
			
			x = int(x)
			y = int(y)
			if (x > -res) and (x < res) and (y > 0) and (y < 2*res):
				exploredMap[y][res+x] = 1
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

explored = [[0 for x in range(-resolution, resolution)] for y in range(0,2*resolution)] #2r * 2r map of what we have explored

finished = False
scans = []

allBots = []

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
				
				#depending on what the command is, do something
				#scans.append(command)
				#
		
		
		#since something changed, we are going to do something with the information
		o, explored = exploreEnv(explored, resolution, scans)
		
		showMap(explored)
		print(str(count) + ": COMMAND NAME GOES HERE" ))
		count+=1
	
	time.sleep(1)
	








#TODO
#2 maps, obstacles & fog of war


#dijk
#integrate scanning code

#Planning
	#look at unexplored areas and try to path robots into them
	#dijk only through explored


















