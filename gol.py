
# Conway's game of Life
# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any live cell with more than three live neighbours dies, as if by overpopulation.
# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

# We are using the Moore neighborhood definition
# That means, every cell has 8 potential neighboring cells
# N E S W NE SE SW NW

import time
import pygame
import random
import sys



def print2dArray(inp):
    for row in inp:
        for c in row:
            print(c, end=' ')
        print("")
    print("\n")

def brdCopy(brd):
        retBoard = [[Cell([i,j], False) for i in range(len(brd))] for j in range(len(brd))]

        for row in range(len(brd)):
            for col in range(len(brd)):
                retBoard[row][col] = brd[row][col]
        return retBoard
# Found function from on stackoverflow for drawing a cell with an outline.
# Implementation is simple and is performed by drawing a box with outline color, and then a smaller box
# with the desired cell color.
def fill_woutline(surface, fill_color, outline_color, border=1):
    surface.fill(outline_color)
    surface.fill(fill_color, surface.get_rect().inflate(-border, -border))

class Cell:
    def __init__(self, location, alive=False):
        self.loc = tuple(location)
        self.alive = bool(alive)
        self.numAdj = 0
    def __str__(self):
        if self.alive:
            #return x with green text then reset color coding
            return "\u001b[032mx\u001b[0m" #+ str(self.loc[0]) + str(self.loc[1])
        else:    
            #return 0 with red text then reset color coding
            return "\u001b[031m0\u001b[0m" #+ str(self.loc[0]) + str(self.loc[1])




class gol:
    def __init__(self, size):
        self.size = size
        self.board = [[Cell([i,j], False) for i in range(size)] for j in range(size)]
        self.numGens = 0

    def getNumGens(self):
        return self.getNumGens

    
    def evaluate(self):
        boardTemplate = brdCopy(self.board)

        for row in range(self.size):
            for col in range(self.size):
                #tempCell = self.board[row][col]
                tempCell = Cell((row,col), self.board[row][col].alive)
                # Count number of neighbors
                # note to self - using %size in the indexes gives wrapping functionality
                #N
                if(self.board[(row-1)%self.size][col%self.size].alive): 
                    tempCell.numAdj = tempCell.numAdj + 1
                #NW
                if(self.board[(row-1)%self.size][(col-1)%self.size].alive): 
                    tempCell.numAdj = tempCell.numAdj + 1
                #NE
                if(self.board[(row-1)%self.size][(col+1)%self.size].alive): 
                    tempCell.numAdj = tempCell.numAdj + 1
                #S
                if(self.board[(row+1)%self.size][(col)%self.size].alive):
                    tempCell.numAdj = tempCell.numAdj + 1
                #SW
                if(self.board[(row+1)%self.size][(col-1)%self.size].alive):
                    tempCell.numAdj = tempCell.numAdj + 1
                #SE
                if(self.board[(row+1)%self.size][(col+1)%self.size].alive):
                    tempCell.numAdj = tempCell.numAdj + 1
                #W
                if(self.board[(row)%self.size][(col-1)%self.size].alive):
                    tempCell.numAdj = tempCell.numAdj + 1
                #E
                if(self.board[(row)%self.size][(col+1)%self.size].alive):
                    tempCell.numAdj = tempCell.numAdj + 1

                #print("Cell: " + str(tempCell.loc[0]) + str(tempCell.loc[1]) + " adj: " + str(tempCell.numAdj))
                # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                if(tempCell.alive and tempCell.numAdj < 2):
                    tempCell.alive = False
                    #print("cell dies (under pop)")
                
                # Any live cell with two or three live neighbours lives on to the next generation.
                elif(tempCell.alive and (tempCell.numAdj == 2 or tempCell.numAdj == 3)):
                    tempCell.alive = True    
                    #print("cell lives (adj == 2|3)")

                    # Cell lives on
                # Any live cell with more than three live neighbours dies, as if by overpopulation.
                elif(tempCell.alive and tempCell.numAdj > 3):
                    tempCell.alive = False
                    #print("cell dies (over pop)")

                # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                elif(not tempCell.alive and tempCell.numAdj == 3):
                    tempCell.alive = True
                    #print("reproduce")
                    #Cell comes alive
                boardTemplate[row][col] = tempCell
                #print2dArray(boardTemplate)
                #END OF LOOP
        #Set board to new board - return
        self.board = boardTemplate
        return

    def isDead(self)->bool:
        for row in range(self.size):
            for col in range(self.size):
                if (self.board[row][col].alive):
                    #If a single cell is still alive, the board is alive
                    return False
        #But if we iterate through the whole board with no live cells then the game is dead
        return True

    def setRandomStates(self):
        for row in range(self.size):
            for col in range(self.size):
                self.board[row][col].alive = (random.randint(0,1))


def main():
    # -------- Game setup ----------
    # Use gameScale variable to change the scale of the game. 
    # Beware the limitations of the GUI, that is, 
    # that each cell draws at a 3px x 3px square at minimum
    # 
    # 256 seems to be good scale for large board, and 128 for medium
    # and 64 for small. Smaller values work fine, but going larger
    # becomes more and more intensive & unstable
    # ------------------------------
    gameScale = 128
    #Create instance of GOL using gamescale as input
    game = gol(gameScale)
    #Set all cells to be randomly alive or dead
    game.setRandomStates()
    #Start GUI
    pygame.init()
    width = 600
    height = 600
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Conway\'s Game of Life')
    clock = pygame.time.Clock()
    cellSize = height/gameScale
    #Start time clock
    startTime = time.time()



   
    #Game loop 
    while(1):
        #print2dArray(game.board)
        game.evaluate()
        game.numGens+=1
        #time.sleep(.1)
        if(game.isDead()):
            break
        # Make the X button work to quit program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # Fill each cell on the GUI
        for row in range(game.size):
            for col in range(game.size):
                tempCell = game.board[row][col]
                tempCellSurf = pygame.Surface((cellSize,cellSize))
                #Set color of cell dependant on Alive status
                if(tempCell.alive):
                    fill_woutline(tempCellSurf, 'Green', 'Black')
                else:
                    fill_woutline(tempCellSurf, 'Black', 'Black')
                # Set location of cell
                screen.blit(tempCellSurf,(tempCell.loc[0]*cellSize,tempCell.loc[1]*cellSize))
        pygame.display.update()

        # Generation rate / sec
        # 
        if(game.numGens%20 == 0):
            timeDelta = time.time() - startTime
            generationRate = round(20/timeDelta, 2)
            startTime = time.time()
            print(generationRate," generations /sec")

if __name__ == "__main__":
    main()


    