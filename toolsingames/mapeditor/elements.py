#!/usr/bin/env python

# Import UI subsystem
from PySide import QtGui, QtCore

# Our basic block is 40x32 px
BLOCK_SIZE_X=40
BLOCK_SIZE_Y=32

class BlockRenderer(QtGui.QGraphicsItem):
    """
    Base block renderer, all items inherit from this one
    """
    def __init__(self, mainWindow, canvas, x, y, asset=None, xspan=1, yspan=1):
        QtGui.QGraphicsItem.__init__(self)

        # The QMainWindow
        self.mainWindow=mainWindow

        # The QGraphicsView
        self.canvas=canvas

        self.gbcolor=QtGui.QColor(255, 0, 0, 128)

        # Set size and position of the itemt
        self.xl=BLOCK_SIZE_X*xspan
        self.yl=BLOCK_SIZE_Y*yspan
        self.x=x
        self.y=y+(yspan-1)
        self.xspan=xspan
        self.yspan=yspan

        # Used asset :D
        self.asset=asset

        # Define th size of the item
        self._rect=QtCore.QRectF(QtCore.QPoint(self.x*self.xl, -self.y*self.yl), QtCore.QSize(self.xl, self.yl))
        self._rect.translate(QtCore.QPointF(0,self.yl))

        # Enable hoover and mouse events
        self.is_hoover=False
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return self._rect

    def paint(self, painter, option, widget):
        # Save painter state
        painter.save()

        # Draw background, just a gray rect nothing more
        painter.fillRect(self._rect,QtCore.Qt.darkCyan)
        painter.drawRect(self._rect)

        # Draw an empty block or the block image
        if self.asset == None:
            painter.fillRect(self._rect,QtCore.Qt.darkCyan)
            painter.drawRect(self._rect)
        else:
            painter.drawImage(self._rect, self.asset)
            #painter.drawText(self._rect, QtCore.Qt.AlignCenter, "(%d,%d)"%(self.x,self.y))
            #painter.drawRect(self._rect)

        # Draw the hoover graphic. Should represent the action on for the next click
        if self.is_hoover:
            painter.fillRect(self._rect.left(), self._rect.top(), BLOCK_SIZE_X, BLOCK_SIZE_Y, self.gbcolor)
            #painter.drawText(self._rect, QtCore.Qt.AlignCenter, "AA")

        # Restore painter state
        painter.restore()

    def hoverEnterEvent(self, event):
        self.is_hoover=True
        self.scene().update()

    def hoverLeaveEvent(self, event):
        self.is_hoover=False
        self.scene().update()
