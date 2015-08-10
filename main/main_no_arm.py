import numpy as np
import argparse
import cv2
import regions
import tictactoe
import time
import pygame

# define video port here, usually 0
VIDEPORT = 1

def findCircles(image):
    # Returns the position and the size of the circle found.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(5,5))
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.4, 30)
    return circles

def drawCircles(image, x , y, r):
    # Draws a circle on the frame.
    cv2.circle(image, (x, y), r, (0, 255, 0), 4)
    cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

def findMove(image, circles):
    # Returns the move of the opponent.

    # convert coordinates to integer
    circles = np.round(circles[0, :]).astype("int")
    opponentMove = 0

    # iterate all circles found
    for (x, y, r) in circles:

        isMoved = True
        # check which region the found circle belongs to
        if((x >= regions.minX) and (x <= regions.maxX)) and ((y >= regions.minY) and (y <= regions.maxY)):
            region = regions.checkRegion(x,y)
        else:
            break

        # iterate all available moves
        for move in board.availableMoves():
            # if the region has'nt been occupied, take it as the opponent's move
            if move + 1  == region:
                isMoved = False
                break
            # do nothing if the region has been occupied before
            else:
                pass

        if not isMoved:
            opponentMove = region - 1
            isMoved = True
            return opponentMove

def nextMove(opponentMove):
    # Returns the next best move for the arm

    player = 'X'
    # save the opponent's move in the list
    board.makeMove(opponentMove, player)
    print "Opponent Move: ", opponentMove + 1
    board.show()

    # get the next best move based on the opponent's move
    player = tictactoe.getEnemy(player)
    computerMove = tictactoe.determine(board, player)

    # save the computer's move in the list
    board.makeMove(computerMove, player)
    print "Computer Move: ", computerMove + 1
    board.show()

    # play a beep sound the acknowldge the opponent's move
    pygame.init()
    pygame.mixer.music.load("beep.wav")
    pygame.mixer.music.play()
    return computerMove + 1

def drawRegions(image):
    # Draws all the squares on the frame
    '''
    sample data
    [0, 213, 426, 639]
    [0, 160, 320, 480]
    r1 = (0   , 0  ) (213  , 160)
    r2 = (213 , 0  ) (426  , 160)
    r3 = (426 , 0  ) (640  , 160)

    r4 = (0 ,  160 ) (213, 320)
    r5 = (213, 160 ) (426, 320)
    r6 = (426, 160 ) (640, 320)

    r7 = (0, 320 ) (213, 480)
    r8 = (213, 320 ) (426, 480)
    r9 = (426, 320 ) (640, 480)
    '''
    fontIndex = 0
    for i in xrange(regions.totalYintercepts-1):
        for ii in xrange(regions.totalXintercepts-1):
            x1 = regions.xIntercepts()[ii]
            x2 = regions.xIntercepts()[ii + 1]
            y1 = regions.yIntercepts()[i]
            y2 = regions.yIntercepts()[i+1]
            # draw the rectangles
            cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
            fontIndex = fontIndex + 1
            #dra the labels
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image,str(fontIndex),(x1 +5,y1+25), font, 0.7,(255,255,255),2)

def drawOpponentMoves(image):
    # Draws all the opponent's moves on the frame
    for move in board.getSquares('X'):
        x = regions.center()[move][0]
        y = regions.center()[move][1]
        cv2.circle(image, (x, y), 40, (0, 0, 255), 10)

def drawComputerMoves(image):
    # Draws all the computer's moves on the frame
    for move in board.getSquares('O'):
        x = regions.center()[move][0]
        y = regions.center()[move][1]
        cv2.rectangle(image, (x - 40, y - 40), (x + 40, y + 40), (255, 0, 0), 10)

def main():
    # store which turn it is.
    turn = 0
    # continue looping until there's a winner
    while not board.complete():

        # get the frame from the video feed
        ret, image = videoCapture.read()

        # find all the circles on the frame
        circles = findCircles(image)

        if circles is not None:

            # get opponent's move
            opponentMove = findMove(image, circles)
            if not opponentMove in board.availableMoves():
                continue

            # calculate what's the next move
            computerMove = nextMove(opponentMove)

            #end the game if thpyere's any winner
            if board.complete():
                break

        #draw opponent's and computer's move on the screen
        drawComputerMoves(image)
        drawOpponentMoves(image)
        drawRegions(image)
        cv2.imshow('TICTACTOE',image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
    		break

    print "winner is", board.winner()
    pygame.mixer.music.load("beep2.wav")
    pygame.mixer.music.play()
    time.sleep(1)
    videoCapture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    regions = regions.Regions(50,400,400,50,3,3)
    videoCapture = cv2.VideoCapture(VIDEPORT)
    board = tictactoe.Tic()
    image = None
    main()
