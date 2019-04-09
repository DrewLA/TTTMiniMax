#Author: Andrew Lewis
#Program: TicTacToe
#       
#       Implementation of a TicTacToe game instance between a user and a MiniMax search algorithm
#       Game Class stores game board state and helper functions
#       Human Class is a wrapper for the input listener represeting the human player
#       MiniMax Class is an instance of the MiniMax algorithm

import time
class Game:

    def __init__(self):
        self.board = ['-' for i in range(9)]
        self.prevMoves = []
        self.winner = None
        self.gameIsActive = True

    def openSpots(self):
        moves = []
        for i,j in enumerate(self.board):
            if j == '-':
                moves.append(i)
        return moves
    
    def tickSpot(self, letter, spot):
        self.board[spot] = letter
        self.prevMoves.append(spot)

    #Helper function to revert to previous state
    def prevMove(self):
        self.board[self.prevMoves.pop()] = '-'
        self.winner = None        

    #Helper for MiniMax terminal state search
    def checkTerminal(self):
        terminalStates = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8), (2,4,6)]
        for i,j,k in terminalStates:
            if self.board[i] != '-' and self.board[i] == self.board[j] == self.board[k]:
                self.winner = self.board[i]
                return True

        if '-' not in self.board:
                self.winner = '-'
                return True

        return False
    
    #Check the terminal state
    def checkWinner(self):
        terminalStates = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8), (2,4,6)]
        for i,j,k in terminalStates:
            if self.board[i] != '-' and self.board[i] == self.board[j] == self.board[k]:
                self.winner = self.board[i]
                self.printBoard()
                self.gameIsActive = False
                if self.winner == '-':
                    print("\nGame over with Draw")
                else:
                    print("\nWinner : %s" %self.winner)
                self.gameIsActive = False
                return True

            if '-' not in self.board:
                self.winner = '-'
                return True

        return False

    def printBoard(self):
        print("Current Board")
        for j in range(0,9,3):
            for i in range(3):
                if self.board[j+i] == '-':
                    print("- |", end ="")
                    #print("%d |" %(j+i), end ="")
                else:
                    print("%s |" %self.board[j+i], end="")
    
            print("\n", end="")
    
    #Restart game instance
    def restart(self):
        self.board = ['-' for i in range(9)]
        self.prevMoves = []
        self.winner = None
        self.gameIsActive = True
        while True:        
            hMarker = input("X or O: ")            
            try:
                hMarker = str(hMarker)
            except:
                hMarker = None    
            if hMarker == 'X' or hMarker == 'O':
                break
    
        player1 = Human(hMarker)
        if hMarker == "X":
            player2 = MiniMax("O")
        else:
            player2 = MiniMax("X")
        self.play(player1, player2)
        
    def play(self, p1, p2):
        self.human = p1
        self.ai = p2
        self.turn = 0
        #check game state
        print("")
        print("Move Postions are from 1-9")
        while (self.checkTerminal())!= True:
            self.printBoard()
            print("")
            if self.turn==0: 
                    print("Enter move")
                    self.human.move(self)
                    self.turn = 1
            else:
                    print("AI moves")
                    self.ai.move(self)
                    self.turn=0
        print("Game Over")
        self.printBoard()
        if self.winner == '-':
                    print("\nGame over with Draw")
        else:
                    print("\nWinner : %s" %self.winner)
        x = input("Do you want to play again? enter y/n: ")
        try:
            x = str(x)
        except:
            x = None
        if x == 'y':
            self.restart()
            return
        else:
            exit()            

class Human:
    
    def __init__(self,marker):
        self.marker = marker
    
    def move(self, gameInstance):

        while True:        
            m = input("Input position:")            
            try:
                m = int(m)
            except:
                m = -1
            #meet input requirements for text interface
            m = m - 1
            if m not in gameInstance.openSpots():
                print ("Invalid move. Retry")
            else:
                break    
        gameInstance.tickSpot(self.marker,m)
        #gameInstance.checkWinner()
    

class MiniMax:
    def __init__(self, marker):
        self.marker = marker
        if self.marker == 'X':
            self.humanMarker = 'O'
        else:
            self.humanMarker = 'X'

    def move(self,gameInstance):
        movePosition,score = self.maxMove(gameInstance)
        gameInstance.tickSpot(self.marker,movePosition)
    
    #Returns score and index of best move to make for Max
    def maxMove(self,gameInstance):
        bestScore = None
        bestMove = None

        for m in gameInstance.openSpots():
            gameInstance.tickSpot(self.marker,m)
        
            if gameInstance.checkTerminal():
                score = self.getScore(gameInstance)
            else:
                movePosition,score = self.minMove(gameInstance)
        
            gameInstance.prevMove()
            
            if bestScore == None or score > bestScore:
                bestScore = score
                bestMove = m

        return bestMove, bestScore

    #Returns score and index of best move for Min
    def minMove(self,gameInstance):
        bestScore = None
        bestMove = None

        for m in gameInstance.openSpots():
            gameInstance.tickSpot(self.humanMarker,m)
        
            if gameInstance.checkTerminal():
                score = self.getScore(gameInstance)
            else:
                movePosition, score = self.maxMove(gameInstance)
        
            gameInstance.prevMove()
            
            if bestScore == None or score < bestScore:
                bestScore = score
                bestMove = m

        return bestMove, bestScore
       
    def getScore(self,gameInstance):
        if gameInstance.checkTerminal():
            if gameInstance.winner  == self.marker:
                return 1 # Won

            elif gameInstance.winner == self.humanMarker:
                return -1 # Opponent won

        return 0 # Draw
        
#main program driver
if __name__ == '__main__':
    game = Game() 
    while True:        
        hMarker = input("X or O: ")            
        try:
            hMarker = str(hMarker)
        except:
            hMarker = None    
        if hMarker == 'X' or hMarker == 'O':
            break
    
    player1 = Human(hMarker)
    if hMarker == "X":
        player2 = MiniMax("O")
    else:
        player2 = MiniMax("X")
    game.play(player1, player2)
