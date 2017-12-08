import numpy as np

myList = [0,1,2,3,4]

myMap = [[0, 1, 2, 3, 4 ],
	     [5, 6, 7, 8, 9 ],
	     [10,11,12,13,15],
	     [16,17,18,19,20]]




startCoords = [0,0]

endCoords = [3,2]

for y in range(startCoords[1], endCoords[1]):
	for x in range(startCoords[0], endCoords[0]):
		print(myMap[x][y])

