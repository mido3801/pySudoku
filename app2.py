class Board():

    def __init__(self):

        self.grid = [[0,7,1,0,9,0,8,0,0],
                [0,0,0,3,0,6,0,0,0],
                [4,9,0,0,0,0,7,0,5],
                [0,1,0,9,0,0,0,0,0],
                [9,0,2,0,0,0,6,0,3],
                [0,0,0,0,0,8,0,2,0],
                [8,0,5,0,0,0,0,7,6],
                [0,0,0,6,0,7,0,0,0],
                [0,0,7,0,4,0,3,5,0]]

    def isValidBoard(self):
        for x,row in enumerate(self.grid):
            rowSet = set()
            for y,num in enumerate(row):
                if (num == 0):
                    continue
                if num in rowSet:
                    return False
                else:
                    rowSet.add(num)

                if (x == 0):
                    col = [row[y] for row in self.grid]
                    colSet = set()
                    if(col.count(num) > 1):
                        return False

                if(x%3 == 0 and y%3 == 0):
                    subgrid = [self.grid[i][j] for i in range(x,x+3) for j in range(y,y+3)]
                    subgridSet = set()
                    for i in subgrid:
                        if i in subgridSet:
                            return False
                        else:
                            subgridSet.add(i)
        return True

    def checkPosition(self,val,position):

        #check row
        for i in range(9):
            if self.grid[position[0]][i] == val and i != position[1]:
                return False

        #check column
        for i in range(9):
            if self.grid[i][position[1]] == val and i != position[0]:
                return False

        #check subgrid
        gridCol = position[1] // 3
        gridRow = position[0] // 3

        for i in range(gridRow*3, gridRow*3+3):
            for j in range(gridCol*3, gridCol*3+3):
                if self.grid[i][j] == val and (i,j) != position:
                    return False

        return True



    def printBoard(self):
        for x,row in enumerate(self.grid):
            if (x in [3,6]):
                print("-"*11)
            for y,num in enumerate(row):
                if (y in [3,6]):
                    print("|", end = "")
                print(num, end = "")
            print("")


    def nextEmpty(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                if self.grid[x][y] == 0:
                    return(x, y) #row,column

        return False


    def boardSolver(self):

        toSolve = self.nextEmpty
        if not toSolve:
            return True
        else:
            row,col = toSolve

        for i in range(1,10):
            if checkPosition(self.grid,i,(row,col)):
                self.grid[row][col] = i

                if self.boardSolver:
                    return True

                board[row][col] = 0

        return False
