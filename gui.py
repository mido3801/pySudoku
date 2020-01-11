import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPen, QColor, QFont, QTransform
from PyQt5.QtCore import QRectF, Qt
from app2 import Board


class Scene(QGraphicsScene):

    def __init__(self,board):
        super().__init__()

        self.grid = board.grid

        self.font = QFont('Sand Serif', pointSize = 40)
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
                newRect = QRectF(j*60,i*60,60,60)
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



        # num = QGraphicsTextItem("5",rectGrid[0][0])
        # num2 = QGraphicsTextItem("7", rectGrid[0][1])
        # num.setPlainText("6")
        # num.setFont(self.font)
        # num2.setFont(self.font)
        # num2.setTransform(QTransform(1,0,0,1,70,0))
        # print(rectGrid[0][1].x())


    def setNums(self):
        for x,row in enumerate(self.grid):
            for y,i in enumerate(row):
                if (i != 0):
                    self.numGrid[x][y].setPlainText(str(i))




class Viewer(QGraphicsView):

    def __init__(self,scene):
        super().__init__()

        self.initGui()
        self.scene = scene

        self.setScene(scene)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

        self.cmenu = QMenu(self)
        self.checker = self.cmenu.addAction("CheckBoard")


    def initGui(self):

        self.setMinimumSize(560,560)
        self.setMaximumSize(560,560)
        self.show()

    def mousePressEvent(self, e):
        #gridX = int(e.pos[0])//60
        #gridY = int(e.pos[1])//60
        if e.button() == Qt.LeftButton:

            gridX = e.x()//60
            gridY = e.y()//60

            if (gridX <= 8) and (gridY <= 8):

                input, ok = QInputDialog.getText(self, "Guess", "Enter Number: ")

                if ok:

                    if board.checkPosition(int(input),(gridX,gridY)):
                        scene.numGrid[gridX][gridY].setDefaultTextColor(QColor(0,0,0))
                        scene.numGrid[gridX][gridY].setPlainText(input)
                        scene.board.grid[gridX][gridY] = int(input)


                    else:
                        scene.numGrid[gridX][gridY].setDefaultTextColor(QColor(255,0,0))
                        scene.numGrid[gridX][gridY].setPlainText(input)
                        scene.board.grid[gridX][gridY] = int(input)




    def onContextMenu(self, pos):

        action = self.cmenu.exec_(self.mapToGlobal(pos))

        if action == self.checker:
            message = QMessageBox()
            message.setText("asdufha")
            message.exec_()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = Board()
    scene = Scene(board)
    view = Viewer(scene)
    #view.setScene(scene)
    sys.exit(app.exec_())
