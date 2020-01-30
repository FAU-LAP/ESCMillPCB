"""
Created on 29.01.2018

@author: Christian Ott
"""

# initialize logging
import logging
from Base.LogHandlers import TracebackFormatter
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = TracebackFormatter("%(asctime)s %(levelname)s:%(name)s: %(message)s%(traceback)s")
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

from PyQt5 import QtWidgets, QtGui
import sys
import traceback
import os.path
import ctypes
import pyqtgraph as pg

# convert UI files if not in frozen environment
from Base.UITools import convertUI, convertResources
if not getattr(sys, 'frozen', False):
    convertUI()
    convertResources()

# from Base.AppSettings import AppSettings
from Base.AppBase import AppBase
from ui.MainWindow import MainWindow

# needed for Qt resource support
import ui.Resources


def handle_exception(exc_type, exc_value, exc_traceback):
    """ Main exception handler """

    # KeyboardInterrupt is a special case.
    # We don't raise the error dialog when it occurs.
    if issubclass(exc_type, KeyboardInterrupt):
        if QtWidgets.qApp:
            QtWidgets.qApp.quit()
            return

    filename, line, dummy, dummy = traceback.extract_tb(exc_traceback).pop()
    filename = os.path.basename(filename)
    error    = "%s: %s (line %s in %s)" % (exc_type.__name__, exc_value, line, filename)

    logger.error(error, extra={'traceback':"".join(traceback.format_exception(exc_type, exc_value, exc_traceback))})
    
    QtWidgets.QMessageBox.critical(None,"Error",
        "<html>A critical error has occured.<br/> "
        + "<b>%s</b><br/><br/>" % error
        + "It occurred at <b>line %d</b> of file <b>%s</b>.<br/>" % (line, filename)
        + "</html>")

    print("Closed due to an error. This is the full error report:")
    print()
    print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))


if __name__ == '__main__':
    
    sys.excepthook = handle_exception
    appid = 'fau.lap.escmillpcb'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
    
    pg.setConfigOptions(imageAxisOrder='row-major')
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    
    AppBase.initialize()
    
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setWindowIcon(QtGui.QIcon(":/root/images/icon.png"))
    mainwindow = MainWindow()
    logger.info("ESCMillPCB Version {}".format(AppBase.version))
    AppBase.setMainwindow(mainwindow)
    mainwindow.show()
    app.exec_()
    
    AppBase.finalize()
