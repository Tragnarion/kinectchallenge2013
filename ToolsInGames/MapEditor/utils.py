#!/usr/bin/env python

import os

# Import UI subsystem
from PySide import QtGui

# ----------------------------------------------------------------------
# File Handling
# ----------------------------------------------------------------------

def file_openFileDialog(parent, title, directory, filter):
    return QtGui.QFileDialog.getOpenFileName(parent, title, directory, filter)[0]

def file_getExistingDirectory(parent, title, directory):
    return QtGui.QFileDialog.getExistingDirectory(parent, title, directory, options=QtGui.QFileDialog.ShowDirsOnly)

# ----------------------------------------------------------------------
# Dialog Handling
# ----------------------------------------------------------------------
def dialog_input_getText(parent,title,label,text=""):
    return QtGui.QInputDialog.getText(parent, title, label, QtGui.QLineEdit.Normal, text)

# ----------------------------------------------------------------------
# XMl Handling
# ----------------------------------------------------------------------

def xml_getXMLAttribute(xmlElement, name, default):
    return xmlElement.attribute(name,str(default))

# ----------------------------------------------------------------------
# Interpolation Handling
# ----------------------------------------------------------------------

def lerp(value1,value2,alpha):
    return value1+(value2-value1)*alpha

# ----------------------------------------------------------------------
# Type Handling
# ----------------------------------------------------------------------

def str2bool(s):
    return s.lower() in ['true', 'True', '1', 't', 'y', 'yes', 'yeah', 'yup', 'yep', 'si', 'ja', 'certainly', 'uh-huh']

def bool2str(b):
    if b:
        return "true"
    return "false"

def hex2int(s):
    return int(s, 16)

def hexcolor2int(s):
    return hex2int(s.replace('#',''))
    
def int2hex(n):
    return "%X" % n

def int2hexcolor(n):
    return "#%X" % n

# ----------------------------------------------------------------------
# IO Handling
# ----------------------------------------------------------------------

def makeOsPath(path):
    """Make the current path using the OS path separator"""
    return path.replace('/',os.sep)
    
def makeUnixPath(path):
    """Make a given OS path using the unix path separator"""
    return path.replace(os.sep,'/')
    
def createFolderConditional(path):
    """Creates a folder given an absolute path if the folder does not exists. Returns the path again"""
    if not os.path.exists(path):
        os.makedirs(path)
    return path