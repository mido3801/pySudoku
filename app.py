import pygame
from pygame import *

class Grid:
    grid = [[0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]]

def isValidBoard(board):
    for x,item in enumerate(grid[1]):
        for row in grid[1:8:1]:
            if (row[x] == item):
                return false
    for row in board:
        for item in row:
            if (row.count(item) > 1):
                return false
    for x in range(1:4):
        for y in range(0:4):
            
