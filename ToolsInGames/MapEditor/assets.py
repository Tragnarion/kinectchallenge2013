#!/usr/bin/env python

# base imports
import os

# Import UI subsystem
from PySide import QtGui

class AssetNotSupportedException(Exception):
    pass

class AssetFileNotFoundException(Exception):
    pass
    
class AssetLoadException(Exception):
    pass

class AssetNotFoundException(Exception):
    pass

class Asset():
    def __init__(self, absolutePath, asset):
        self.absolutePath = absolutePath
        self.asset = asset
        
class AssetManager():
    def __init__(self, baseDir):
        self._baseDir = baseDir
        self._assetDict = {}
        self._assetBasePath = os.path.join(self._baseDir,"assets")
        self._tilesBasePath = os.path.join(self._assetBasePath,"tiles")
        
        # This should come from a plugin subsystem... but for now it's ok
        self._assetLoaders = {
                'PNG': self._loadPNG,
            }
        self._assetUnloaders = {
                'PNG': self._unloadPNG,
            }

        # Load all tiles in
        for tile in os.listdir(self._tilesBasePath):
            self.load_asset("tiles/%s"%tile)
        
    
    # ------------------------------------------------------------------
    # Create a real asset
    # ------------------------------------------------------------------
    
    def _createAsset(self, assetPath):
        if not os.path.exists(assetPath):
            raise AssetFileNotFoundException("Asset file '%s' does not exist!"%(assetPath))
            
        extension = os.path.splitext(assetPath)[1].upper()[1:]
        if extension in self._assetLoaders:
            return self._assetLoaders[extension](assetPath)
        else:
            raise AssetNotSupportedException("No loader found for asset '%s'!"%(assetPath))
    
    # ------------------------------------------------------------------
    # Image loaders
    # ------------------------------------------------------------------
    
    def _loadPNG(self, assetPath):
        return self._loadImage(assetPath)
        
    def _unloadPNG(self, asset):
        return True
            
    def _loadImage(self, assetPath):
        finalAsset = QtGui.QImage()
        if not finalAsset.load(assetPath):
            raise AssetLoadException("Asset '%s' is not am image or is corrupted!"%(assetPath))
        return finalAsset
    
    # ------------------------------------------------------------------
    # Return and create an asset
    # ------------------------------------------------------------------
    
    def get_asset(self, assetPath):
        if assetPath in self._assetDict:
            return self._assetDict[assetPath].asset
        raise AssetNotFoundException("'%s' asset could not be found!"%(assetPath))
            
    def load_asset(self, assetPath, basePath=""):
        if assetPath in self._assetDict:
            return self._assetDict[assetPath]
         
        # Set base path
        if not basePath:
            basePath = self._assetBasePath;
        
        # Create new asset
        absolutePath = os.path.join(basePath, assetPath)
        self._assetDict[assetPath] = Asset(absolutePath, self._createAsset(absolutePath) )
    
    def release_asset(self, assetPath):
        if assetPath in self._assetDict:
            extension = os.path.splitext(assetPath)[1].upper()[1:]
            if extension in self._assetUnloaders:
                res = self._assetUnloaders[extension](self._assetDict[assetPath])
                del self._assetDict[assetPath]
                return res
            else:
                raise AssetNotSupportedException("No unloader found for asset '%s'!"%(assetPath))
        print("Can not release an asset that has not been laoded...")
        return False