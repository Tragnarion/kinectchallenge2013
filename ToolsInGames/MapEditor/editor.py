#!/usr/bin/env python

import sys
import platform
import os

# Import UI subsystem
from PySide import QtGui, QtCore
from ui.main import Ui_MapEditor
from assets import AssetManager

import utils

WORKING_DIR = os.getcwd()

class GraphicsScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
    
    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        
class GraphicsView(QtGui.QGraphicsView):
    def __init__(self, parent=None, gbcolor=QtGui.QColor('#CCCCCC'), space=10):
        super(GraphicsView, self).__init__(parent)
        
        self.bgcolor = gbcolor
        self.space = space
        self.background = None
        
        # This fixes the scroll issue but the bounding is not correct
        #self.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
    
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
        self.scene = GraphicsScene()  
        self.graphicsView = GraphicsView(self.scene)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)

def main(vargs):
    app = QtGui.QApplication(sys.argv)
    frame = MapEditor()
    frame.show()
    app.exec_()
        
if __name__ == '__main__':
    main(sys.argv)
    print("See you again soon :D")
