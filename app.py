import pygame
from pygame import *

grid = [[0,7,1,0,9,0,8,0,0],
        [0,0,0,3,0,6,0,0,0],
        [4,9,0,0,0,0,7,0,5],
        [0,1,0,9,0,0,0,0,0],
        [9,0,2,0,0,0,6,0,3],
        [0,0,0,0,0,8,0,2,0],
        [8,0,5,0,0,0,0,7,6],
        [0,0,0,6,0,7,0,0,0],
        [0,0,7,0,4,0,3,5,0]]

def isValidBoard(board):
    for x,row in enumerate(board):
        rowSet = set()
        for y,num in enumerate(row):
            if (num == 0):
                continue
            if num in rowSet:
                return False
            else:
                rowSet.add(num)

            if (x == 0):
                col = [row[y] for row in board]
                colSet = set()
                if(col.count(num) > 1):
                    return False

            if(x%3 == 0 and y%3 == 0):
                subgrid = [board[i][j] for i in range(x,x+3) for j in range(y,y+3)]
                subgridSet = set()
                for i in subgrid:
                    if i in subgridSet:
                        return False
                    else:
                        subgridSet.add(i)
    return True

def checkPosition(board,val,position):

    #check row
    for i in range(9):
        if board[position[0]][i] == val and i != position[1]:
            return False

    #check column
    for i in range(9):
        if board[i][position[1]] == val and i != position[0]:
            return False

    #check subgrid
    gridCol = position[1] // 3
    gridRow = position[0] // 3

    for i in range(gridRow*3, gridRow*3+3):
        for j in range(gridCol*3, gridCol*3+3):
            if board[i][j] == val and (i,j) != position:
                return False

    return True



def printBoard(board):
    for x,row in enumerate(board):
        if (x in [3,6]):
            print("-"*11)
        for y,num in enumerate(row):
            if (y in [3,6]):
                print("|", end = "")
            print(num, end = "")
        print("")


def nextEmpty(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 0:
                return(x, y) #row,column

    return False


def boardSolver(board):

    toSolve = nextEmpty(board)
    if not toSolve:
        return True
    else:
        row,col = toSolve

    for i in range(1,10):
        if checkPosition(board,i,(row,col)):
            board[row][col] = i

            if boardSolver(board):
                return True

            board[row][col] = 0

    return False
