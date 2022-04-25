import threading
import math
import timeit
from queue import Queue
from tkinter import *
from tkinter import font
from connect4 import maxdepth, piecesInserted, rows, cols, getNeighbors, initState, addPiece

# --------------------------------- Algorithm Functions ----------------------------------------
def terminal_state(node):
    global maxdepth, piecesInserted
    guiProgram.nodesExpanded += 1
    if node.depth == piecesInserted + maxdepth:
        guiProgram.treeStr += str(node.key) + " "
        # guiProgram.treeStr += node.printState() + " "
        # print(node.key, end=" ")
        return True
    if node.depth == rows*cols:
        return True
    else:
        guiProgram.treeStr += "Depth: " + str(node.depth-piecesInserted) + "\t" + "expanding: " + str(node.key) + "\n"
        # guiProgram.treeStr += "Depth: " + str(node.depth-piecesInserted) + "\t" + "expanding:\n" + node.printState() + ""
        # print("Depth: ", str(node.depth-piecesInserted), "\t", "expanding: ", str(node.key))
        return False

def maximize(node):
    if terminal_state(node):
        return (None,node.key)
    (max_node,max_score) = (None, -math.inf)
    for neighbor in getNeighbors(node, node.turn*-1):
        (_,score) = minimize(neighbor)
        if score > max_score:
            (max_node,max_score) = (neighbor,score)

    guiProgram.treeStr += "\t | Depth: " + str(max_node.depth-piecesInserted) + "\t\t" + "max = " + str(max_score) + "\n"
    # guiProgram.treeStr += "\t\t" + "max = \n" + max_node.printState() + ""
    # print('\tmax = ',max_score)
    # print('-------------------------------')
    return (max_node,max_score)

def minimize(node):
    if terminal_state(node):
        return (None,node.key)
    (min_node,min_score) = (None,math.inf)
    for neighbor in getNeighbors(node, node.turn*-1):
        (_,score) = maximize(neighbor)
        if score < min_score:
            (min_node,min_score) = (neighbor,score)

    guiProgram.treeStr += "\t | Depth: " + str(min_node.depth-piecesInserted) + "\t\t" + "min = " + str(min_score) + "\n"
    # guiProgram.treeStr += "\t\t" + "min = \n" + min_node.printState() + ""
    # print('\tmin = ',min_score)
    # print('-------------------------------')
    return(min_node,min_score)

def decision(node):
    global piecesInserted
    (max_node,_) = maximize(node)
    piecesInserted += 1
    return max_node

def maxAlphaBeta (node, alpha,beta):
    if terminal_state(node):
        return(node,node.key)
    (max_node,max_score) = (None,-math.inf)
    for neighbor in getNeighbors(node, node.turn*-1):
        (_,score) = minAlphaBeta(neighbor,alpha,beta)
        if score > max_score:
            (max_node,max_score) = (neighbor,score)
        if max_score >= beta :
            break
        if max_score > alpha:
            alpha = max_score
    guiProgram.treeStr += "\t | Depth: " + str(max_node.depth-piecesInserted) + "\t\t" + "max = " + str(max_score) + "\n"
    # guiProgram.treeStr += "\t\t" + "max = \n" + max_node.printState() + ""
    # print('\tmax = ',max_score)
    # print('-------------------------------')
    return (max_node,max_score) 

def minAlphaBeta (node, alpha,beta):
    if terminal_state(node):
        return(node,node.key)
    (min_node,min_score) = (None,math.inf)
    for neighbor in getNeighbors(node, node.turn*-1):
        (_,score) = maxAlphaBeta(neighbor,alpha,beta)
        if score < min_score:
            (min_node,min_score) = (neighbor,score)
        if min_score <= alpha :
            break
        if min_score < beta:
            beta = min_score
    guiProgram.treeStr += "\t | Depth: " + str(min_node.depth-piecesInserted) + "\t\t" + "min = " + str(min_score) + "\n"
    # guiProgram.treeStr += "\t\t" + "min = \n" + min_node.printState() + ""
    # print('\tmin = ',min_score)
    # print('-------------------------------')
    return (min_node,min_score)

def decisionAlphaBeta(node):
    global piecesInserted
    (max_node,_) = maxAlphaBeta(node,-math.inf,math.inf)
    piecesInserted += 1
    return max_node

