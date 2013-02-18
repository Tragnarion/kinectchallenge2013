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

        self.overlay_color=QtGui.QColor(255, 0, 0, 128)

        # Set size and position of the itemt
        self.xl=BLOCK_SIZE_X*xspan
        self.yl=BLOCK_SIZE_Y*yspan
        self.x=x
        self.y=y
        self.xspan=xspan
        self.yspan=yspan

        # Used asset :D
        self.asset=asset

        # Define th size of the item
        self._rect=QtCore.QRectF(QtCore.QPoint(0, 0), QtCore.QSize(self.xl, self.yl))
        self._rect.moveCenter(QtCore.QPointF(self.x*BLOCK_SIZE_X+(xspan-1)*BLOCK_SIZE_X*0.5, -(self.y+(yspan-1))*BLOCK_SIZE_Y+(yspan-1)*BLOCK_SIZE_Y*0.5))

        # Enable hoover and mouse events
        self.is_hoover=False
        self.is_clickable=True
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(True)

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
        elif isinstance(self.asset,QtGui.QImage):
            painter.drawImage(self._rect, self.asset)

        # Show the overlay state
        if not self.is_clickable:
            painter.drawImage(self._rect, self.mainWindow.assetManager.get_asset("deny.png"))
        elif self.is_hoover:
            painter.fillRect(self._rect.left()+1, self._rect.top()+1, self.xl-1, self.yl-1, self.overlay_color)

        # Restore painter state
        painter.restore()

    def hoverEnterEvent(self, event):
        self.is_hoover=True
        self.scene().update()
        self.mainWindow.statusBar().showMessage("Element: %s"%self.get_tool_name())

    def hoverLeaveEvent(self, event):
        self.is_hoover=False
        self.scene().update()

    def mousePressEvent(self, event):
        """
        Called when the item receives a mouse press
        """
        self.mainWindow.element_clicked(self)

    def element_clicked(self, element):
        """
        A tool has received a click from an element. The tool just redirected the call to us
        so we can perform any required action over the element
        """
        raise NotImplementedError("A base block must implement the 'element_clicked' method")

    def convert_element(self, old_element):
        """
        Convert the old_element into a block of our own class. Before getting rid of the old
        one let the new one copy any data over
        """
        new_element=self._create_new_element(old_element.mainWindow, old_element.x, old_element.y, old_element.xspan, old_element.yspan, old_element)
        new_element.copy_from(old_element)
        self.mainWindow.scene.add_element(new_element, new_element.x, new_element.y)

    def _create_new_element(self, mainWindow, x, y, xspan, yspan, old_element):
        return self.__class__(mainWindow, x, y, xspan, yspan)

    def copy_from(self, old_element):
        """
        Once an old element has been turned into our-selfs we have the opportunity to copy
        any data from it to persist it.
        """
        pass

    def tool_clicked(self, tool):
        """
        The user selected the default instance element as the current tool
        """
        self.mainWindow.set_current_tool(tool)

    def get_id_char(self):
        """
        Return the character that represents the block in a level
        """
        raise NotImplementedError("A base block must implement the 'get_id_char' method")

    def get_tool_icon(self):
        """
        Return the icon used for the tool set for this block
        """
        raise NotImplementedError("A base block must implement the 'get_tool_icon' method")

    def get_tool_name(self):
        """
        Return the name used for the tool set for this block
        """
        raise NotImplementedError("A base block must implement the 'get_tool_name' method")

class EmptyBlock(BlockRenderer):
    """
    Just an empty block
    """
    def get_id_char(self):
        """
        Return the character that represents the block in a level
        """
        return '.'

    def get_tool_icon(self):
        return None

    def get_tool_name(self):
        return "Blank"

    def element_clicked(self, element):
        if isinstance(element,self.__class__):
            return
        # Convert block into one of our own type
        self.convert_element(element)

class EreaseRow(BlockRenderer):
    """
    Just an empty block
    """
    def get_id_char(self):
        """
        Return the character that represents the block in a level
        """
        return '.'

    def get_tool_icon(self):
        return None

    def get_tool_name(self):
        return "Erease Row"

    def element_clicked(self, element):
        # Not finished!
        #self.mainWindow.scene.remove_row(element.y)
        pass

class EreaseColumn(BlockRenderer):
    """
    Just an empty block
    """
    def get_id_char(self):
        """
        Return the character that represents the block in a level
        """
        return '.'

    def get_tool_icon(self):
        return None

    def get_tool_name(self):
        return "Erease Col"

    def element_clicked(self, element):
        # Not finished!
        #self.mainWindow.scene.remove_col(element.x)
        pass

