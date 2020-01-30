"""
Created on 06.03.2018

@author: Christian Ott
"""

import logging.handlers
logger = logging.getLogger(__name__)

import os
from pathlib import Path
import copy
import sys

from PyQt5 import QtWidgets

import Base.Errors as errs
from Base.AppSettings import AppSettings
from Base.MachineBase import MachineBase

#from Machines import TinyG


class AppBase(object):
    """
    This static class handles base application variables and functions.
    """
    
    version = "1.31 Build 022"
    
    mainwindow = None
    settings = AppSettings()
    machine = MachineBase()
    workpiece = None
    workpieceOriginal = None
    workpieceMirrored = False
    appdata = None
    
    
    @classmethod 
    def initialize(cls):
        """
        Initialize base application and read application settings.
        """
        # initialize application data directory
        cls.appdata = Path(os.getenv("LOCALAPPDATA", os.getenv("APPDATA")))
        cls.appdata /= "ESCMillPCB"
        if not cls.appdata.exists():
            cls.appdata.mkdir()
            
        # load application settings
        settingsfile = cls.appdata / "settings.json"
        if settingsfile.exists():
            cls.settings.loadSettings(settingsfile)
        else:
            cls.settings.loadDefaults()
            
        # apply logger settings
        loghandler = logging.handlers.TimedRotatingFileHandler(
            cls.appdata / "logfile.log",
            when="midnight",
            backupCount=cls.settings.value('General', 'logfile_backups')
        )
        formatter = logging.Formatter("%(asctime)s %(levelname)s:%(name)s: %(message)s")
        loghandler.setFormatter(formatter)
        loghandler.setLevel(cls.settings.value('General', 'logfile_level'))
        logging.getLogger().addHandler(loghandler)
        
        cls.changeMachine(cls.settings.value('MachineBaseHidden', 'machine_name'), signal=False)
    
    
    @classmethod
    def finalize(cls):
        """
        Finalize base application and save application settings.
        """
        cls.getSettings().saveSettings(cls.appdata / "settings.json")
    
    
    @classmethod
    def setMainwindow(cls, mainwindow):
        """
        Stores the application's main window instance.

        :param ui.MainWindow.MainWindow mainwindow: Main window instance
        """
        cls.mainwindow = mainwindow
        
    @classmethod
    def getMainwindow(cls):
        """
        :returns: Main window instance
        :rtype: ui.MainWindow.MainWindow
        """
        return cls.mainwindow
    
    
    @classmethod
    def applicationLoaded(cls):
        """
        Called by the main window when the application is done loading.
        """
        if cls.getMachine() is not None:
            if cls.getSettings().value("General", "startup_init"):
                cls.initMachine(cls.getSettings().value("General", "startup_setup"))
        else:
            logger.warning("No machine selected!")
    
    
    @classmethod
    def getDocumentationPath(cls):
        """
        Returns the path to the HTML documentation index file.
        """
        basepath = Path(os.path.abspath(os.path.dirname(sys.argv[0])))
        helppath = basepath / "_docs" / "html" / "docindex.html"
        return helppath
    
        
    @classmethod
    def setWorkpiece(cls, workpiece):
        """
        Set new workpiece. When setting the workpiece, optimizer parameters are updated
        and the workpiece is optimized.

        :param Base.Workpiece.Workpiece workpiece: New workpiece
        """
        cls.workpieceOriginal = copy.deepcopy(workpiece)
        workpiece.setSize((AppBase.getSettings().value('UI', 'board_size_x'),
                           AppBase.getSettings().value('UI', 'board_size_y')))
        cls.workpiece = workpiece
        cls.workpiece.updateOptimizers(cls.getSettings().child('Optimizers'))
        cls.workpiece.optimize()
        cls.workpiece.holeList.active = cls.getSettings().value('UI', 'holes_active')
        cls.workpiece.millingList.active = cls.getSettings().value('UI', 'millings_active')
        cls.workpieceMirrored = False
        
    @classmethod
    def getWorkpiece(cls):
        """
        :returns: Current workpiece
        :rtype: Base.Workpiece.Workpiece
        """
        return cls.workpiece
    
    @classmethod
    def setWorkpieceMirrored(cls, mirror):
        """
        :param bool mirror: new mirror status
        :returns: mirror status changed
        :rtype: bool
        """
        if cls.workpieceMirrored != mirror:
            cls.getWorkpiece().mirror()
            cls.workpieceMirrored = mirror
            return True
        return False
    
    
    @classmethod
    def getSettings(cls):
        """
        :returns: Current application settings
        :rtype: Base.AppSettings.AppSettings
        """
        return cls.settings
    
    
    @classmethod
    def getMachine(cls):
        """
        :returns: (Base.MachineBase) Current active machine
        :rtype: Base.MachineBase.MachineBase
        """
        return cls.machine
    
    
    @classmethod
    def getMachineType(cls, name):
        """
        :param str name: Machine name
        :returns: Machine class
        :rtype: class
        """
        return cls.getSettings().machines[name]
            
    
    @classmethod
    def initMachine(cls, setup=False, signal=True):
        """
        (Re-)Initializes the current active machine

        :param bool setup: Apply machine parameters after initialization
        :param bool signal: Emit AppSettings.sigMachineChanged signal
        """
        # check if valid active machine
        if cls.getMachine() is None:
            return
        # close machine if already initialized
        cls.closeMachine()
        # initialize and setup machine
        logger.info("Initializing machine %s...", cls.getMachine().getName())
        try:
            cls.getMachine().initialize(cls.getSettings().child('MachineCom', cls.getMachine().getName()))
        except Exception as e:
            logger.error("Machine init failed: %s", e)
            QtWidgets.QMessageBox.critical(
                cls.getMainwindow(),
                "Machine init failed",
                "Machine initialization failed, see log for details."
            )
        if setup and cls.getMachine().isInitialized():
            cls.setupMachine()
        # emit signal
        if signal:
            cls.getSettings().sigMachineChanged.emit()
    
    
    @classmethod
    def setupMachine(cls):
        """
        Applies machine parameters.
        """
        logger.info("Applying parameters for machine %s...", cls.getMachine().getName())
        settings = cls.getSettings()
        machine = cls.getMachine()
        name = machine.getName()
        machine.applyBasicParameters(settings.child('MachineBase'), settings.child('MachineBaseHidden'))
        logger.debug(machine.getDefaultOrigin())
        logger.debug(machine.getParkPosition())
        machine.applyParameters(settings.child('MachineParams', name), settings.child('MachineHidden', name))
    
    
    @classmethod
    def closeMachine(cls):
        """
        Finalizes machine.
        """
        if cls.getMachine() is None or not cls.getMachine().isInitialized():
            return
        logger.info("Closing machine %s", cls.getMachine().getName())
        cls.getMachine().finalize()
    
    
    @classmethod
    def changeMachine(cls, machine, init=False, setup=False, signal=True):
        """
        Close the current active machine and sets another machine as currently active.

        :param str machine: Name of the new machine
        :param bool init: Initialize new machine
        :param bool setup: Apply machine parameters after initialization
        :param bool signal: Emit AppSettings.sigMachineChanged signal
        """
        if not machine in cls.getSettings().machines.keys():
            raise errs.InvalidArgument('machine', 'Invalid machine.')
        cls.closeMachine()
        # instantiate machine object for given machine name
        cls.machine = cls.getSettings().machines[machine]()
        cls.getSettings().setValue(machine, 'MachineBaseHidden', 'machine_name')
        if init:
            cls.initMachine(setup, signal=False)
        if signal:
            cls.getSettings().sigMachineChanged.emit()
            
    
    @classmethod        
    def setParkPosition(cls, position):
        """
        Sets the park position.

        :param position: (x, y, z) coordinates
        :type position: tuple(float, float, float)
        """
        machine = cls.getMachine()
        settings = cls.getSettings()
        if machine is not None:
            machine.setParkPosition(position[:])
        settings.setValue(position[0], "MachineBaseHidden", "parkpos_x")
        settings.setValue(position[1], "MachineBaseHidden", "parkpos_y")
        settings.setValue(position[2], "MachineBaseHidden", "parkpos_z")
        
        
    @classmethod        
    def setDefaultOrigin(cls, position):
        """
        Sets the default origin.

        :param position: (x, y, z) coordinates
        :type position: tuple(float, float, float)
        """
        machine = cls.getMachine()
        settings = cls.getSettings()
        if machine is not None:
            machine.setDefaultOrigin(position[:])
        settings.setValue(position[0], "MachineBaseHidden", "boardorigin_x")
        settings.setValue(position[1], "MachineBaseHidden", "boardorigin_y")
        settings.setValue(position[2], "MachineBaseHidden", "boardorigin_z")