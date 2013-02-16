#!/usr/bin/env python

import sys
import platform
import os

# Import UI subsystem
from PySide import QtGui, QtCore
from ui.main import Ui_MapEditor
from assets import AssetManager
import elements

import utils

WORKING_DIR = os.getcwd()
INDEX_NONE = -1

class EditorScene(QtGui.QGraphicsScene):
    def __init__(self, main_window=None):
        super(EditorScene, self).__init__(main_window)

        # The window ref
        self.main_window=main_window

        # Both of list represented in row major order.
        # The scene matrix is created listing the items starting at (0,0)
        self.scene_matrix=[]
        # Precomputed length, use it with care!!
        self.scene_matrix_length=0

        # We start with an empty scene
        self.scene_height=0
        self.scene_width=0

    def initialize_scene(self):
        self._recreate_scene(0,0)

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)

    def _get_index(self,x,y,width):
        return y*width+x
    
    def valid_pos(self, x, y):
        index=self._get_index(x,y,self.scene_width)
        if self.scene_matrix_length > 0 and index < self.scene_matrix_length:
            return index
        return INDEX_NONE

    def get_element(self, x, y):
        index = self.valid_pos(x,y)
        if index != INDEX_NONE:
            return self.scene_matrix[index]
        return None

    def add_element(self, element, x, y):
        """
        Look if the index does exists for the given item
        if so just add/replace the existing block with it
        """
        index = self.valid_pos(x,y)
        if index != INDEX_NONE:
            # Add the element at the given position
            self.scene_matrix[index]=element
            self.addItem(element)

    def add_row(self):
        self._recreate_scene(self.scene_width,self.scene_height+1)

    def add_col(self):
        self._recreate_scene(self.scene_width+1,self.scene_height)

    def remove_row(self, y):
        # Remove all items from the scene and null the scene ref
        for i in range(0,self.scene_width):
            index = self._get_index(i, y, self.scene_width)
            self.removeItem(self.scene_matrix[index])
            self.scene_matrix[index]=None
        self._clean_null_elements()

    def remove_col(self, x):
        """
        Remove all items from the scene and null the scene ref
        """
        for i in range(0,self.scene_height):
            index = self._get_index(x, i, self.scene_width)
            self.removeItem(self.scene_matrix[index])
            self.scene_matrix[index]=None
        self._clean_null_elements()

    def _clean_null_elements(self):
        """
        Remove all items from the scene matrix iterating from 
        the end of the list removing None entries
        """
        for element in reversed(self.scene_matrix):
            self.scene_matrix.remove(element)
        self.scene_matrix_length=len(self.scene_matrix)

    def _recreate_scene(self,new_width=0,new_height=0):
        # Recreate the scene and rebuild items
        bInitialize=False
        old_width=self.scene_width
        old_height=self.scene_height
        if new_width == 0 and new_height == 0:
            self.scene_height=1
            self.scene_width=1
            bInitialize=True
        else:
            self.scene_height=new_height
            self.scene_width=new_width

        # Save the old matrix
        old_scene_matrix=self.scene_matrix
        self.scene_matrix_length=self.scene_width*self.scene_height
        self.scene_matrix=[None]*self.scene_matrix_length

        if bInitialize:
            # just add an empty block
            self.add_element(elements.EMPTY_BLOCK(self.main_window,0,0),0,0)
        else:
            # Repleace all none elements with empty blocks. We will
            # iterate over the whole matrix so this method will be felixble.
            # If we have already an element in the old matrix re-use it :D
            for col in range(0,self.scene_width):
                for row in range(0,self.scene_height):
                    element = None
                    if col < old_width and row < old_height:
                        element = old_scene_matrix[self._get_index(col,row,old_width)]
                        # TODO: We should not remove-add an existing item!
                        self.removeItem(element)
                    if element == None:
                        element = elements.EMPTY_BLOCK(self.main_window,col,row)
                    self.add_element(element,col,row)
        
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
        """
        Draw the rectangle background
        """
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

class ToolSet(QtGui.QPushButton):
    def __init__(self, element_class, main_window=None):
        QtGui.QPushButton.__init__(self,main_window)

        self.element_class = element_class
        # Create the default object instance, this is just used to perform
        # operations on an element
        self.element_instance = None
        if self.element_class:
            self.element_instance = self.element_class(main_window,0,0)

        # We should hold a ref to the window itself
        self.main_window = main_window

        if self.element_instance:
            icon = self.element_instance.get_tool_icon()
            if icon:
                self.setIcon(icon)
            text = self.element_instance.get_tool_name()
            if text:
                self.setText(text)

        # Connect the clicked dignal
        self.clicked.connect(self._tool_clicked)

    def _tool_clicked(self):
        """
        Route call to default instance
        """
        if self.element_instance:
            self.element_instance.tool_clicked(self)

    def can_element_clicked(self, element):
        """
        Decide if we can click the given element
        """
        if self.element_instance:
            return self.element_instance.element_clicked(element)
        return False
    def element_clicked(self, element):
        """
        Route the call back to the element itself.
        I know that is is a loop-back but this way we can
        cut the flow in case we need it :D
        """
        if self.can_element_clicked(element) and self.element_instance:
            return self.element_instance.element_clicked(element)

    def get_tool_name(self):
        if self.element_instance:
            return self.element_instance.get_tool_name()
        return "Tool: None"

class MapEditor(QtGui.QMainWindow, Ui_MapEditor):
    def __init__(self, parent=None):
        super(MapEditor, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("assets/icon.png"))

        print("Working Directory: %s"%(WORKING_DIR))

        # Create our asset manager
        self.assetManager = AssetManager(WORKING_DIR)
        self.assetManager.load_asset("deny.png")

        # Create the canvas :D
        self.scene = EditorScene(self)  
        self.graphicsView = GraphicsView(self.scene)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)

        # We can now initialize the scene
        self.scene.initialize_scene()

        # The tool that is currently active
        self.current_tool=None
        self.current_status=None

        # Init all available tools
        self.initialize_tools()

    def initialize_tools(self):
        self.toolSetLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)

        # Add tool status
        self.current_status = QtGui.QLabel("Tool: None", self)
        self.toolSetLayout.addWidget(self.current_status)

        # Add world building elements
        self._add_tool_section("Brushes:",elements.ELEM_BRUSH_CLASSES)
        self._add_tool_section("Player:",elements.ELEM_PLAYER_CLASSES)
        self._add_tool_section("Building:",elements.ELEM_WORLD_CLASSES)
        self._add_tool_section("Enemies:",elements.ELEM_ENEMY_CLASSES)
        self._add_tool_section("Power-Ups:",elements.ELEM_POWERUP_CLASSES)

    def _add_tool_section(self, title, tools):
        self.toolSetLayout.addWidget(QtGui.QLabel(title, self))
        i=0
        for tool in tools:
            # Create a new horizontal layout for every 2 tools
            if i == 0:
                currentContainer = QtGui.QWidget(self.centralwidget)
                currentSetLayout = QtGui.QHBoxLayout(currentContainer)
                self.toolSetLayout.addWidget(currentContainer)
            currentSetLayout.addWidget(ToolSet(tool, self))
            i=(i+1)%2

    def set_current_tool(self, tool):
        self.current_tool = tool
        self.current_status.setText("Tool: %s"%tool.get_tool_name())

    def element_clicked(self, element):
        if self.current_tool:
            self.current_tool.element_clicked(element)

def main(vargs):
    app = QtGui.QApplication(sys.argv)
    frame = MapEditor()
    frame.show()
    app.exec_()
        
if __name__ == '__main__':
    main(sys.argv)
    print("See you again soon :D")
