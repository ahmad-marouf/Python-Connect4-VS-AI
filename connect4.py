import copy

# --------------------------- GAME CLASS ----------------------------------
class Node:
    insertedIndex = 0

    def __init__(self, state, parent, depth, key, turn):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.key = key
        self.turn = turn


        self.scoreAI = 0
        self.scorePlayer = 0

        self.potPointsAI = 0
        self.potPointsPlayer = 0
        self.potPrereq = 0

    
    def __eq__(self, other):
            return self.state is other.state

    # ------------------- CLASS METHODS FOR GAME STATE -------------------------
    def getCols(self):
        return [[row[p] for row in self.state]
                for p in range(cols)]

    def getRows(self):
        return self.state
    
    def getDiagonals(self):
        return [[self.state[rows - p + q - 1][q]
             for q in range(max(p-rows+1, 0), min(p+1, cols))]
            for p in range(rows + cols - 1)]

    def getAntiDiagonals(self):
        return [[self.state[p - q][q]
             for q in range(max(p-rows+1,0), min(p+1, cols))]
            for p in range(rows + cols - 1)]
    
    def printState(self):
        stateStr = ""
        stateStr += "----------------------\n"
        for row in self.state:
            stateStr += str(row) + "\n"
        stateStr += "----------------------\n"
        return stateStr

    def calcScores(self):
        directionalArrays = [self.getRows(), self.getCols(), self.getDiagonals(), self.getAntiDiagonals()]
        for group in directionalArrays:
            for array in group:
                countPlayer = 0
                countAI = 0
                if len(array) > 3:
                    # print(array)
                    for i in range(len(array)):
                        if array[i] == 1: 
                            countAI += 1
                            countPlayer = 0
                        elif array[i] == -1:
                            countAI = 0
                            countPlayer += 1
                        else:
                            countAI = 0
                            countPlayer = 0
                        # print(countPlayer)
                        if countAI > 3: 
                            self.scoreAI += 1
                        if countPlayer > 3: 
                            # print(array)
                            self.scorePlayer += 1


    # ------------------- HEURISTIC FUNCTIONS -------------------------
    def getAvailable(self, col):
        if col > 6:
            return -1
        for i in reversed(range(rows)):
            if self.state[i][col] == 0:
                return i
        return -1
    
    def potentialPointsCol(self, player):  # checks potential points in columns
        array = self.getCols()
        i = 0
        count = 0
        for row in array:
            if substring([player, player, player, player, player, player], row):
                i += 1
                continue
            elif substring([player, player, player, player, player], row):
                # print("index = ")
                # row.reverse()
                if self.state[abs(5 - substring([player, player, player, player, player], row))][i] != 0:
                    continue
                count = + 1000000
                # print([player, player, player, player, player])
                # print("--------------------\n")
                i += 1
                continue
            elif substring([player, player, player, player], row):
                # print("index = ")
                # row.reverse()
                if self.state[abs(5 - substring([player, player, player, player], row))][i] != 0:
                    continue
                # print(abs(5 - substring([player, player, player, player], row)), i)
                count = + 100000
                # print([player, player, player, player])
                # print("--------------------\n")
                i += 1
                continue
            elif substring([player, player, player], row):
                # print("index = ")
                # row.reverse()
                if self.state[abs(5 - substring([player, player, player], row))][i] != 0:
                    continue
                # print(abs(5 - substring([player, player, player], row)), i)
                count = + 100
                # print([player, player, player])
                # print("--------------------\n")
                i += 1
                continue
            elif substring([player, player], row):
                # print("index = ")
                # row.reverse()
                if self.state[abs(5 - substring([player, player], row))][i] != 0:
                    continue
                # print(abs(5 - substring([player, player], row)), i)
                count = + 1
                # print([player, player])
                # print("--------------------\n")
                i += 1
                continue
            i += 1

        if player == 1:
            self.potPointsAI += count * 50
        else:
            self.potPointsPlayer += count * 50
        return

    def potentialPointsRow(self, player):  # checks potential points in rows
        array = self.getRows()
        i = 0
        count = 0
        for row in array:
            if substring([player, player, player, player, player, player, player], row):
                continue
            elif substring([player, player, player, player, player, player], row):
                # print("index = ")
                # print(i, substring([player, player, player, player, player, player], row))
                if i > 6:
                    continue
                available = self.getAvailable(substring([player, player, player, player, player, player], row))
                if available:
                    if available == i:
                        count += 10000000
                    elif available < i:
                        count += 10 - i
                print([player, player, player, player, player])
                print("--------------------\n")
                i += 1
                break
            elif substring([player, player, player, player, player], row):
                # print("index = ")
                # print(i, substring([player, player, player, player, player], row))
                if i > 6:
                    continue
                available = self.getAvailable(substring([player, player, player, player, player], row))
                if available:
                    if available == i:
                        count += 1000000
                    elif available < i:
                        count += 10 - i
                # print([player, player, player, player, player])
                # print("--------------------\n")
                i += 1
                break
            elif substring([player, player, player, player], row):
                # print("index = ")
                # print(i, substring([player, player, player, player], row))
                if i > 6:
                    continue
                available = self.getAvailable(substring([player, player, player, player], row))
                if available:
                    if available == i:
                        count += 100000
                    elif available < i:
                        count += 10 - i
                # print([player, player, player, player])
                # print("--------------------\n")
                i += 1
                break
            elif substring([player, player, player], row):
                # print("index = ")
                # print(i, substring([player, player, player], row))
                if i > 6:
                    continue
                available = self.getAvailable(substring([player, player, player], row))
                if available:
                    if available == i:
                        count += 100
                    elif available < i:
                        count += 10 - i
                # print([player, player, player])
                # print("--------------------\n")
                i += 1
                break
            elif substring([player, player], row):
                # print("index = ")
                # print(i, substring([player,  player], row))
                if i > 6:
                    continue
                available = self.getAvailable(substring([player, player], row))
                if available:
                    if available == i:
                        count += 1
                    elif available < i:
                        count += 1 - i
                # print([player,  player])
                # print("--------------------\n")
                i += 1
                continue
            i += 1

        if player == 1:
            self.potPointsAI += count * 50
        else:
            self.potPointsPlayer += count * 50
        return

    
    def potScoresDiag(self):        # checks potential points in diagonals
        rowsGrp = self.getRows()
        colsGrp = self.getCols()
        diagsGrp = self.getDiagonals()
        adiagsGrp = self.getAntiDiagonals()
        directionalArrays = [rowsGrp, colsGrp, diagsGrp, adiagsGrp]
        for group in directionalArrays:
            
            for n, array in enumerate(group):
                countPlayer = 0
                countAI = 0
                totalInserts = 0
                countZeros = 0
                rowIndex = None
                colIndex = None
                insertIndex = None
                # numofInserts = 0
                if len(array) > 3:
                    # print(array)
                    for i in range(len(array)):
                        if array[i] == 1: 
                            countAI += 1
                            countPlayer = 0
                        elif array[i] == -1:
                            countAI = 0
                            countPlayer += 1
                        else:
                            totalInserts += 1
                            countZeros += 1
                            countPlayer += 1
                            countAI += 1
                            if group is rowsGrp:
                                rowIndex = n
                                colIndex = i
                            elif group is colsGrp:
                                rowIndex = i
                                colIndex = n
                            elif group is diagsGrp:
                                if n < rows:
                                    rowIndex = (rows-1) - n + i
                                    colIndex = i
                                else:
                                    rowIndex = i
                                    colIndex = i + (n-rows)
                            elif group is adiagsGrp:
                                if n < rows:
                                    rowIndex = n - i
                                    colIndex = i
                                else:
                                    rowIndex = (rows-1) - i
                                    colIndex = i + (n-rows+1)
                            insertIndex = self.getAvailable(colIndex)
                            if insertIndex != -1:
                                insertsNeeded = insertIndex - rowIndex
                                totalInserts += insertsNeeded
                        if insertIndex is not None:
                            if insertIndex < 3 and countAI == 0:
                                continue
                            if insertIndex < 3 and countPlayer == 0:
                                continue
                        if countAI-countZeros > 2: 
                            self.potPointsAI += countAI*5
                        elif countAI > 3:
                            self.potPointsAI += countAI*5 + countZeros - totalInserts
                        if countPlayer-countZeros > 2: 
                            self.potPointsPlayer += countPlayer*5
                        elif countPlayer > 3: 
                            self.potPointsPlayer += countPlayer*5 + countZeros - totalInserts
    
    def calcHeuristic(self):
        self.calcScores()
        # self.potentialPointsRow(1)
        # self.potentialPointsRow(-1)
        # self.potentialPointsCol(1)
        # self.potentialPointsCol(-1)
        self.potScoresDiag()
        self.key = (self.scoreAI*10 + self.potPointsAI) - (self.scorePlayer*10 + self.potPointsPlayer)
        return self.key

