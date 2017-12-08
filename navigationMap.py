'''
navigation map class -- uses the sensor data map to generate a navigable space map for sparki to move
sensor map is 200 * 200

'''
import math

class navBlock:

    def __init__(self, startCoords, endCoords, mapID):
        self.startCoords = startCoords
        self.endCoords = endCoords
        self.visited = False
        self.clear = False
        self.exploreID = None
        self.mapID = mapID
        self.neighbors = []


class navigationMap:

    #sensor map is size (accuracy, accuracy)
    def __init__(self, blockSize, accuracy):
        self.blockList = []

        #block assignment and initiation

        numBlocks = math.ceil(accuracy/blockSize)

        for i in range(0, numBlocks):
            for j in range(0, numBlocks):
                self.blockList.append(navBlock())


    def assignPaths(self, robots):
        print('stub')

    def findPaths(self):
        print('stub')


