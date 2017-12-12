from sparkiConnection import *
import time
from math import cos, sin, sqrt
from scanParser import scanParser
import data
import random


resolution = 80
pi = 3.14159





def exploreEnv(exploreMap, res, scans):
	obs = []
	exploredMap = exploreMap[:][:]


	for [rx,ry,t,a,r] in scans:#grab each datapoint
		# convert the sensed obstacle to x and y
		# x values should range from -r to r
		# y values should range from 0 to 2r
		# rx *= 100
		# ry *= 100
		
		r = int(r)
		if (r == -1) or (r > 60): # infinity cases
			continue
			#r = 2*resolution
		
		#convert to radians for math
		t = (t)*pi/180 #our world is defined in bearing from north, this corrects cos and sin for that calculation
		a = a*pi/180


		x = rx + r*sin(t+a)
		y = ry+ r*cos(t+a)
		# this keeps track of where the walls are for later use
		obs.append([res+x,y])
		if (x > -res) and (x < res) and (y > 0) and (y < 2*res):
			exploredMap[int(y)][int(res+x)] = 2
		#this updates our map with free space we have found.
		for d in range(0,r-1): # 0<= d <r 
			
			x = rx + d*sin(t+a)
			y = ry + d*cos(t+a)
			
			x = int(x)
			y = int(y)
			if (x > -res) and (x < res) and (y > 0) and (y < 2*res):
				exploredMap[y][res+x] = 1
	return obs, exploredMap
		
def cleanMap(MapToClean):
	#generate a fresh map
	cleanedUpMap = [[0 for x in range(-resolution, resolution)] for y in range(0,2*resolution)] #2r * 2r map of what we have explored
	
	#for every square on the map
	for y in range(1, len(MapToClean)-1):
		for x in range(1, len(MapToClean)-1):
			
			#get value, and take a count of similar squares near it
			squareType = MapToClean[y][x]
			simNeighbors = 0
			
			for dy in [-1,0,1]:
				for dx in [-1,0,1]:
					#print(y+dy, x+dx)
					if MapToClean[y+dy][x+dx] == squareType:
						simNeighbors += 1
			
			#if there arent enought neighbors, keep it as unknown
			if simNeighbors > 2:
				cleanedUpMap[y][x] = squareType
	
	return cleanedUpMap

def growObs(mapToGrow, growthSize, depth=0):
	mapToPath = [[0 for x in range(-resolution, resolution)] for y in range(0,2*resolution)] #2r * 2r map of what we have explored
	if depth > growthSize:
		return mapToGrow
	
	for y in mapToPath:
		for x in y:
			if mapToPath[y][x] == 2:
				try:
					mapToPath[y-1][x-1] = 2
					mapToPath[y-1][x-0] = 2
					mapToPath[y-1][x+1] = 2
					
					mapToPath[y+0][x-1] = 2
					mapToPath[y+0][x+0] = 2
					mapToPath[y+0][x+1] = 2
					
					mapToPath[y+1][x-1] = 2
					mapToPath[y+1][x-0] = 2
					mapToPath[y+1][x+1] = 2
					
				except:
					print("out of bounds occured")
	return growObs(mapToPath, growthSize, depth+1)
	
	
def showMap(explored):
	print("="*2*resolution+'==')
	for row in [explored[len(explored)-1-i] for i in range(0, len(explored))]: 
		r='|'
		for char in row:
			if char == 0:#have not seen
				r += '.'
			if char == 1:#things is clear
				r += ' '
			if char == 2:#thinks is wall
				r += 'X'
		
		r+='|'
		print(r)
	print("="*2*resolution+'==')

def robotExplore(MapToMoveOn, botNumber, locations, botConnections):
	currentLocation = locations[botNumber] #[x, y]
	
	#xDistance = random.randint(0,10)
	#yDistance = random.randint(10,20)
	
	xDistance = 0
	yDistance = 10
	
	print(currentLocation)
	print(currentLocation[0]+xDistance, currentLocation[1]+yDistance)
	
	botConnections[botNumber].sendCommand(['move', currentLocation[0]+xDistance, currentLocation[1]+yDistance, 0])
	#botConnections[botNumber].sendCommand(['move', 0, 0.1, 0])
	
	botConnections[botNumber].sendCommand(['scan'])
	
	
	
	
#======================================================================#
# MAIN CODE STARTS HERE
#======================================================================#

#init new map, and empty scan data
explored = [[0 for x in range(-resolution, resolution)] for y in range(0,2*resolution)] #2r * 2r map of what we have explored
scans = []

#init robot connections
allBots = []
port = "/dev/cu.ArcBotics-DevB" 
baudrate = 9600 

try:
	#====MAC====
	#sparki1 = sparkiConnection("/dev/cu.ArcBotics-DevB", 9600) #port, baudrate

	#====WINDOWS====
	sparki1 = sparkiConnection("COM10", 9600) #port, baudrate
	sparki2 = sparkiConnection("COM12", 9600) #port, baudrate
except:
	print("a sparki failed to connect")

try:
	allBots.append(sparki1)
	allBots.append(sparki2)
except:
	print("a sparki failed to connect")

botLocations = []
for connected in allBots:
	botLocations.append([0, 0])
	
	
#start main loop
finished = False
count=0
while not finished:
	
	idle = True
	command = "No Command Read"
	for bot in allBots:
		if (bot.checkBuffer() > 2):
			idle = False
			
	if not idle:
		for botNum, bot in enumerate(allBots):
			if bot.checkBuffer() != 0:
				print(bot.checkBuffer())
				command = bot.receiveCommand() #this will wait until it has recieved a full command, then parse it and return it as a list
				print(command)
				
				
				
				
				
				# depending on what the command is, do something:
				# if robot is scanning, read the scan data
				if command[0] == 'scan':
					scans.append(command[1:])
					botLocations[botNum] = [command[1], command[2]]
					print(botLocations)
					
				# if robot is idle, make it explore
				if command[0] == 'Idle':
					#explored = cleanMap(explored)
					showMap(explored)
					
					#send the bot to explore
					robotExplore(explored, botNum, botLocations, allBots)
					
					idle = True
					
				# if robot needs help make the other one come
				if command[0] == 'help':
					print("not yet implemented")
			
		
		
		
		
		#since something changed, we are going to do something with the information
		o, explored = exploreEnv(explored, resolution, scans)
		
		#for obs in o:
		#	print(int(obs[0])-80, int(obs[1]), sqrt((int(obs[0])-80)*(int(obs[0])) + obs[1]*obs[1]))
		#if count%1 == 0:
		#	showMap(explored)
		#print(str(count) + ": COMMAND NAME GOES HERE" )
		count+=1
		print("looping... {}".format(count))
		
	else:
		print("idle...... {}".format(count))
		time.sleep(1)

###TODO

# Exploration
	#look at unexplored areas and try to path robots into them
# Planning
	#dijk only through explored -- just treat unexplored as blocked areas

	
#sparki needs help case
#initalize positions cases



























