"""
Created on 21.05.2019

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

from PyQt5 import QtWidgets


class FlowchartCtrlLibrary(object):
    """
    Library of custom widgets for flowchart CtrlNodes.
    Static class.
    """
    
    library = {}
        
    @classmethod
    def registerCtrlType(cls, name, ctrlClass, factoryFun=None):
        """
        Register widget type.

        :param str name: type name of the control (identifier in the CtrlNode's uiTemplate)
        :param class ctrlClass: class of the control, must be derived from QWidget
        :param factoryFun: factory function to create the widget, recieves opts dict
        :type factoryFun: function(dict)
        """
        if not issubclass(ctrlClass, QtWidgets.QWidget):
            raise Exception("Object %s is not a QWidget subclass" % str(ctrlClass))
        if factoryFun is None:
            factoryFun = lambda opts: ctrlClass(**opts)
        cls.library[name] = (ctrlClass, factoryFun)
        
    
    @classmethod
    def createCtrl(cls, name, opts={}):
        """
        Creates a widget of the type associated with name.

        :param str name: type name of the control
        :param dict opts: additional options for the control
        """
        logger.debug("Creating control of type %s.", name)
        return cls.library[name][1](opts)