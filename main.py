from sparkiConnection import *
import time
from math import cos, sin
from scanParser import scanParser
import data


resolution = 100
pi = 3.14159





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

#init new map, and empty scan data
explored = [[0 for x in range(-resolution, resolution)] for y in range(0,2*resolution)] #2r * 2r map of what we have explored
scans = []

#init robot connections
allBots = []

sparki1 = sparkiConnection("/dev/cu.ArcBotics-DevB", 9600) #port, baudrate
allBots.append(sparki1)


#start main loop
finished = False
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
				command = bot.receiveCommand() #this will wait until it has recieved a full command, then parse it and return it as a list
				print(command)
				
				
				
				
				
				# depending on what the command is, do something:
				# if robot is scanning, read the scan data
				# if robot is idle, make it explore
				# if robot needs help make the other one come
				
				
				
				
				
		
		
		
		#since something changed, we are going to do something with the information
		o, explored = exploreEnv(explored, resolution, scans)
		
		#showMap(explored)
		#print(str(count) + ": COMMAND NAME GOES HERE" )
		count+=1
		print("looping... {}".format(count))
	else:
		print("idle...... {}".format(count))
	
	time.sleep(1)








#TODO
#2 maps, obstacles & fog of war


#dijk
#integrate scanning code

#Planning
	#look at unexplored areas and try to path robots into them
	#dijk only through explored


