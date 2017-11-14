

from math import cos, sin
resolution = 15
pi = 3.14159

#should read data in as: [X,Y,theta, alpha, range]
#test data:
scans = [	[0,0,90*pi/180,-30*pi/180, 10], #90 degrees from north aligns with the positive x axis
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
def showMap(points):
	worldMap = [['.' for x in range(-resolution, resolution+1)] for y in range(-resolution, resolution+1)]
	for [x,y] in points:
		worldMap[resolution+x][resolution+y] = 'O'   #O for obstacle
	for row in [worldMap[len(worldMap)-1-i] for i in range(0, len(worldMap))]: 
		r='|'
		for char in row:
			r += char
		r+='|'
		print(r)


r1 = scansToReal(scans[0:7])
showMap(r1)

r2 = scansToReal(scans[8:14])
showMap(r2)

showMap(r1+r2)











