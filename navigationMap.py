'''
navigation map class -- uses the sensor data map to generate a navigable space map for sparki to move
sensor map is 200 * 200

'''
import math

class navBlock:

    def __init__(self, startIndex, endIndex, mapID):
        self.startIndex = startIndex
        self.endIndex = endIndex
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

        numBlocks = int(math.ceil(accuracy/blockSize))

        print(numBlocks)

        totalIter = 0

        for i in range(0, numBlocks):
            for j in range(0, numBlocks):

                startIndex = [i*blockSize,j*blockSize]
                endIndex = [i*blockSize+(blockSize-1), j*blockSize+(blockSize-1)]

                self.blockList.append(navBlock(startIndex, endIndex, totalIter))
                totalIter += 1

        for block in self.blockList:
            print('start: ' + str(block.startIndex) + 'end: ' + str(block.endIndex) + 'for block num: ' + str(block.mapID))


    def assignPaths(self, robots):
        print('stub')

    def findPaths(self):
        print('stub')


