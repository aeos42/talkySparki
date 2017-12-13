from sparkiConnection import *
import time
from math import cos, sin, sqrt
from scanParser import scanParser
import data
import random


resolution = 80
pi = 3.14159






def exploreEnv(exploreMap, res, scans, visitedBotLocations):
	obs = []
	exploredMap = exploreMap[:][:]


	for [rx,ry,t,a,r] in scans:#grab each datapoint
		# convert the sensed obstacle to x and y
		# x values should range from -r to r
		# y values should range from 0 to 2r
		# rx *= 100
		# ry *= 100
		foundWall = True
		r = round(r)
		if (r == -1) or (r > 60): # infinity cases
			foundWall=False
			r = 60
			
		#convert to radians for math
		t = (t)*pi/180 #our world is defined in bearing from north, this corrects cos and sin for that calculation
		a = a*pi/180

		if foundWall:
			x = rx + r*sin(t+a)
			y = ry+ r*cos(t+a)
			# this keeps track of where the walls are for later use
			obs.append([res+x,y])
			if (x > -res) and (x < res) and (y > 0) and (y < 2*res):
				exploredMap[round(y)][round(res+x)] = 2
		
		#this updates our map with free space we have found.
		for d in range(0,r-1): # 0<= d <r 
			
			x = rx + d*sin(t+a)
			y = ry + d*cos(t+a)
			
			x = round(x)
			y = round(y)
			if (x > -res) and (x < res) and (y > 0) and (y < 2*res):
				exploredMap[y][res+x] = 1
		
	
	for [x,y] in visitedBotLocations:
		try:
			exploredMap[round(y)][round(res+x)] = 4
		except:
			None
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
	if depth >= growthSize:
		return mapToGrow
	
	for y in range(1, len(mapToPath)):
		for x in range(1, len(mapToPath)):
			if mapToGrow[y][x] == 1:
				mapToPath[y][x] = 1
			if mapToGrow[y][x] == 4:
				mapToPath[y][x] = 4
			
				
		for x in range(1, len(mapToPath)):	
			if mapToGrow[y][x] == 2:
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
			if char == 4:#thinks is a location sparki has visited
				r += 'S'
				
		
		r+='|'
		print(r)
	print("="*2*resolution+'==')

def robotExplore(MapToMoveOn, botNumber, locations, botConnections, visitedBotLocations):
	[curX, curY] = locations[botNumber] #[x, y]
	curX = round(curX)
	curY = round(curY)
	
	radius = 20
	
	possibleCoords = []
	#get all empty squares on the circle near the point
	for dx in range(-radius, radius+1):
		side2 = round(sqrt((radius*radius) - (dx*dx)))
		for dy in [side2, -side2]:
			
			try:
				if MapToMoveOn[curY+dy][resolution+curX+dx] == 1:#if the point at the radius is clear
					if [curX+dx, curY+dy] not in possibleCoords:
						possibleCoords.append([curX+dx, curY+dy])
			except:
				None
				
	
	#dont go near any other previously explored places
	
	for i, point in enumerate(possibleCoords):
		conflict = False
		for check in visitedBotLocations:
			if abs(point[0]-check[0])+abs(point[1]-check[1])  < radius * 3/4:
				try:
					possibleCoords.remove(point)
				except:
					None
	
	for i, point in enumerate(possibleCoords):
		conflict = False
		for check in possibleCoords[i:]:
			if abs(point[0]-check[0])+abs(point[1]-check[1])  < radius * 3/4:
				possibleCoords.remove(check)
			
				
		
	for point in possibleCoords:
		print(point)
	try:
		pick = random.randint(0,len(possibleCoords)-1)
		nextPoint = possibleCoords[pick]
		botConnections[botNumber].sendCommand(['move', nextPoint[0], nextPoint[1], 0])
	except:
		botConnections[botNumber].sendCommand(['move', curX, curY, 90])
	
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
pastBotLocations=[[0,0]]
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
				command = bot.receiveCommand() #this will wait until it has recieved a full command, then parse it and return it as a list
				#print(command)
				
				
				
				
				
				# depending on what the command is, do something:
				# if robot is scanning, read the scan data
				if command[0] == 'scan':
					scans.append(command[1:])
					botLocations[botNum] = [command[1], command[2]]
					if [command[1], command[2]] not in pastBotLocations:
						pastBotLocations.append([command[1], command[2]])
					showMap(explored)
					
				# if robot is idle, make it explore
				if command[0] == 'Idle':
					
					showMap(explored)
					blobMap = growObs(cleanMap(explored),3)
					#blobMap is a version of the scan data that is blown out of true size in an effort to make sparki not get to close to the obstacles.
					showMap(blobMap)
					
					#send the bot to explore
					robotExplore(blobMap, botNum, botLocations, allBots, pastBotLocations)
					
					idle = True
					
				# if robot needs help make the other one come
				if command[0] == 'help':
					NeedsHelpBot = botNum
					
		#since something changed, we are going to do something with the information
		o, explored = exploreEnv(explored, resolution, scans, pastBotLocations)
		
		
		#for obs in o:
		#	print(int(obs[0])-80, int(obs[1]), sqrt((int(obs[0])-80)*(int(obs[0])) + obs[1]*obs[1]))
		#if count%1 == 0:
		#	showMap(explored)
		#print(str(count) + ": COMMAND NAME GOES HERE" )
		count+=1
		if count % 200 ==0:
			explored = cleanMap(explored)
			explored = cleanMap(explored)
			explored = cleanMap(explored)
			
		#print("looping... {}".format(count))
		
	else:
		#print("idle...... {}".format(count))
		time.sleep(0.1)

###TODO

# Exploration
	#look at unexplored areas and try to path robots into them
# Planning
	#dijk only through explored -- just treat unexplored as blocked areas

	
#sparki needs help case
#initalize positions cases



























