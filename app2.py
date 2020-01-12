class Board():

    def __init__(self):

        self.grid = [[5,3,0,0,7,0,0,0,0],
                    [6,0,0,1,9,5,0,0,0],
                    [0,9,8,0,0,0,0,6,0],
                    [8,0,0,0,6,0,0,0,3],
                    [4,0,0,8,0,3,0,0,1],
                    [7,0,0,0,2,0,0,0,6],
                    [0,6,0,0,0,0,2,8,0],
                    [0,0,0,4,1,9,0,0,5],
                    [0,0,0,0,8,0,0,7,9]]

    def isValidBoard(self):
        #checks rows for repeats, then columns, then the subgrids. If finds a duplicate returns false
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
        #finds next empty space (used for solver)
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                if self.grid[x][y] == 0:
                    return(x, y)

        return False


    def solveBoard(self):
        toSolve = self.nextEmpty()
        if toSolve == False:
            return True
        else:
            x,y = toSolve

            #tries a value in open spots, then calls function recursively so if
            # a roadblock is hit it backtracks
        for i in range(1,10):
            if self.checkPosition(i,(x,y)):
                self.grid[x][y] = i

                if self.solveBoard():
                    return True

                self.grid[x][y] = 0

        return False

    def resetBoard(self):
        self.__init__()
