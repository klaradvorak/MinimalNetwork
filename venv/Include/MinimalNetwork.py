import numpy as np
import sys,os

# prints the entire numpy array
np.set_printoptions(threshold=sys.maxsize)

#Loads text file from the same directory as the script
#in case of manual address imput: filePath = "C:\\Users\\...\\p107_network.txt"
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
filePath = os.path.join(dirname, "p107_network.txt")
fileContent =  np.genfromtxt(filePath,delimiter=",")

edgesDict = {}
sourceNodeID = 0

#iterates throught all nodes
while sourceNodeID < (len(fileContent) -1):
    unmappedConnections = fileContent[sourceNodeID][sourceNodeID + 1:]
    connectedNodeID = sourceNodeID + 1

    #stores the value and source and connected node in dictionary for all edges
    for edge in unmappedConnections:
        if not np.isnan(edge):
            edge = int(edge)
            edgesDict[(sourceNodeID, connectedNodeID)] = edge
        connectedNodeID += 1
    sourceNodeID += 1

#find subset of i
def getParent(parent, i):
    if parent[i] == -1:
        return i
    if parent != -1:
        return getParent(parent, parent[i])

#join two subsets
def setParent(parent, x,y):
    xSet = getParent(parent, x)
    ySet = getParent(parent, y)
    parent[xSet] = ySet

#find lowest non cyclic edges
def isCycle():
    numberOfFoundEdges = 0
    #fills list with -1
    parent = [-1] * len(fileContent)

    #iterate through all edges starting with the one with smallest value
    for i, j in sortedEdgesDict.keys():
        x = getParent(parent, i)
        y = getParent(parent, j)

        # if no cycle
        if x != y:
            setParent(parent, x, y)
            #adds edge to new matrix
            minimalMatrix[i][j] = sortedEdgesDict[(i,j)]
            minimalMatrix[j][i] = sortedEdgesDict[(i, j)]

            # checkes if all the non cyclic edges are found if they are ends the search
            if numberOfFoundEdges == (len(fileContent)-1):
                print("All edges are found")
                return True

            #adds one to the total number of found non cyclic edges
            numberOfFoundEdges += 1



#sortes all edges from smallest to highest
sortedEdgesDict = dict(sorted(edgesDict.items(), key = lambda kv:(kv[1], kv[0])))

#initialize new 2d array and fill it with zeros
minimalMatrix = np.zeros((len(fileContent), len(fileContent)))

isCycle()

#calculation of the saved distance
sumOfMinMatrix = sum(minimalMatrix)
savedDistance = int (np.nansum(fileContent)/2 - sum(sumOfMinMatrix)/2 )
print(savedDistance)