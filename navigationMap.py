'''
navigation map class -- uses the sensor data map to generate a navigable space map for sparki to move
sensor map is 200 * 200
'''

import math
from enum import Enum
from collections import deque
import time

sampleMap = [[0, 0, 0, 0, 0, 0],
             [1, 1, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0],
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
        print("node")


class NavigationMap:

    def __init__(self, navMap):
        self.deck = deque()
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

        print('hi')


    def addValidNeighbors(self, row, col):
        #these are row & column shifts that define geographic adjacency
        rShifts = (-1, -1, 0, 1, 1, 1, 0, -1)
        cShifts = (0, 1, 1, 1, 0, -1, -1, -1)

        for i in range(0, len(rShifts)):
            neighborLoc = [row + rShifts[i], col + cShifts[i]]

            if self.isValidIndices(neighborLoc):
                if self.graph[neighborLoc[0]][neighborLoc[1]] is not None:
                    self.setNodesAdjacent(self.graph[row][col], self.graph[neighborLoc[0]][neighborLoc[1]])


    def setNodesAdjacent(self, nodeA, nodeB):
        nodeA.adjacent.append(nodeB)


    def isValidIndices(self, indices):
        for index in indices:
            if ((index >= 2*accuracy) or (index < 0)):
                return False
        return True


    # takes in the ARRAY locations for each robot
    # each robot[num]Loc is a two-member list [R,C] for robot location map[R][C]
    def findPaths(self, robotOneLoc, navMap):

        rShifts =      ( -1,-1, 0, 1, 1, 1, 0,-1)
        cShifts =      (  0, 1, 1, 1, 0,-1,-1,-1)
        shiftMeaning = ('up', 'upRight', 'right', 'downRight', 'down', 'downLeft', 'left', 'upLeft')

        self.deck.append(mapNode(robotOneLoc, 'none'))

        while (len(self.deck) > 0):


            currentNode = self.deck.pop()
            currentNode.checked = True
            currentNode.printNode()


            neighbors = []

            for i in range(0, len(rShifts)):
                shiftedIndices = [currentNode.indices[0] + rShifts[i], currentNode.indices[1] + cShifts[i]]
                nodeIndices = self.returnValidNeighbor(shiftedIndices)

                if nodeIndices:
                    neighbors.append(mapNode(nodeIndices, shiftMeaning[i]))

            for node in neighbors:
                if self.isFree(node.indices, navMap):
                    node.parent = currentNode

                    #prioritizes straight directions by jumping the line
                    if (currentNode.direction == node.direction):
                        self.deck.appendleft(node)
                    else:
                        self.deck.append(node)

            time.sleep(1)


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