class AddRow(BlockRenderer):
    """
    Just an empty block
    """
    def get_id_char(self):
        """
        Return the character that represents the block in a level
        """
        return '.'

    def get_tool_icon(self):
        return None

    def get_tool_name(self):
        return "Add Row"

    def tool_clicked(self, tool):
        """
        Add a row to the scene matrix
        """
        self.mainWindow.scene.add_row()

class AddColumn(BlockRenderer):
    """
    Just an empty block
    """
    def get_id_char(self):
        """
        Return the character that represents the block in a level
        """
        return '.'

    def get_tool_icon(self):
        return None

    def get_tool_name(self):
        return "Add Col"

    def tool_clicked(self, tool):
        """
        Add a column to the scene matrix
        """
        self.mainWindow.scene.add_col()

class BaseBlock(BlockRenderer):
    """
    Base block renderer, all items inherit from this one
    """
    def __init__(self, mainWindow, x, y, xspan=1, yspan=1):
        BlockRenderer.__init__(self, mainWindow, x, y, self.get_asset(mainWindow), xspan, yspan)

    def get_asset(self, mainWindow):
        return mainWindow.assetManager.get_asset(self._get_asset_base_name());

    def get_tool_icon(self):
        return QtGui.QIcon("assets/%s"%self._get_asset_base_name())

    def _get_asset_base_name(self):
        raise NotImplementedError("A base block must implement the '_get_asset_base_name' method")

    def element_clicked(self, element):
        if isinstance(element,self.__class__):
            return
        # Convert block into one of our own type
        self.convert_element(element)

class BlockA(BaseBlock):
    """
    Block of type A. Uses random assets.
    """
    def _get_asset_base_name(self):
        return "tiles/BlockA%d.png"%(random.randint(0, 6));

    def get_tool_name(self):
        return "Block A"

class BlockB(BaseBlock):
    """
    Block of type B. Uses random assets.
    """
    def _get_asset_base_name(self):
        return "tiles/BlockB%d.png"%(random.randint(0, 1));

    def get_tool_name(self):
        return "Block B"

class Platform(BaseBlock):
    """
    A platform block
    """
    def _get_asset_base_name(self):
        return "tiles/Platform.png";

    def get_tool_name(self):
        return "Platform"

class Exit(BaseBlock):
    """
    The exit block
    """
    def _get_asset_base_name(self):
        return "tiles/Exit.png";

    def get_tool_name(self):
        return "Exit"

class Actor(BaseBlock):
    """
    Base actor block, a player or a monster for example
    """
    pass

class Monster(Actor):
    """
    The monster actor
    """
    pass

class MonsterA(Monster):
    """
    A monster of type A
    """
    def _get_asset_base_name(self):
        return "tiles/MonsterA.png";

    def get_tool_name(self):
        return "Monster A"

class MonsterB(Monster):
    """
    A monster of type B
    """
    def _get_asset_base_name(self):
        return "tiles/MonsterB.png";

    def get_tool_name(self):
        return "Monster B"

class MonsterC(Monster):
    """
    A monster of type C
    """
    def _get_asset_base_name(self):
        return "tiles/MonsterC.png";

    def get_tool_name(self):
        return "Monster C"

class MonsterD(Monster):
    """
    A monster of type D
    """
    def _get_asset_base_name(self):
        return "tiles/MonsterD.png";

    def get_tool_name(self):
        return "Monster D"

class Player(Actor):
    """
    The player class
    """
    def _get_asset_base_name(self):
        return "tiles/Player.png";

    def get_tool_name(self):
        return "Player"

class PowerUp(Actor):
    """
    The base power-up class
    """
    def _get_asset_base_name(self):
        return "tiles/Gem.png";

class Gem(PowerUp):
    """
    A normal gem
    """
    def get_tool_name(self):
        return "Gem"

class RedGem(PowerUp):
    """
    A normal gem
    """
    def get_tool_name(self):
        return "Red Gem"

# List of spawnable elements
ELEM_CLASSES=(\
    EmptyBlock,\
    BlockA,\
    BlockB,\
    Platform,\
    Exit,\
    MonsterA,\
    MonsterB,\
    MonsterC,\
    MonsterD,\
    Player\
    )

# The empty block class, used to start a level
EMPTY_BLOCK=EmptyBlock

# Building block list
ELEM_BRUSH_CLASSES=(\
    EreaseRow,\
    EreaseColumn,\
    AddRow,\
    AddColumn,\
    EmptyBlock\
    )

# Building block list
ELEM_WORLD_CLASSES=(\
    BlockA,\
    BlockB,\
    Platform,\
    )

# List of enemies
ELEM_ENEMY_CLASSES=(\
    MonsterA,\
    MonsterB,\
    MonsterC,\
    MonsterD\
    )

# List of building blocks
ELEM_PLAYER_CLASSES=(\
    Player,\
    Exit\
    )

# List of building blocks
ELEM_POWERUP_CLASSES=(\
    Gem,\
    RedGem\
    )