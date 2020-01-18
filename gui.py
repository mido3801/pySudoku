import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPen, QColor, QFont, QTransform
from PyQt5.QtCore import QRectF, Qt, QTimer
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

        self.numGrid = numGrid
        self.possNums = []

        for x,row in enumerate(self.numGrid):
            possNumsRow = []
            for y,num in enumerate(row):
                possNumsArray = []
                for i in range(2):
                    for j in range(2):
                        possNum = QGraphicsTextItem("")
                        possNum.setTransform(QTransform(1,0,0,1,(self.numGrid[x][y].transform().dx())+(i*46)-10,(self.numGrid[x][y].transform().dy())+(j*45)-5))
                        self.addItem(possNum)
                        possNumsArray.append(possNum)

                possNumsRow.append(possNumsArray)
            self.possNums.append(possNumsRow)



    def setNums(self):
        self.defaultSet = []
        for x,row in enumerate(self.board.grid):
            for y,i in enumerate(row):
                if (i != 0):
                    #self.numGrid[x][y].setPlainText(str(i))
                    self.numGrid[x][y].setHtml("<font color = \"DarkBlue\">{}</font>".format(str(i)))
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

            self.gridCol = e.x()//60
            self.gridRow = e.y()//60

            if (self.gridCol <= 8) and (self.gridRow <= 8):

                self.guesswindow = guess2Window(self)
                self.guesswindow.show()

                # self.scene.numGrid[gridRow][gridCol].setDefaultTextColor(QColor(0,0,0))
                # self.scene.numGrid[gridRow][gridCol].setPlainText(self.guesswindow.choice)
                #
                # if self.scene.board.checkPosition(int(self.guesswindow.choice),(gridRow,gridCol)):
                #     self.scene.board.grid[gridRow][gridCol] = int(self.guesswindow.choice)


    def onContextMenu(self, pos):

        action = self.cmenu.exec_(self.mapToGlobal(pos))

        if action == self.checker:
            message = QMessageBox()

            if  self.scene.board.isValidBoard():
                message.setText("Solved!")
                message.exec_()

            else:
                for x,row in enumerate(self.scene.board.grid):
                    for y,num in enumerate(row):
                        if ((x,y) not in self.scene.defaultSet):
                            if self.scene.board.checkPosition(num,(x,y)) == False:
                                self.scene.numGrid[x][y].setHtml("<font color = \"red\">{}</font>".format(self.scene.numGrid[x][y].toPlainText()))


                message.setText("Nope")
                message.exec_()

        elif action == self.resetboard:
            self.scene.board.resetBoard()
            for x,row in enumerate(self.scene.numGrid):
                for y,i in enumerate(row):

                    if (x,y) not in self.scene.defaultSet:
                        self.scene.numGrid[x][y].setDefaultTextColor(QColor(0,0,0))
                        self.scene.numGrid[x][y].setPlainText("")


        elif action == self.solveboard:
            self.scene.board.solveBoard()

            for x,row in enumerate(self.scene.numGrid):
                for y,i in enumerate(row):
                    #scene.numGrid[y][x].setDefaultTextColor(QColor(0,0,0))
                    self.scene.numGrid[x][y].setPlainText(str(self.scene.board.grid[x][y]))


class guess2Window(QWidget):

    def __init__(self,viewer):
        super().__init__()

        self.viewer = viewer
        self.numchecked = 0
        self.guessed = []
        self.initGui()
        self.guess = False

    def initGui(self):

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

        self.cmenu = QMenu(self)

        self.guessAct = QAction("Guess", self)
        self.guessAct.setStatusTip('For when you\'re not sure')
        self.guessAct.setCheckable(True)
        self.cmenu.addAction(self.guessAct)

        grid = QGridLayout()
        count = 1
        for x in range(3):
            for y in range(3):
                button = QPushButton(str(count))
                button.setFixedSize(60,60)
                button.clicked.connect(self.buttonClicked)
                grid.addWidget(button, x, y)
                count += 1
        self.setLayout(grid)
        self.setGeometry(300,300,200,200)

    def mousePressEvent(self,e):
        pass


    def buttonClicked(self):

        if self.guess == False:

            self.sender = self.sender()
            self.viewer.scene.numGrid[self.viewer.gridRow][self.viewer.gridCol].setDefaultTextColor(QColor(0,0,0))
            self.viewer.scene.numGrid[self.viewer.gridRow][self.viewer.gridCol].setPlainText(self.sender.text())
            self.viewer.scene.board.grid[self.viewer.gridRow][self.viewer.gridCol] = int(self.sender.text())
            for i in self.viewer.scene.possNums[self.viewer.gridRow][self.viewer.gridCol]:
                i.setPlainText("")
            self.close()

        else:
            sender = self.sender()
            if sender.text() not in self.guessed:

                self.viewer.scene.possNums[self.viewer.gridRow][self.viewer.gridCol][self.numchecked].setPlainText(sender.text())
                self.numchecked+=1
                if self.numchecked == 4: self.numchecked = 0
                self.guessed.append(sender.text())
            else:

                self.guessed.remove(sender.text())
                for textObj in self.viewer.scene.possNums[self.viewer.gridRow][self.viewer.gridCol]:
                    if textObj.toPlainText() == sender.text():
                        textObj.setPlainText("")
                        self.numchecked -= 1
                        break

    def onContextMenu(self, pos):

        action = self.cmenu.exec_(self.mapToGlobal(pos))

        if action == self.guessAct:
            self.guess = not self.guess
            checkstat = self.guessAct.isChecked()
            if checkstat == True:
                self.guessAct.setChecked(True)
            else:
                self.guessAct.setChecked(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = Board()
    scene = Scene(board)
    view = Viewer(scene)
    #view.setScene(scene)

    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    sys.exit(app.exec_())