# --------------------------- GLOBAL VARIABLES -----------------------------
rows, cols = (6, 7) # Initialized length and width of game board
initState = Node([[0 for i in range(cols)] for j in range(rows)], None, 0, 0, -1) # Create 2d array with dimensions rows x cols filled with 0s

maxdepth = 1 # Maximum levels K tested by minimax determined by input
useAlphaBeta = 0
piecesInserted = 0

# --------------------------- GAME FUNCTIONS -----------------------------
def addPiece(node, column, turn):
    newNode = Node(copy.deepcopy(node.state), node, node.depth + 1, 0, turn)
    for i in reversed(range(rows)):
        if newNode.state[i][column] == 0:
            newNode.state[i][column] = turn
            newNode.insertedIndex = (i, column)
            newNode.calcHeuristic()
            return newNode
    return node # if column is full return original node

def getNeighbors(node, turn):
    neighbors = list()
    for col in range(cols):
        newNode = addPiece(node, col, turn)
        if newNode is not node: # check that column was not full
            neighbors.append(newNode)
    return neighbors

def substring(lst1, lst2):
        m = len(lst1)
        n = len(lst2)
        i = 0
        index = 0
        while i <= n - m:
            j = 0
            while j < m:
                if lst2[i + j] != lst1[j]:
                    index += 1
                    break
                j += 1
                if j == m:
                    return index + m
            i += 1
        return 0

# --------------------------- MAIN -----------------------------
# def initializeGame(maxD, useAB):
#     global maxdepth, useAlphaBeta
#     maxdepth = maxD
#     useAlphaBeta = useAB
#     playTurn(None)
#     pass

# def playTurn(node):
#     global piecesInserted
#     # node.printState()
#     # print(maxdepth)
#     if piecesInserted == 0:
#         node = initState

#     if (node.depth == 42):
#         print("done")
#         print("AI Score: ", node.scoreAI, "\tPlayer Score: ", node.scorePlayer)
#         return
    
#     if (node.turn == 1):
#         colIndex = int(input("Enter column number: "))
#         print("col selected is ", colIndex)
#         rowIndex = node.getAvailable(colIndex)
#         result = addPiece(node, colIndex, node.turn*-1)
#         piecesInserted += 1
#         result.printState()
#         playTurn(result)
#         # get input from user
#     else:
#         result = decision(node)
#         result.printState()
#         playTurn(result)


# playTurn(None)