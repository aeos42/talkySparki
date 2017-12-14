'''
navigation map class -- uses the sensor data map to generate a navigable space map for sparki to move
sensor map is 200 * 200
'''

import math

import queue
import time

sampleMap = [[0, 0, 0, 0, 0, 0],
             [1, 1, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 1, 1],
             [0, 0, 0, 0, 0, 0],
             [1, 1, 1, 0, 0, 0],
             ]
accuracy = 3


class mapNode:

    def __init__(self, indices, dir):
        self.indices = indices
        self.checked = False
        self.adjacent = []
        self.parent = None
        self.direction = dir

    def printNode(self):
        print("node" + str(self.indices))


class NavigationMap:

    def __init__(self, navMap):
        self.queue = queue.Queue()
        self.tree = {}
        self.navMap = navMap
        self.graph = [[None for x in range(0, len(navMap))] for y in range(0, len(navMap[0]))]


    def buildGraph(self):
        #reads in the map, and if clear in navMap, add to the graph
        for i in range(0, len(self.navMap)):
            for j in range(0, len(self.navMap[i])):
                if (self.navMap[i][j] == 0):
                    self.graph[i][j] = mapNode([i,j], None)

        #for each node sent to the graph, checks geographic neighbors and marks them as adjacent
        for i in range(0, len(self.graph)):
            for j in range(0, len(self.graph[i])):
                if self.graph[i][j] is not None:
                    self.addValidNeighbors(i, j)


    def addValidNeighbors(self, row, col):
        #these are row & column shifts that define geographic adjacency
        rShifts = (-1, -1, 0, 1, 1, 1, 0, -1)
        cShifts = (0, 1, 1, 1, 0, -1, -1, -1)
        shiftMeaning = ('up', 'upRight', 'right', 'downRight', 'down', 'downLeft', 'left', 'upLeft')

        for i in range(0, len(rShifts)):
            if(shiftMeaning[i] == 'up'):
                j = 1
                while self.isValidIndices([row-j, col]):
                    neighborLoc = [row-j, col]
                    if self.graph[neighborLoc[0]][neighborLoc[1]] is not None:
                        self.setNodesAdjacent(self.graph[row][col], self.graph[neighborLoc[0]][neighborLoc[1]], shiftMeaning[i])
                    else:
                        break
                    j += 1

            elif(shiftMeaning[i] == 'down'):
                j = 1
                while self.isValidIndices([row + j, col]):
                    neighborLoc = [row + j, col]
                    if self.graph[neighborLoc[0]][neighborLoc[1]] is not None:
                        self.setNodesAdjacent(self.graph[row][col], self.graph[neighborLoc[0]][neighborLoc[1]], shiftMeaning[i])
                    else:
                        break
                    j += 1

            elif(shiftMeaning[i] == 'left'):
                j = 1
                while self.isValidIndices([row, col - j]):
                    neighborLoc = [row, col - j]
                    if self.graph[neighborLoc[0]][neighborLoc[1]] is not None:
                        self.setNodesAdjacent(self.graph[row][col], self.graph[neighborLoc[0]][neighborLoc[1]], shiftMeaning[i])
                    else:
                        break
                    j += 1

            elif(shiftMeaning[i] == 'right'):
                j = 1
                while self.isValidIndices([row, col + j]):
                    neighborLoc = [row, col + j]
                    if self.graph[neighborLoc[0]][neighborLoc[1]] is not None:
                        self.setNodesAdjacent(self.graph[row][col], self.graph[neighborLoc[0]][neighborLoc[1]], shiftMeaning[i])
                    else:
                        break
                    j += 1

            elif(shiftMeaning[i] == 'upRight'):
                j = 1
                while self.isValidIndices([row - j, col + j]):
                    neighborLoc = [row - j, col + j]
                    if self.graph[neighborLoc[0]][neighborLoc[1]] is not None:
                        self.setNodesAdjacent(self.graph[row][col], self.graph[neighborLoc[0]][neighborLoc[1]], shiftMeaning[i])
                    else:
                        break
                    j += 1

            elif(shiftMeaning[i] == 'upLeft'):
                j = 1
                while self.isValidIndices([row - j, col - j]):
                    neighborLoc = [row - j, col - j]
                    if self.graph[neighborLoc[0]][neighborLoc[1]] is not None:
                        self.setNodesAdjacent(self.graph[row][col], self.graph[neighborLoc[0]][neighborLoc[1]], shiftMeaning[i])
                    else:
                        break
                    j += 1

            elif(shiftMeaning[i] == 'downRight'):
                j = 1
                while self.isValidIndices([row + j, col + j]):
                    neighborLoc = [row + j, col + j]
                    if self.graph[neighborLoc[0]][neighborLoc[1]] is not None:
                        self.setNodesAdjacent(self.graph[row][col], self.graph[neighborLoc[0]][neighborLoc[1]], shiftMeaning[i])
                    else:
                        break
                    j += 1

            elif(shiftMeaning[i] == 'downLeft'):
                j = 1
                while self.isValidIndices([row + j, col - j]):
                    neighborLoc = [row + j, col - j]
                    if self.graph[neighborLoc[0]][neighborLoc[1]] is not None:
                        self.setNodesAdjacent(self.graph[row][col], self.graph[neighborLoc[0]][neighborLoc[1]],
                                              shiftMeaning[i])
                    else:
                        break
                    j += 1


    def setNodesAdjacent(self, nodeA, nodeB, Dir):
        nodeA.adjacent.append((nodeB, Dir))


    def isValidIndices(self, indices):
        for index in indices:
            if ((index >= 2*accuracy) or (index < 0)):
                return False
        return True


    # takes in the ARRAY locations for each robot
    # each robot[num]Loc is a two-member list [R,C] for robot location map[R][C]
    def findPaths(self, robotOneLoc):

        firstNode = self.graph[robotOneLoc[0]][robotOneLoc[1]]
        firstNode.checked = True
        self.queue.put(firstNode)

        while (not self.queue.empty()):
            currentNode = self.queue.get()


            for node in currentNode.adjacent:
                if not node[0].checked:
                    node[0].parent = currentNode
                    node[0].checked = True
                    self.queue.put(node[0])

        print('debug')


    def retrievePath(self, goalIndices):

        node = self.graph[goalIndices[0]][goalIndices[1]]
        indexList = []

        while node.parent is not None:
            indexList.append([node.indices[0], node.indices[1]])
            node = node.parent

        return indexList


    def returnValidNeighbor(self, indices):
        for index in indices:
            if ((index >= 2*accuracy) or (index < 0)):
                return False
        return indices


    def isFree(self, indices, navMap):
        if (navMap[indices[0]][indices[1]] == 0):
            return True
        return False

    def arrayIndexToCoords(self, indices):
        return [indices[1] - accuracy, indices[0]]

    def coordsToArrayIndex(self, coords):
        return [coords[1], coords[0] + accuracy]



myMap = NavigationMap(sampleMap)

myMap.buildGraph()

myMap.findPaths([5,5])

print(myMap.retrievePath([0,0]))