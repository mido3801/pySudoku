import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPen, QColor, QFont, QTransform
from PyQt5.QtCore import QRectF, Qt
from app2 import Board


class Scene(QGraphicsScene):

    def __init__(self,board):
        super().__init__()

        origGrid = board.grid.copy()

        self.origGrid = origGrid
        self.board = board

        self.font = QFont('Sans Serif', pointSize = 40)
        self.pen = QPen()
        self.getMouseTracking = True
        self.drawLines()
        self.setSquares()
        self.setNums()

    def drawLines(self):
        #draw vertical lines
        for i in range(1,9):
            if i%3 == 0:
                self.pen.setWidth(4)

            self.addLine(i*60,0,i*60,540,self.pen)
            self.addLine(0,i*60,540,i*60,self.pen)

            self.pen.setWidth(1)

    def setSquares(self):

        rectGrid = []
        numGrid = []

        for i in range(9):
            rectRow = []
            numRow = []
            for j in range(9):
                newRect = QRectF(i*60,j*60,60,60)
                newRectItem = QGraphicsRectItem()
                newRectItem.setRect(newRect)
                self.addItem(newRectItem)
                rectRow.append(newRectItem)
                num = QGraphicsTextItem("",newRectItem)
                num.setTransform(QTransform(1,0,0,1,(10+60*j),(60*i)))
                num.setFont(self.font)
                numRow.append(num)
            rectGrid.append(rectRow)
            numGrid.append(numRow)


        self.rectGrid = rectGrid
        self.numGrid = numGrid


    def setNums(self):
        self.defaultSet = []
        for x,row in enumerate(self.board.grid):
            for y,i in enumerate(row):
                if (i != 0):
                    self.numGrid[x][y].setPlainText(str(i))
                    self.defaultSet.append((x,y))



class Viewer(QGraphicsView):

    def __init__(self,scene):
        super().__init__()

        self.initGui()
        self.scene = scene

        self.setScene(scene)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

        self.cmenu = QMenu(self)
        self.checker = self.cmenu.addAction("Check Board")
        self.resetboard = self.cmenu.addAction("Reset Board")
        self.solveboard = self.cmenu.addAction("Solve Board")


    def initGui(self):

        self.setMinimumSize(560,560)
        self.setMaximumSize(560,560)
        self.show()

    def mousePressEvent(self, e):

        if e.button() == Qt.LeftButton:

            gridX = e.x()//60
            gridY = e.y()//60

            if (gridX <= 8) and (gridY <= 8):

                input, ok = QInputDialog.getText(self, "Guess", "Enter Number: ")

                if ok:

                    scene.numGrid[gridY][gridX].setDefaultTextColor(QColor(0,0,0))
                    scene.numGrid[gridY][gridX].setPlainText(input)
                    scene.board.grid[gridY][gridX] = int(input)


    def onContextMenu(self, pos):

        action = self.cmenu.exec_(self.mapToGlobal(pos))

        if action == self.checker:
            message = QMessageBox()

            if  scene.board.isValidBoard():
                message.setText("Solved!")
                message.exec_()

            else:
                for x,row in enumerate(scene.board.grid):
                    for y,num in enumerate(row):
                        if ((y,x) not in scene.defaultSet):
                            scene.numGrid[y][x].setDefaultTextColor(QColor(255,0,0))


                message.setText("Nope")
                message.exec_()

        elif action == self.resetboard:

            for x,row in enumerate(scene.numGrid):
                for y,i in enumerate(row):

                    if (y,x) not in scene.defaultSet:
                        scene.numGrid[y][x].setPlainText("")

        elif action == self.solveboard:

            scene.board.solveBoard()

            for x,row in enumerate(scene.numGrid):
                for y,i in enumerate(row):

                    scene.numGrid[y][x].setPlainText(str(scene.board.grid[y][x]))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = Board()
    scene = Scene(board)
    view = Viewer(scene)
    #view.setScene(scene)
    sys.exit(app.exec_())
