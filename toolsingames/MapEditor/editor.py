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

class BlockRenderer(QtGui.QGraphicsItem):
    def __init__(self, mainWindow, canvas, x, y, asset=None, xl=40, yl=32):
        QtGui.QGraphicsItem.__init__(self)

        # The QMainWindow
        self.mainWindow=mainWindow

        # The QGraphicsView
        self.canvas=canvas

        # Set size and position of the item
        self.x=x
        self.y=y
        self.xl=xl
        self.yl=yl

        # Used asset :D
        self.asset=asset

        # Define th size of the item
        self._rect=QtCore.QRectF(QtCore.QPoint(self.x*self.xl, -self.y*self.yl), QtCore.QSize(self.xl, self.yl))

    def boundingRect(self):
        return self._rect

    def paint(self, painter, option, widget):
        # Save painter state
        painter.save();

        if self.asset == None:
            painter.drawText(self._rect, QtCore.Qt.AlignCenter, "(%d,%d)"%(self.x,self.y))
            painter.drawRect(self._rect)
        else:
            painter.drawImage(self._rect, self.asset)

        # Restore painter state
        painter.restore();

class MapEditor(QtGui.QMainWindow, Ui_MapEditor):
    def __init__(self, parent=None):
        super(MapEditor, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("assets/icon.png"))

        print("Working Directory: %s"%(WORKING_DIR))

        # Create our asset manager
        self.assetManager = AssetManager(WORKING_DIR)

        # Load all tiles in
        #self.tilesDir=os.path.join(WORKING_DIR,'assets','tiles')
        #for tile in os.listdir(self._tilesDir):
        #    self.assetManager.load_asset(os.path.join(self.tilesDir,tile)

        # Create the canvas :D
        self.scene = GraphicsScene()  
        self.graphicsView = GraphicsView(self.scene)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)

        # Add the level renderer
        self.scene.addItem(BlockRenderer(self, self.graphicsView,0,0,self.assetManager.get_asset("tiles/BlockA0.png")))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,1,0))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,2,0))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,3,0))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,4,0))

        self.scene.addItem(BlockRenderer(self, self.graphicsView,0,1))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,1,1))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,2,1))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,3,1))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,4,1))

        self.scene.addItem(BlockRenderer(self, self.graphicsView,0,2))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,1,2))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,2,2))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,3,2))
        self.scene.addItem(BlockRenderer(self, self.graphicsView,4,2))

def main(vargs):
    app = QtGui.QApplication(sys.argv)
    frame = MapEditor()
    frame.show()
    app.exec_()
        
if __name__ == '__main__':
    main(sys.argv)
    print("See you again soon :D")
