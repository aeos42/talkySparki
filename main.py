from math import cos, sin
from scanParser import scanParser

resolution = 20
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
			
			[5,5,-15*pi/180,-30*pi/180, 5],
			[5,5,-15*pi/180,-20*pi/180, 5],
			[5,5,-15*pi/180,-10*pi/180, 5],
			[5,5,-15*pi/180,00*pi/180, 5],
			[5,5,-15*pi/180,10*pi/180, 5],
			[5,5,-15*pi/180,20*pi/180, 5],
			[5,5,-15*pi/180,30*pi/180, 5],
			]
scans = exampleScans




#TODO read from sparki
#scans=[]
# scans += scanParser(BTtoString)




#convert scans into real world XY
def scansToReal(scans):
	realPoints = []
	for [rx,ry,t,a,r] in scans:#grab each datapoint
		#convert to x and y
		x = rx + r*cos(t+a)
		y = ry+ r*sin(t+a)
		realPoints.append([int(x+.5),int(y+.5)])
	return realPoints


#convert points to a map for display
def showMap(points, x1, y1, x2, y2):#(list of obstacles, s1x, s1y, s2x, s2y)
	worldMap = [['.' for x in range(-resolution, resolution+1)] for y in range(-resolution, resolution+1)]
	for [x,y] in points:
		worldMap[resolution+x][resolution+y] = 'O'   #O for obstacle
	worldMap[resolution+x1][resolution+y1]="1"
	worldMap[resolution+x2][resolution+y2]="2"

	print("=========================================")
	for row in [worldMap[len(worldMap)-1-i] for i in range(0, len(worldMap))]: 
		r='|'
		for char in row:
			r += char
		r+='|'
		print(r)
	print("=========================================")

r1 = scansToReal(scans[0:7])
#showMap(r1, 0, 0, 5, 5)

r2 = scansToReal(scans[8:])
#showMap(r2, 0, 0, 5, 5)

#showMap(r1+r2, 0, 0, 5, 5)


r = resolution
explored = [[0 for x in range(-r, r)] for y in range(0,2*r)] #2r * 2r map of what we have explored


def exploreEnv(exploreMap, res, scans):
	obs = []
	exploredMap = exploreMap[:][:]
	
	for [rx,ry,t,a,r] in scans:#grab each datapoint
		#convert the sensed obstacle to x and y
		x = rx + r*cos(t+a)
		y = ry+ r*sin(t+a)
		obs.append([res+x,y])
		
		for d in range(0,r):
			x = rx + d*cos(t+a)
			y = ry + d*sin(t+a)
			
			exploredMap[int(res+x)][int(y)] = 1
	return obs, exploredMap
		

o, explored = exploreEnv(explored, r, scans)


print("=========================================")
for row in [explored[len(explored)-1-i] for i in range(0, len(explored))]: 
	r='|'
	for char in row:
		r += str(char)
	r+='|'
	print(r)
print("=========================================")









#TODO

#2 maps, obstacles & fog of war


#dijk
#integrate scanning code

#Planning
	#look at unexplored areas and try to path robots into them
	#dijk only through explored
