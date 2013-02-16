#!/usr/bin/env python

import sys
import platform
import os

# Import UI subsystem
from PySide import QtGui, QtCore
from ui.main import Ui_MapEditor
from assets import AssetManager
from elements import *

import utils

WORKING_DIR = os.getcwd()

class EditorScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(EditorScene, self).__init__(parent)
    
    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)

    # TODO: Add methods to add an block and then create empty blocks near them.
    #       Adding a block should be done by a mouse-click selecting a tool
    #       from the tools pane on the left. The idea is to maintain always
    #       a rectangle of blocks. An empty base block represents a hole in the
    #       map where the player will explode!
        
class GraphicsView(QtGui.QGraphicsView):
    def __init__(self, parent=None, gbcolor=QtGui.QColor('#CCCCCC'), space=10):
        super(GraphicsView, self).__init__(parent)
        
        self.bgcolor = gbcolor
        self.space = space
        self.background = None
        
        # Full update
        self.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
    
    def resizeEvent(self, event):
        QtGui.QGraphicsView.resizeEvent(self,event)
        
    def drawBackground(self, painter, rect):        
        # Draw the rectangle background
        left = rect.left()
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()
        xPos = left
        iteration = 0
        while xPos < right:
            yPos = top
            if iteration % 2 == 0:
                yPos += self.space
            while yPos < bottom:
                painter.fillRect(xPos,yPos,self.space,self.space,self.bgcolor)
                yPos += self.space*2
            xPos += self.space
            iteration += 1

class MapEditor(QtGui.QMainWindow, Ui_MapEditor):
    def __init__(self, parent=None):
        super(MapEditor, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("assets/icon.png"))

        print("Working Directory: %s"%(WORKING_DIR))

        # Create our asset manager
        self.assetManager = AssetManager(WORKING_DIR)

        # Create the canvas :D
        self.scene = EditorScene()  
        self.graphicsView = GraphicsView(self.scene)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)

        # Create a button for all available blocks
        self.toolSetLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        #button = QtGui.QPushButton("&Download", self)
        #button.setIcon(self.assetManager.get_asset("assets/icon.png"))
        self.toolSetLayout.addWidget(QtGui.QLabel("Brushes:", self))

        for i in range(0,100):
            currentContainer = QtGui.QWidget(self.centralwidget)
            currentSetLayout = QtGui.QHBoxLayout(currentContainer)
            currentSetLayout.addWidget(QtGui.QPushButton("Erease", self))
            currentSetLayout.addWidget(QtGui.QPushButton("Blank", self))
            self.toolSetLayout.addWidget(currentContainer)

        # Add the level renderer
        self.scene.addItem(BlockA(self,0,0))
        self.scene.addItem(BlockB(self,1,0))
        self.scene.addItem(BlockA(self,2,0))
        self.scene.addItem(BlockA(self,3,0))
        self.scene.addItem(BlockB(self,4,0))
        self.scene.addItem(BlockB(self,5,0))
        self.scene.addItem(BlockB(self,6,0))
        self.scene.addItem(BlockB(self,7,0))

        self.scene.addItem(Player(self,0,1))
        self.scene.addItem(EmptyBlock(self,1,1))
        self.scene.addItem(EmptyBlock(self,2,1))
        self.scene.addItem(EmptyBlock(self,3,1))
        self.scene.addItem(MonsterA(self,4,1))

        #self.scene.addItem(EmptyBlock(self,0,2))
        self.scene.addItem(EmptyBlock(self,1,2))
        self.scene.addItem(Platform(self,2,2))
        self.scene.addItem(Platform(self,3,2))
        #self.scene.addItem(EmptyBlock(self,4,2))

        self.statusBar().showMessage("Current Tool: Erease")

def main(vargs):
    app = QtGui.QApplication(sys.argv)
    frame = MapEditor()
    frame.show()
    app.exec_()
        
if __name__ == '__main__':
    main(sys.argv)
    print("See you again soon :D")