# ------------------------------- GUI CLASS ----------------------------------------
class GUI:
    
    def __init__(self, master):
        self.master = master
        self.master.geometry("1100x700+150+10")
        self.piecesAdded = 0
        self.turn = 1
        self.selectedCol = -1
        self.selectedRow = -1
        self.que = Queue()
        self.treeStr = ""
        self.timeTaken = 0
        self.nodesExpanded = 0
        # ------------------ Initialize Images ---------------------------------
        self.pieceImgsR = [0] * 21
        self.pieceImgsY = [0] * 21
        self.pieceImgsRC = [0] * 21
        self.pieceImgsYC = [0] * 21
        for i in range(21):
            self.pieceImgsR[i] = PhotoImage(file='red piece.png')
            self.pieceImgsY[i] = PhotoImage(file='yellow piece.png')
        # ------------------ GUI Layout ---------------------------------
        titleLbl = Label(self.master, text= "Connect-4", fg = "blue")
        titleLbl.config(font=font.Font(family="Courier", size=44, weight='bold'))
        titleLbl.grid(row=0, column=0, columnspan=15)

        fillLbl = Label(self.master, text= "                     ")
        fillLbl.grid(row=1, column=2)
        
        kLbl = Label(self.master, text="Maximum evaluated tree height: ", font=("Bahnschrift", 12, 'bold'))
        kLbl.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        self.kEntry = Entry(self.master, font=("", 12), width=10)
        self.kEntry.grid(row=1, column=1, sticky=W)

        self.checkAB = IntVar()
        self.ABpruneCheck = Checkbutton(self.master, text='Use alpha-beta pruning', font=("Bahnschrift", 12, 'bold'), variable=self.checkAB)
        self.ABpruneCheck.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=W)

        solveBtnFont = font.Font(size=12, weight='bold')
        solveBtn = Button(master, height=1, width=10, text="Play", bg = "blue", fg = "white", font=solveBtnFont, command=self.initializeGame)
        solveBtn.grid(row=3,column=0, padx=10, pady=10, sticky=W)

        self.timeLbl = Label(self.master, text="Time Taken : ", font=("Bahnschrift", 12), fg = "red")
        self.timeLbl.grid(row=6, column=3, padx=10, pady=5, sticky=N)
        self.timeResLbl = Label(self.master, text="0", font=("Bahnschrift", 12), fg = "red")
        self.timeResLbl.grid(row=6, column=4, padx=10, pady=5, sticky=N)

        self.nodesLbl = Label(self.master, text="Nodes Expanded : ", font=("Bahnschrift", 12), fg = "red")
        self.nodesLbl.grid(row=7, column=3, padx=10, pady=5, sticky=N)
        self.nodesResLbl = Label(self.master, text="0", font=("Bahnschrift", 12), fg = "red")
        self.nodesResLbl.grid(row=7, column=4, padx=10, pady=5, sticky=N)

        self.pScoreLbl = Label(self.master, text="Player Score = 0", font=("Bahnschrift", 12, 'bold'), fg = "red")
        self.pScoreLbl.grid(row=5, column=3, padx=10, pady=5, sticky=N)
        self.aiScoreLbl = Label(self.master, text="AI Score = 0", font=("Bahnschrift", 12, 'bold'), fg = "red")
        self.aiScoreLbl.grid(row=5, column=4, padx=10, pady=5, sticky=N)

        self.resTxt = Text(state='disabled', font=("Calibri", 11), width=80, height=23)
        self.resTxt.grid(row=4, column=0, columnspan=3, rowspan=5, padx=10, pady=20)
        self.scroller = Scrollbar(self.master)
        self.scroller.place(in_=self.resTxt, relx=0.97, rely= 0, height=415)
        self.scroller.config(command=self.resTxt.yview)
        self.resTxt.config(yscrollcommand = self.scroller.set)

        self.canvas = Canvas(self.master, width=500, height=500)
        self.canvas.grid(row=1, column=3, rowspan=4, columnspan=2, sticky=NE)
        
        self.boardImg = PhotoImage(file='Game Board.png')
        self.boardImgC = self.canvas.create_image(250, 270, image=self.boardImg)

    # ------------------ Functions ---------------------------------
    def printTree(self, key):
        self.resTxt.configure(state='normal')
        self.resTxt.delete('1.0','end')
        self.resTxt.insert('end', key)
        self.resTxt.configure(state='disabled')

    def initializeGame(self):
        global maxdepth, useAlphaBeta
        try:
            maxdepth = int(self.kEntry.get())
            useAlphaBeta = self.checkAB.get()
            self.playTurn(None)
        except ValueError:
            print("Please enter max tree depth")
        

    def playTurn(self, node):
        global piecesInserted
        
        if piecesInserted == 0:
            node = initState

        self.pScoreLbl.config(text="Player Score = " + str(node.scorePlayer))
        self.aiScoreLbl.config(text="AI Score = " + str(node.scoreAI))

        # WHEN GAME ENDS
        if (node.depth == 42):
            # print("done")
            # print("AI Score: ", node.scoreAI, "\tPlayer Score: ", node.scorePlayer)
            guiProgram.treeStr += "GAME OVER \n"
            if node.scoreAI > node.scorePlayer:
                guiProgram.treeStr += "AI WINS \n"
            elif node.scoreAI < node.scorePlayer:
                guiProgram.treeStr += "PLAYER WINS \n"
            else:
                guiProgram.treeStr += "TIE \n"

            self.printTree(self.treeStr)
            return

        # PLAYER'S TURN
        if (node.turn == 1): 

            print("waiting for user input")
            self.canvas.bind('<Button-1>', lambda event, arg = node: self.selectColumn(event, arg))

        # AI'S TURN
        elif (node.turn == -1): 
            self.nodesExpanded = 0
            start = timeit.default_timer()
            if useAlphaBeta == 0:
                t = threading.Thread(target=lambda q, arg1: q.put(decision(arg1)), args=(self.que, node))
            else:
                t = threading.Thread(target=lambda q, arg1: q.put(decisionAlphaBeta(arg1)), args=(self.que, node))
            t.start()
            self.master.update()
            t.join()
            stop = timeit.default_timer()
            self.timeTaken = stop-start
            self.timeResLbl.config(text=str(self.timeTaken))
            self.nodesResLbl.config(text=str(self.nodesExpanded))
            self.printTree(self.treeStr)
            self.treeStr = ""
            result = self.que.get()
            self.newTurn(result)

                
    
    def getCoord(self, index, axis):
        # axis = 0 for col index, axis = 1 for row index
        coords = {
            -1: [0,30],
            0: [60.5, 101.5],
            1: [124, 164],
            2: [187.45, 225],
            3: [251, 287],
            4: [314, 349],
            5: [378, 411],
            6: [442, 0],
        }
        return coords.get(index)[axis]
    
    def selectColumn(self, event, node):
        global piecesInserted
        x = event.x
        # coords = [0, 90, 153, 216, 279, 342, 405, 500]
        if x < 90:
            self.selectedCol = 0
        elif x < 153:
            self.selectedCol = 1
        elif x < 216:
            self.selectedCol = 2
        elif x < 279:
            self.selectedCol = 3
        elif x < 342:
            self.selectedCol = 4
        elif x < 405:
            self.selectedCol = 5
        else:
            self.selectedCol = 6

        # insert new piece into state
        self.printTree("")
        result = addPiece(node, self.selectedCol, node.turn*-1)
        piecesInserted += 1
        self.canvas.unbind('<Button-1>')
        self.canvas.after(100,self.newTurn, result)

    def newTurn(self, node):
        (self.selectedRow, self.selectedCol) = node.insertedIndex
        self.addPieceGUI(self.selectedRow, self.selectedCol, node)

    def addPieceGUI(self, row, column, node):
        imageIndex = int(self.piecesAdded/2)
        if self.turn == 1: 
            self.pieceImgsRC[imageIndex] =self.canvas.create_image(self.getCoord(column,0), self.getCoord(-1,1), image=self.pieceImgsR[imageIndex])
            self.canvas.tag_lower(self.pieceImgsRC[imageIndex])
            self.currentPos = self.getCoord(-1,1)
            self.finalPos = self.getCoord(row,1)
            self.moveImg(node)
            
        elif self.turn == -1:
            self.pieceImgsYC[imageIndex] = self.canvas.create_image(self.getCoord(column,0), self.getCoord(-1,1), image=self.pieceImgsY[imageIndex])
            self.canvas.tag_lower(self.pieceImgsYC[imageIndex])
            self.currentPos = self.getCoord(-1,1)
            self.finalPos = self.getCoord(row,1)
            self.moveImg(node)
            
    def moveImg(self, node):
        imageIndex = int(self.piecesAdded/2)
        if (self.currentPos + 70 < self.finalPos):
            if self.turn == 1:
                self.canvas.move(self.pieceImgsRC[imageIndex], 0, 70)
            elif self.turn == -1:
                self.canvas.move(self.pieceImgsYC[imageIndex], 0, 70)
            self.currentPos += 70
            self.canvas.after(100, self.moveImg, node)
        elif(self.currentPos < self.finalPos):
            if self.turn == 1:
                self.canvas.move(self.pieceImgsRC[imageIndex], 0, self.finalPos - self.currentPos)
            elif self.turn == -1:
                self.canvas.move(self.pieceImgsYC[imageIndex], 0, self.finalPos - self.currentPos)
            self.canvas.unbind('<Button-1>')

            # Start new turn
            self.turn *= -1
            self.piecesAdded += 1
            self.canvas.after(500, self.playTurn, node)
            

root = Tk()
guiProgram = GUI(root)
root.mainloop()