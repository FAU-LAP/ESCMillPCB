"""
Created on 16.02.2018

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

import json
import binascii
from PyQt5 import QtCore
import pyqtgraph.parametertree.parameterTypes as ptypes

import Base.BaseOptimizers as bo
from Base.MachineBase import MachineBase
from Machines import TinyG


class AppSettings(QtCore.QObject):
    """
    This class handles application settings.
    It acts as a settings database and stores/restores settings when exiting/starting the application.
    The application settings are stored in a pyqtgraph.parametertree.parameterTypes.GroupParameter object.

    This class derives from QObject to support Qt signals.

    ======================  ==========================================================================
    **Signals**
    ======================  ==========================================================================
    sigSettingsChanged      Emitted when a setting has changed.
                            Carries a list with the names of the root setting nodes which are affected
    sigMachineChanged       Emitted when the active machine has changed
    ======================  ==========================================================================
    """
    
    # Qt signals
    sigSettingsChanged = QtCore.pyqtSignal(list)
    sigMachineChanged = QtCore.pyqtSignal()
    
    # available optimizers
    optimizers = [bo.HoleOrderOptimizer, bo.MillingCombinationOptimizer, bo.BreakoutOptimizer, bo.MillingOrderOptimizer]
    
    # available machines
    machines = {'None':MachineBase, 'TinyG':TinyG.TinyG}
    
    settings = ptypes.GroupParameter(name='Settings')

    def __init__(self):
        """
        Constructor
        """
        super().__init__(None)
        
    
    def child(self, *names):
        """
        Access parameter nodes, equivalent to AppSettings.settings.child(\*names).
        See pyqtgrapgh.parametertree.Parameter.child()

        :param str \*names: path, to, child
        """
        return self.settings.child(*names)
    
    
    def value(self, *names):
        """
        Read parameter values, equivalent to AppSettings.settings.child(\*names).value()
        See pyqtgrapgh.parametertree.Parameter.child(), pyqtgrapgh.parametertree.Parameter.value()

        :param str \*names: (strings) path, to, child
        :returns: Parameter value
        """
        return self.settings.child(*names).value()
    
    
    def setValue(self, value, *names):
        """
        Set parameter values, equivalent to AppSettings.settings.child(\*names).setValue(value)
        See pyqtgrapgh.parametertree.Parameter.child(), pyqtgrapgh.parametertree.Parameter.value()

        :param value: Value of the parameter
        :param \*names: path, to, child
        :type \*names: str
        """
        return self.settings.child(*names).setValue(value)
    
    
    def storeQtState(self, qobject, *names):
        """
        Store the state of a QObject which supports saveState() to a string parameter.

        :param QObject qobject: Object with state to store
        :param str \*names: Name of child or tuple (path, to, child)
        """
        logger.debug("Save QObject state (" + ", ".join(names) + ")")
        self.setValue(qobject.saveState().data().hex(), *names)
        
    def restoreQtState(self, qobject, *names):
        """
        Restore the state of a QObject which supports restoreState() from a string parameter.
        The state is only restored if the string parameter is not an empty string,
        otherwise false is returned.
        If the restore operation fails, a warning is written to the log and false is returned.
        If the restore operation was perfomed and successful, true is returned

        :param QObject qobject: Object with state to store
        :param str \*names: Name of child or tuple (path, to, child)
        """
        result = False
        logger.debug("Load QObject state (" + ", ".join(names) + ")")
        value = self.value(*names)
        if value != '':
            result = qobject.restoreState(QtCore.QByteArray().append(binascii.unhexlify(value)))
            if not result:
                logger.warning("Could not restore QObject state (" + ", ".join(names) + ")")
        else:
            logger.debug("Did not restore empty QObject state (" + ", ".join(names) + ")")
        return result
    
    def storeQtGeometry(self, widget, *names):
        """
        Store the geometry of a QWidget to a string parameter.

        :param QWidget widget: (QWidget) Widget with geometry to store
        :param  str \*names: Name of child or tuple (path, to, child)
        """
        logger.debug("Save QWidget geometry (" + ", ".join(names) + ")")
        self.setValue(widget.saveGeometry().data().hex(), *names)
        
    def restoreQtGeometry(self, widget, *names):
        """
        Restore the state of a QWidget from a string parameter.
        The state is only restored if the string parameter is not an empty string,
        otherwise false is returned.
        If the restore operation fails, a warning is written to the log and false is returned.
        If the restore operation was perfomed and successful, true is returned

        :param QWidget widget: Widget with state to store
        :param str \*names: Name of child or tuple (path, to, child)
        """
        result = False
        logger.debug("Load QWidget geometry (" + ", ".join(names) + ")")
        value = self.value(*names)
        if value != '':
            result = widget.restoreGeometry(QtCore.QByteArray().append(binascii.unhexlify(value)))
            if not result:
                logger.warning("Could not restore QWidget geometry (" + ", ".join(names) + ")")
        else:
            logger.debug("Did not restore empty QWidget geometry (" + ", ".join(names) + ")")
        return result
        
    
    def loadDefaults(self, signal=True):
        """
        Clears all settings and reverts them to default.

        :param bool signal: Can be used to suppress the sigSettingsChanged signal
        """
        self.settings.clearChildren()
        self.settings.addChildren([
            {'name':'UI', 'type':'group'},
            {'name':'General', 'type':'group'},
            {'name':'MachineBase', 'type':'group'},
            {'name':'MachineBaseHidden', 'type':'group'},
            {'name':'Optimizers', 'type':'group'},
            {'name':'MachineCom', 'type':'group'},
            {'name':'MachineParams', 'type':'group'},
            {'name':'MachineHidden', 'type':'group'}
        ])
        
        # load UI settings
        self.child('UI').addChildren(self.uiSettings().children())
        
        # load default software settings
        self.child('General').addChildren(self.generalSettings().children())
                
        # load optimizer defaults
        for opt in AppSettings.optimizers:
            self.child('Optimizers').addChild(opt.getParameters())
            
        # load machine defaults
        self.child('MachineBase').addChildren(MachineBase.getBasicParameters().children())
        self.child('MachineBaseHidden').addChildren(MachineBase.getBasicHiddenParameters().children())
        for key, val in self.machines.items():
            mparams = ptypes.GroupParameter(name=key)
            comparams = ptypes.GroupParameter(name=key)
            hiddenparams = ptypes.GroupParameter(name=key)
            if val is not None:
                mparams.addChildren(val.getParameters().children())
                comparams.addChildren(val.getComParameters().children())
                hiddenparams.addChildren(val.getHiddenParameters().children())
            self.child('MachineParams').addChild(mparams)
            self.child('MachineCom').addChild(comparams)
            self.child('MachineHidden').addChild(hiddenparams)
            
        if signal:
            self.sigSettingsChanged.emit([ch.name() for ch in self.settings.children()])
            
            
    def loadSettings(self, file):
        """
        Load settings from a previously saved JSON file.

        :param str file: Path to the settings file
        """
        # read settings from file
        with open(file, 'r') as fhnd:
            newsettings = json.load(fhnd)
        # revert current settings to default
        self.loadDefaults(signal=False)
        # store read settings
        self.settings.restoreState(newsettings, addChildren=False, removeChildren=False)
        self.sigSettingsChanged.emit([ch.name() for ch in self.settings.children()])
    
        
    def saveSettings(self, file):
        """
        Save settings as JSON file.

        :param str file: Path to the settings file
        """
        with open(file, "w") as fhnd:
            tosave = self.settings.saveState()
            json.dump(tosave, fhnd, indent=2)
            
            
    def copySettings(self):
        """
        :returns: a copy of the settings
        :rtype: AppSettings
        """
        copy = ptypes.GroupParameter(name='Settings')
        copy.restoreState(self.settings.saveState())
        return copy
    
    
    def updateSettings(self, newsettings, settingsChanged):
        """
        Update current application settings.

        :param pyqtgraph.GroupParameter newsettigns: Parameter containing new settings
        :param settingsChanged: List with names of parameters which have changed
        :type settingsChanged: list[str]
        """
        self.settings = newsettings
        self.sigSettingsChanged.emit(settingsChanged)
    
    
    @staticmethod
    def generalSettings():
        """
        Returns the general settings parameters and their default values.

        :returns: general settings parameters
        :rtype: pyqtgraph.GroupParameter
        """
        params = {
            'name':'General', 'type':'group', 'children':[
                {
                    'name':'startup_init',
                    'title':'Connect to machine on startup',
                    'type':'bool',
                    'default':False,
                    'value':False
                },
                {
                    'name':'startup_setup',
                    'title':'Apply machine settings on startup',
                    'type':'bool',
                    'default':False,
                    'value':False
                },
                {
                    'name':'logfile_level',
                    'title':'Logfile threshold level',
                    'type':'list',
                    'values':{
                        'Debug':logging.DEBUG, 'Info':logging.INFO, 'Warning':logging.WARNING,
                        'Error':logging.ERROR, 'Critical':logging.CRITICAL
                    },
                    'default':logging.DEBUG,
                    'value':logging.DEBUG
                },
                {
                    'name':'logfile_backups',
                    'title':'Logfiles to keep',
                    'type':'int',
                    'min':1,
                    'default':10,
                    'value':10
                },
                {
                    'name':'loglist_level',
                    'title':'Log window threshold level',
                    'type':'list',
                    'values':{
                        'Debug':logging.DEBUG, 'Info':logging.INFO, 'Warning':logging.WARNING,
                        'Error':logging.ERROR, 'Critical':logging.CRITICAL
                    },
                    'default':logging.INFO,
                    'value':logging.INFO
                }
            ]
        }
        return ptypes.GroupParameter(**params)
    
    
    @staticmethod
    def uiSettings():
        """
        Returns the UI settings parameters and their default values.

        :returns: UI settings parameters
        :rtype: pyqtgraph.GroupParameter
        """
        params = {
            'name':'UI', 'type':'group', 'children':[
                {
                    'name':'mainWindow_geometry',
                    'type':'str',
                    'value':''
                },
                {
                    'name':'splitterRight_state',
                    'type':'str',
                    'value':''
                },
                {
                    'name':'splitterBottom_state',
                    'type':'str',
                    'value':''
                },
                {
                    'name':'settingsDialog_geometry',
                    'type':'str',
                    'value':''
                },
                {
                    'name':'holes_active',
                    'type':'bool',
                    'value':True
                },
                {
                    'name':'millings_active',
                    'type':'bool',
                    'value':True
                },
                {
                    'name':'board_mirrored',
                    'type':'bool',
                    'value':True
                },
                {
                    'name':'board_outlines',
                    'type':'bool',
                    'value':True
                },
                {
                    'name':'board_size_x',
                    'type':'float',
                    'value':100
                },
                {
                    'name':'board_size_y',
                    'type':'float',
                    'value':75
                }
            ]
        }
        return ptypes.GroupParameter(**params)