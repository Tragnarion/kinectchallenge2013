#!/usr/bin/env python

import random

# Import UI subsystem
from PySide import QtGui, QtCore

# Our basic block is 40x32 px
BLOCK_SIZE_X=40
BLOCK_SIZE_Y=32

class BlockRenderer(QtGui.QGraphicsItem):
    """
    Base class used to render a section of the game grid
    """
    def __init__(self, mainWindow, x, y, asset=None, xspan=1, yspan=1):
        QtGui.QGraphicsItem.__init__(self)

        # The QMainWindow
        self.mainWindow=mainWindow

        # The QGraphicsView
        self.canvas=mainWindow.graphicsView

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
        self._rect=QtCore.QRectF(QtCore.QPoint(0, 0), QtCore.QSize(self.xl, self.yl))
        self._rect.moveCenter(QtCore.QPointF(self.x*BLOCK_SIZE_X+(xspan-1)*BLOCK_SIZE_X*0.5, -self.y*BLOCK_SIZE_Y+(yspan-1)*BLOCK_SIZE_Y*0.5))

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
            painter.fillRect(self._rect.left(), self._rect.top(), self.xl, self.yl, self.gbcolor)
            #painter.drawText(self._rect, QtCore.Qt.AlignCenter, "AA")

        # Restore painter state
        painter.restore()

    def hoverEnterEvent(self, event):
        self.is_hoover=True
        self.scene().update()

    def hoverLeaveEvent(self, event):
        self.is_hoover=False
        self.scene().update()

class BaseBlock(BlockRenderer):
    """
    Base block renderer, all items inherit from this one
    """
    def __init__(self, mainWindow, x, y, xspan=1, yspan=1):
        BlockRenderer.__init__(self, mainWindow, x, y, self._get_asset(mainWindow), xspan, yspan)

    def _get_asset(self, mainWindow):
        return mainWindow.assetManager.get_asset(self._get_asset_base_name());

    def _get_asset_base_name(self):
        return ""

class BlockA(BaseBlock):
    """
    Block of type A. Uses random assets.
    """
    def _get_asset_base_name(self):
        return "tiles/BlockA%d.png"%(random.randint(0, 6));

class BlockB(BaseBlock):
    """
    Block of type B. Uses random assets.
    """
    def _get_asset_base_name(self):
        return "tiles/BlockB%d.png"%(random.randint(0, 1));

class Platform(BaseBlock):
    """
    A platform block
    """
    def _get_asset_base_name(self):
        return "tiles/Platform.png";

class Exit(BaseBlock):
    """
    The exit block
    """
    def _get_asset_base_name(self):
        return "tiles/Exit.png";

class Actor(BaseBlock):
    """
    Base actor block, a player or a monster for example
    """
    def __init__(self, mainWindow, x, y, xspan=1, yspan=2):
        BaseBlock.__init__(self, mainWindow, x, y, xspan, yspan)

    def _get_asset_base_name(self):
        return "tiles/MonsterA.png";
