"""
Created on 24.02.2018

@author: Christian Ott
"""

import logging
logger = logging.getLogger(__name__)

from PyQt5 import QtCore, QtWidgets
import numpy as np
import json
#import io
import serial
import serial.tools.list_ports as slp
import time
import pyqtgraph.parametertree.parameterTypes as ptypes

import Base.Errors as errs
from Base.MachineBase import MachineBase
from ui.TinyGCycleControl import TinyGCycleControl
from ui.TinyGTestpanel import TinyGTestpanel


class TinyGSender(QtCore.QObject):
    """
    Worker class which sends commands to the TinyG board. Will be run in a separate thread.

    This class manages a command buffer to implement TinyG's linemode protocol.
    (See https://github.com/synthetos/TinyG/wiki/Tinyg-Communications-Programming)

    Inherits from QObject to support Qt's threading and signal/slot mechanisms.

    ===================  ===================================================================================
    **Signals**
    ===================  ===================================================================================
    sigQueryReceived     Emitted when the answer to a query command is received.
                         Carries a command response dictionary.
    sigBufferChanged     Emitted when the output buffer content changed.
                         Carries a dictionary {'sendbuffersize', 'usedlines'}
    ===================  ===================================================================================
    """
    
    sigQueryReceived = QtCore.pyqtSignal(dict)
    sigBufferChanged = QtCore.pyqtSignal(dict)
    
    def __init__(self, tinyg, receiver, maxlines=4, parent=None):
        """
        Constructor

        :param TinyG tinyg: TinyG object using the sender.
        :param TinyGReciever receiver: Currently active TinyGSender object.
        :param int maxlines: Maximal number of lines to be stored in the TinyG board's linebuffer.
        """
        super().__init__(parent)
        
        self.tinyg = tinyg
        self.receiver = receiver
        self.maxlines = maxlines
        self.sendbuffer = []
        self.querybuffer = ""
        self.lastQueryResult = None
        self.freelines = maxlines
        self.testpanel = None
        self.settings = None
        self.cycledlg = None
        
        self.tinyg.sigCommand.connect(self.appendCommand)
        self.tinyg.sigQuery.connect(self.appendQuery)
        self.tinyg.sigFeedhold.connect(self.feedhold)
        self.tinyg.sigResume.connect(self.resume)
        self.tinyg.sigStop.connect(self.stop)
        self.tinyg.sigReset.connect(self.reset)
        self.receiver.sigResponseReceived.connect(self.signalReceived)
            
    
    def getLastQueryResult(self):
        """
        :returns: result of the last successful query
        :rtype: dict
        """
        return self.lastQueryResult
    
    
    def _work(self):
        """
        Handles sending lines to the board to keep the linebuffer filled.
        Should not be called directy.
        """
        while len(self.sendbuffer) > 0 and self.freelines > 0:
            self.tinyg.send(self.sendbuffer.pop(0))
            self.freelines -= 1
            logger.debug("Free line buffers: %s", self.freelines)
            # check if linebuffer is in sync
            if self.freelines < 0:
                logger.warning("freelines < 0! Linebuffer out of sync?")
                self.freelines = 0
                
                
    def _handleError(self, msg):
        """
        Filters and logs error responses.
        """
        if msg['f'][1] != 0:
            # filter lesser warnings (currently only 201 "MINIMUM_LENGTH_MOVE"
            if msg['f'][1] in (201,):
                logger.debug("TinyG response contains a warning. Command %s, error %s", msg['r'], msg['f'][1])
            else:
                logger.error("TinyG response contains an error. Command %s, error %s", msg['r'], msg['f'][1])
                
    
    @QtCore.pyqtSlot(dict)
    def appendCommand(self, cmd):
        """
        Append a simple command to the command buffer.
        Not meant to be called directly, commands should be passed by the :attr:`TinyG.sigCommand` signal.

        :param dict cmd: command
        """
        logger.debug("Appended command: %s", cmd)
        self.sendbuffer.append(cmd)
        self._work()
    
    
    @QtCore.pyqtSlot(dict)
    def appendQuery(self, cmd):
        """
        Append a query command to the command buffer.
        Queries can only be processed one at a time - use :meth:`TinyG.executeQuery` for synchronous processing.
        The answer to queries is returned via the sigQueryReceived signal and also stored in the
        lastQueryResult field.

        Not meant to be called directly, commands should be passed by the :attr:`TinyG.sigQuery` signal.

        :parmam dict cmd: command
        """
        logger.debug("Appended query: %s", cmd)
        self.sendbuffer.append(cmd)
        self.querybuffer = list(cmd.keys())[0]
        self._work()
        
        
    @QtCore.pyqtSlot()
    def feedhold(self):
        """
        Sends a feedhold command.
        """
        self.tinyg.sendRaw("!")
    
    
    @QtCore.pyqtSlot()
    def resume(self):
        """
        Sends a resume command.
        """
        self.tinyg.sendRaw("~")
    
    
    @QtCore.pyqtSlot()
    def stop(self):
        """
        Sends a stop command and resets output buffers.
        """
        self.sendbuffer.clear()
        self.tinyg.sendRaw("!%")
        self.freelines = self.maxlines
        self.sigBufferChanged.emit({'sendbuffersize':len(self.sendbuffer), 
                                    'usedlines':(self.maxlines-self.freelines)})


    @QtCore.pyqtSlot()
    def reset(self):
        """
        Sends a reset command and resets output buffers.
        """
        self.sendbuffer.clear()
        self.tinyg.sendRaw("\x18")  # reset: Cancel character (Ctrl-x)
        self.freelines = self.maxlines
        self.sigBufferChanged.emit({'sendbuffersize':len(self.sendbuffer), 
                                    'usedlines':(self.maxlines-self.freelines)})
    
    
    @QtCore.pyqtSlot(dict)
    def signalReceived(self, msg):
        """
        When a response is received by the :class:`TinyGReceiver` object it is then passed to this slot.

        :param dict msg: message
        """
        self.freelines += 1
        logger.debug("Free line buffers: %s", self.freelines)
        # check if linebuffer is in sync
        if self.freelines > self.maxlines:
            logger.warning("maxlines exceeded! Linebuffer out of sync?")
            self.freelines = self.maxlines
        # check if the response contains an error
        self._handleError(msg)
        # check if response is in querybuffer
        if list(msg["r"].keys())[0] == self.querybuffer:
            self.querybuffer = ""
            self.lastQueryResult = msg
            self.sigQueryReceived.emit(msg)
        self._work()
        self.sigBufferChanged.emit({'sendbuffersize':len(self.sendbuffer), 
                                    'usedlines':(self.maxlines-self.freelines)})
    
    
    
class TinyGReceiver(QtCore.QObject):
    """
    Worker class which receives responses from the TinyG board. Will be run in a separate thread.

    Until the thread is stopped, this class waits for received messages and passes the answers to the
    sender thread where they will be processed and eventually passed to the main thread.

    Inherits from QObject to support Qt's threading and signal/slot mechanisms.

    =========================  ===============================================================================
    **Signals**
    =========================  ===============================================================================
    sigResponseReceived        Emitted when a response is received from the TinyG board.
                               This signal's purpose is to pass the raw responses to the active TinyGSender
                               object which runs in a separate thread.
                               Carries a dictionary containing the response.
    sigSystemReadyReceived     Emitted when a system ready response is received.
                               Carries a dictionary containing the response.
    sigStatusReportReceived    Emitted when a status report is received from the TinyG board.
                               Carries a dictionary containing the status report.
    sigQueueReportReceived     Emitted when a queue report is received from the TinyG board.
                               Carries a dictionary containing the queue report.
    sigUnknownMessageReceived  Emitted when a unknown message is received.
                               Carries a dictionary containing the message.
    =========================  ===============================================================================
    """
    
    sigResponseReceived = QtCore.pyqtSignal(dict)
    sigSystemReadyReceived = QtCore.pyqtSignal(dict)
    sigStatusReportReceived = QtCore.pyqtSignal(dict)
    sigQueueReportReceived = QtCore.pyqtSignal(dict)
    sigUnknownMessageReceived = QtCore.pyqtSignal(dict)
    
    
    def __init__(self, tinyg, parent=None):
        """
        Constructor

        :param TinyG tinyg: TinyG object using the sender.
        """
        super().__init__(parent)
        
        self.tinyg = tinyg
        self.running = False
        self.timer = None
        self.tinyg.sigInitialize.connect(self._run)
        self.tinyg.sigFinalize.connect(self._quit)
        
    
    @QtCore.pyqtSlot()
    def _run(self):
        """
        Starts the receiver loop. Should not be called directly.
        """
        self.running = True
        # QTimers with timeout=0 will timeout as soon as all events are processed
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(0)
        self.timer.timeout.connect(self._work)
        self.timer.start()
        logger.debug("TinyGReceiver main loop started.")
        
        
    @QtCore.pyqtSlot()
    def _quit(self):
        """
        Stops the receiver loop. Should not be called directly.
        """
        self.timer.stop()
        self.timer = None
        self.running = False
        logger.debug("TinyGReceiver stopped.")
    
    
    @QtCore.pyqtSlot()
    def _work(self):
        """
        Receiver loop. Should not be called directly.
        """
        response = self.tinyg.receive()
        if response is not None:
            if "r" in response.keys():
                # special case: SYSTEM READY message after reset
                if "msg" in response['r'].keys() and response['r']['msg'] == "SYSTEM READY":
                    self.sigSystemReadyReceived.emit(response['r'])
                    logger.info("TinyG reboot complete: %s", response['r'])
                else:
                    self.sigResponseReceived.emit(response)
            elif "sr" in response.keys():
                self.sigStatusReportReceived.emit(response)
            elif "qr" in response.keys():
                self.sigQueueReportReceived.emit(response)
            elif "rx" in response.keys():
                logger.debug("RX received: %s", response)
            else:
                logger.warning("Unknown response received: %s", response)
                self.sigUnknownMessageReceived.emit(response)



class TinyG(MachineBase):
    """
    Implementation of MachineBase to control a TinyG board.

    The TinyG board directly understands the g-code language but can only hold up to 8 lines of code.
    Therefore the g-code program has to be spooled to the board.

    Workflow of executing the g-code program:
    - directly send the fist maxlines commands to the board, initialize linesToSend to 0
    - for each {r:...} response increment linesToSend by 1
    - as long as freelines > 0, send lines and decrement freelines
    - do this until the whole programm has been spooled

    Sending of commands and recieving responses is done asynchronously.

    ===================  ===================================================================================
    **Signals**
    ===================  ===================================================================================
    sigCommand           Emitted when a command is to be sent by the active TinyGSender object.
                         This signal's purpose is to pass commands to the active TinyGSender
                         object which runs in a separate thread.
                         Carries a dictionary containing the command with parameters.
    sigQuery             Emitted when a query command is to be sent by the active TinyGSender object.
                         This signal's purpose is to pass query commands to the active TinyGSender
                         object which runs in a separate thread.
                         Carries a dictionary containing the command with parameters.
    sigFeedhold          Emitted when a feedhold is to be performed by the active TinyGSender object.
                         This signal's purpose is to pass commands to the active TinyGSender
                         object which runs in a separate thread.
    sigResume            Emitted when a resume command is to be sent by the active TinyGSender object.
                         This signal's purpose is to pass commands to the active TinyGSender
                         object which runs in a separate thread.
    sigStop              Emitted when the current cycle is to be stopped by the active TinyGSender object.
                         This will cause the TinyGSender object to flush its buffers and the buffers of the
                         machine.
                         This signal's purpose is to pass commands to the active TinyGSender
                         object which runs in a separate thread.
    sigReset             Emitted when the machine is to be reset by the active TinyGSender object.
                         This will cause the TinyGSender object to flush its buffers and the buffers of the
                         machine.
                         This signal's purpose is to pass commands to the active TinyGSender
                         object which runs in a separate thread.
    sigInitialize        Connection to TinyG board is opened.
    sigFinalize          Connection to TinyG board is to be closed.
    ===================  ===================================================================================
    """
    
    sigCommand = QtCore.pyqtSignal(dict)
    sigQuery = QtCore.pyqtSignal(dict)
    sigFeedhold = QtCore.pyqtSignal()
    sigResume = QtCore.pyqtSignal()
    sigStop = QtCore.pyqtSignal()
    sigReset = QtCore.pyqtSignal()
    
    sigInitialize = QtCore.pyqtSignal()
    sigFinalize = QtCore.pyqtSignal()
    

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.receiver = None
        self.receiverThread = None
        self.sender = None
        self.senderThread = None
        self.port = None
        self.io = None
        self.comtimeout = 1
        self.querytimeout = 10
        self.cycleRunning = False
        self.plannerBuffer = []
        self.workpieceOffset = None
        self.lastStatus = {}
        self.homed = False;
        
        
    def initialize(self, comparams):
        """
        Initialize TinyG communication and settings.
        Default communication parameters: 115200 baud, 8 data bits, no parity, 1 stop bit, XonXoff flow control

        :param pyqtgraph.GroupParameter comparams: GroupParameter containing the communication parameters
        """
        try:
            self.homed = False
            
            self.querytimeout = comparams.child('timeout').value()
            logger.info("Connecting to TinyG at port %s (%s baud, %ss com timeout, %ss query timeout)...", 
                        comparams.child('com').value(), comparams.child('baud').value(), 
                        self.comtimeout, self.querytimeout)
                    
            self.port = serial.Serial(
                port=comparams.child('com').value(),
                baudrate=comparams.child('baud').value(),
                timeout=self.comtimeout,
                xonxoff=comparams.child('flowctrl').value()==1,
                rtscts=comparams.child('flowctrl').value()==2
            )
            self.port.reset_input_buffer()
            self.port.reset_output_buffer()
            
            # start sender and receiver threads
            self.receiver = TinyGReceiver(self)
            self.receiverThread = QtCore.QThread()
            self.receiver.moveToThread(self.receiverThread)
            self.receiverThread.start()
            self.receiver.sigStatusReportReceived.connect(self.receiver_sigStatusReportReceived)
            
            self.sender = TinyGSender(self, self.receiver)
            self.senderThread = QtCore.QThread()
            self.sender.moveToThread(self.senderThread)
            self.senderThread.start()
            
            self.sigInitialize.emit()
            
            # reset TinyG
            self.reset()
            # set strict JSON syntax mode
            self.executeCommand({'js':1})
            # set JSON verbosity to verbose
            self.executeCommand({'jv':5})
            # enable all status messages
            self.executeQuery({'sr':{
                'posx':True, 'posy':True, 'posz':True, 'posa':True, 'feed':True, 'vel':True,
                'unit':True, 'coor':True, 'dist':True, 'frmo':True, 'stat':True, 'momo':True
            }})
            # enable queue reports
            self.executeCommand({'qv':1})
            # enable filtered automatic status reports
            self.executeCommand({'sv':1})
            # set status report interval
            self.executeCommand({'si':200})
            # initialize last status report
            report = self.executeQuery({'sr':None})
            self.lastStatus = report['r']['sr']
            # set G54 system to absolute (machine) coordinates
            self.executeCommand({'gc':'g10l2p1x0y0z0'})
            # set G55 system to default board origin
            self.executeCommand({'gc':'g10l2p2x{}y{}z{}'.format(*self.getDefaultOrigin())})
            self.workpieceOffset = np.array(self.getDefaultOrigin())
            self.startCoordinateTimer()
            logger.info("Connected to TinyG.")
        except Exception as e:
            try:
                self.finalize()
            except:
                pass
            raise e
        
        
    def finalize(self):
        """
        Deinitalizes the hardware and finalizes the communication interface.
        """
        if not self.isInitialized():
            return
        try:
            self.stop()
            self.setSpindle(False)
            self.sigFinalize.emit()
            self.senderThread.quit()
            self.senderThread.wait(2000)
            self.receiverThread.quit()
            self.receiverThread.wait(2000)
            self.port.close()
            logger.info("TinyG connection closed.")
        finally:
            self.port = None
            
            
    def reset(self):
        """
        Resets the TinyG board.

        :returns: TinyG version information
        :rtype: dict
        """
        self.homed = False
        # use timer for timeout
        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        # use local event loop to wait for "query received" signal
        localloop = QtCore.QEventLoop()
        self.receiver.sigSystemReadyReceived.connect(localloop.quit)
        timer.timeout.connect(localloop.quit)
        timer.start(10000)
        # send command and start loop
        self.sigReset.emit()
        localloop.exec()
        # check for timeout
        if not timer.isActive():
            logger.error("Reset timeout error.")
        
    
    def isInitialized(self):
        """
        See :meth:´Base.MachineBase.MachineBase.isInitialized´
        """
        return (self.port is not None)
        
        
    def getPosition(self, absolute=True):
        """
        See :meth:´Base.MachineBase.MachineBase.getPosition´
        """
        pos = np.array([self.lastStatus['posx'], self.lastStatus['posy'], self.lastStatus['posz']])
        if absolute:
            if self.lastStatus['coor'] == 1:
                return list(pos)    # already in absolute coordinate system (G54)
            else:
                return list(pos + self.workpieceOffset)
        else:
            if self.lastStatus['coor'] == 1:
                return list(pos - self.workpieceOffset)
            else:
                return list(pos)    # already in workpiece coordinate system (G55)
    
        
    def feedhold(self):
        """
        See :meth:´Base.MachineBase.MachineBase.feedhold´
        """
        self.sigFeedhold.emit()
        
    def resume(self):
        """
        See :meth:´Base.MachineBase.MachineBase.resume´
        """
        self.sigResume.emit()
    
    def stop(self):
        """
        See :meth:´Base.MachineBase.MachineBase.stop´
        """
        self.sigStop.emit()
            
            
    def jog(self, directions, stepsize=None):
        """
        See :meth:´Base.MachineBase.MachineBase.jog´
        """
        target = None
        if stepsize is None:
            self.executeCommand({"gc":"g54"})
            self.executeCommand({"gc":"g90"})
            pos = self.getPosition(True)
            target = self.calculateMaxSteps(directions)
            for i, direction in enumerate(directions):
                if direction == 0:
                    target[i] = pos[i]
        else:
            self.executeCommand({"gc":"g91"})
            target = [stepsize*direction for direction in directions]             
        command = "g1"
        if directions[0] != 0 or directions[1] != 0:
            command += "f{}x{}y{}".format(self.jogspeedXY, target[0], target[1])
        elif directions[2] != 0:
            command += "f{}z{}".format(self.jogspeedZ, target[2])
        self.executeCommand({"gc":command})
        
        
    def goTo(self, position, absolute=True):
        """
        See :meth:´Base.MachineBase.MachineBase.goTo´
        """
        # check position enumeration length
        if len(position) < 2 or len(position) > 3:
            raise errs.InvalidArgument("position", "invalid length")
        # set requested coordinate system
        if absolute:
            self.executeCommand({'gc':'g54'})
        else:
            self.executeCommand({'gc':'g55'})
            
        # set absolute path mode
        self.executeCommand({'gc':'g90'})
        
        # if the z-axis is moving towards the workpiece, z movement should happen after xy movement
        # if the z-axis is moving away from the workpiece, z movement should happen first
        zfirst = False
        zmove = (len(position) == 3)
        if zmove:
            zfirst = (position[2] > self.getPosition(absolute)[2])
        
        # move to position
        if zmove and zfirst:
            self.executeCommand({"gc":"g0z{}".format(position[2])})
        self.executeCommand({"gc":"g0x{}y{}".format(position[0], position[1])})
        if zmove and not zfirst:
            self.executeCommand({"gc":"g0z{}".format(position[2])})
        
        
    def setSpindle(self, enable):
        """
        See :meth:´Base.MachineBase.MachineBase.setSpindle´
        """
        if enable:
            self.executeQuery({"gc":"m3"})
        else:
            self.executeQuery({"gc":"m5"})
            
            
    def setLaserCrosshair(self, enable):
        """
        See :meth:´Base.MachineBase.MachineBase.setLaserCrosshair´
        """
        if enable:
            self.executeQuery({"gc":"m8"})
        else:
            self.executeQuery({"gc":"m9"})
            
            
    def homingCycle(self):
        """
        See :meth:´Base.MachineBase.MachineBase.homingCycle´
        """
        logger.info("TinyG homing cycle started.")
        self.executeCommand({"gc":"g28.2x0y0z0"})
        self.homed = True;
        
        
    def isHomed(self):
        """
        See :meth:´Base.MachineBase.MachineBase.isHomed´
        """
        return self.homed;
    
    
    def preparePlanner(self):
        """
        See :meth:´Base.MachineBase.MachineBase.preparePlanner´
        """
        self.plannerBuffer = [
            "g21",      # use mm
            "g90",      # absolute position mode
            "g55",      # use workpiece coordinate system
            "g17",      # select XY plane for arcs
            "m3",       # enable spindle
            "g1f{}z{}".format(self.jogspeedZ, 0)   # go to working distance
        ]
        
    def finalizePlanner(self):
        """
        See :meth:´Base.MachineBase.MachineBase.finalizePlanner´
        """
        self.plannerBuffer.extend([
            "m2"        # program end
        ])
    
    def planJog(self, position):
        """
        See :meth:´Base.MachineBase.MachineBase.planJog´
        """
        self.plannerBuffer.append("g1f{}x{}y{}".format(self.jogspeedXY, *position))
        
    def planMill(self, position):
        """
        See :meth:´Base.MachineBase.MachineBase.planMill´
        """
        self.plannerBuffer.append("g1f{}x{}y{}".format(self.millspeedXY, *position))
    
    def planMillArc(self, startposition, endposition, center, ccw=True):
        """
        See :meth:´Base.MachineBase.MachineBase.planMillArc´
        """
        offset = (center[0]-startposition[0], center[1]-startposition[1])
        command = None
        if ccw:
            command = "g3"
        else:
            command = "g2"
        if not np.all(startposition == endposition):
            command = command + "x{}y{}".format(*endposition)
        self.plannerBuffer.append(command + "i{}j{}f{}".format(*offset, self.millspeedXY))
    
    def planInfeed(self):
        """
        See :meth:´Base.MachineBase.MachineBase.planInfeed´
        """
        self.plannerBuffer.extend([
            "g91", 
            "g1f{}z{}".format(self.infeedspeed, -self.infeeddepth),
            "g90"
        ])
    
    def planOutfeed(self):
        """
        See :meth:´Base.MachineBase.MachineBase.planOutfeed´
        """
        self.plannerBuffer.extend([
            "g91",
            "g1f{}z{}".format(self.outfeedspeed, self.infeeddepth),
            "g90"
        ])
        
        
    def setWorkpieceOrigin(self, offset=(0, 0)):
        """
        See :meth:´Base.MachineBase.MachineBase.setWorkpieceOrigin´
        """
        position = self.getPosition(True)
        self.workpieceOffset = [position[0]+offset[0], position[1]+offset[1], self.defaultOrigin[2]]
        self.executeCommand({'gc':'g10l2p2x{}y{}z{}'.format(*self.workpieceOffset)})
        self.executeCommand({'gc':'g55'})


    def setDefaultOrigin(self, position):
        """
        See :meth:´Base.MachineBase.MachineBase.setDefaultOrigin´
        """
        super().setDefaultOrigin(position)
        self.workpieceOffset[2] = self.defaultOrigin[2]
        self.executeCommand({'gc':'g10l2p2z{}'.format(self.defaultOrigin[2])})
        
        
    def executeCycle(self):
        """
        See :meth:´Base.MachineBase.MachineBase.executeCycle´
        """
        if len(self.plannerBuffer) == 0:
            pass
        # open cycle control dialog
        logger.info("Executing TinyG cycle with %s commands.", len(self.plannerBuffer))
        self.cycledlg = TinyGCycleControl(self, self.plannerBuffer)
        for cmd in self.plannerBuffer:
            self.executeCommand({'gc':cmd})
        self.cycledlg.show()
        self.plannerBuffer.clear()
        
        
    def executeCommand(self, command):
        """
        Executes a single command asynchonously.

        :param dict command: Command to send
        """
        self.sigCommand.emit(command)
        
    
    def executeQuery(self, command):
        """
        Executes a single command and returns the response (as dict) synchronously.

        :param dict command: Command to send
        :returns: Response
        :rtype: dict
        """
        # use timer for timeout
        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        # use local event loop to wait for "query received" signal
        localloop = QtCore.QEventLoop()
        self.sender.sigQueryReceived.connect(localloop.quit)
        timer.timeout.connect(localloop.quit)
        if self.querytimeout > 0:
            timer.start(self.querytimeout*1100)
        # send command and start loop
        self.sigQuery.emit(command)
        localloop.exec()
        # check for timeout
        if self.querytimeout > 0 and not timer.isActive():
            logger.error("Query timeout error.")
            raise errs.CommunicationError(command, "Timeout")
        # retrieve and return query data
        return self.sender.getLastQueryResult()
    
    
    def send(self, command):
        """
        Send a command dictionary {command:value} to the TinyG.
        Only the currently active TinyGSender object should call this function.

        :param dict command: command to send
        """
        self.sendRaw(json.dumps(command))
    
    
    def sendRaw(self, message):
        """
        Low level function to send a raw message to the TinyG.
        Only the currently active TinyGSender object should call this function.

        :param str message: Message to send
        """
        logger.debug("Send: %s", message)
        if message[-1] != "\n":
            message += "\n"
        #self.io.write(message)
        self.port.write(message.encode('utf-8'))
    
    
    def receive(self):
        """
        Low level function which receives messages from the TinyG.
        Returns a dictionary with the received message or None on timeout.
        Only the currently active TinyGReceiver object should call this function.

        :returns: Recieved message (or None on timeout)
        :rtype: dict
        """
        #line = self.io.readline()
        if not self.isInitialized():
            return None
        line = self.port.readline().decode('utf-8').strip()
        if line != "":
            logger.debug("Received: %s", line)
            return json.loads(line)
        #logger.debug("Read operation timeout.")
        return None 
    
    
    def applyParameters(self, params, hiddenparams=None):
        """
        Applies the given machine parameters to the hardware.

        :param pyqtgraph.GroupParameter params: GroupParameter containing the machine parameters
        :param pyqtgraph.GroupParameter hiddenparams: GroupParameter containing the hidden parameters
        """
        self.settings = params.child('motor').getValues()
        self.settings.update(params.child('axis').getValues())
        self.settings.update(params.child('homing').getValues())
        for key, val in self.settings.items():
            self.executeQuery({key:val[0]})
        logger.info("TinyG parameters applied.")
            
            
    def retrieveParameters(self):
        """
        See :meth:`Base.MachineBase.MachineBase.retrieveParameters`
        """
        params = self.getParameters()
        for grp in params.children():
            for param in grp.children():
                cmd = param.name()
                result = self.executeQuery({cmd:None})
                param.setValue(result['r'][cmd])
        return params
    
    
    def calculateMaxSteps(self, directions):
        """
        Calculates the maximal possible step per direction (in mm) without exceeding soft limits.
        This is needed for continuous jogging.

        :param directions: Tuple of directions (1: positive, -1: negative, 0: not included) for (x, y, z) axis
        :type directions: tuple(int, int, int)
        :returns: maximal possible step (in mm) in the given directions
        :rtype: tuple(float, float, float)
        """
        if self.settings['sl'][0] == 0:
            return [1000, 1000, 1000]
        steps = [0, 0, 0]
        minPos = np.array([self.settings['xtn'][0], self.settings['ytn'][0], self.settings['ztn'][0]])+1
        maxPos = np.array([self.settings['xtm'][0], self.settings['ytm'][0], self.settings['ztm'][0]])-1
        #logger.debug("min: %s", minPos)
        #logger.debug("max: %s", maxPos)
        for i, direction in enumerate(directions):
            if direction < 0:
                steps[i] = minPos[i]
            else:
                steps[i] = maxPos[i]
        return steps
    
    
    @QtCore.pyqtSlot(dict)
    def receiver_sigStatusReportReceived(self, msg):
        """
        Slot triggered when a status report is received.

        :param dict msg: status report
        """
        self.lastStatus.update(msg['sr'])
        statusmsg = "{} (current coordinate system: {})".format(
            self.getStatusMessage('stat', self.lastStatus['stat']),
            self.getStatusMessage('coor', self.lastStatus['coor'])
        )
        self.sigStatusUpdate.emit(statusmsg)
    
    
    @staticmethod
    def checksum(rawmsg):
        """
        Computes a checksum for given received response message string.
        See https://en.wikipedia.org/wiki/Java_hashCode()

        TODO
        """
        pass
        
    
    @staticmethod
    def getStatusMessage(msgtype, code):
        """
        Returns a readable message string for the given status report code.

        ===================  ===========================================
        **Supported types**
        ===================  ===========================================
        footer               Response footer status code
        error                Error message error code
        stat                 Machine state
        momo                 Gcode motion mode
        unit                 Gcode units
        macs                 Raw machine state
        cycs                 Cycle state
        mots                 Motion state
        hold                 Feedhold state
        coor                 Gcode coordinate system
        plan                 Gcode arc plane
        path                 Gcode path control mode
        dist                 Gcode distance mode
        frmo                 Gcode feed rate mode
        ===================  ===========================================

        :param str msgtype: (string) type of status message
        :param int code: (int) status report code
        :returns: message
        :rtype: str
        """
        value = ""
        messages = {
            'footer':["OK", "Error"],
            'error':[],
            'stat':["Machine initializing", "Machine ready", "Machine in soft alarm state",
                    "Program stop or no more blocks", "Program end", "Motion is running",
                    "Motion is holding", "Probe cycle active", "Machine is homing",
                    "Machine is jogging", "Machine in hard alarm state"],
            'momo':["G0", "G1", "G2", "G3", "G80"],
            'unit':["G20 (inch)", "G21 (mm)"],
            'macs':["Machine initializing", "Machine ready", "Machine in soft alarm state",
                    "Program stop or no more blocks", "Program end", "Machine in cycle",
                    "Machine in shutdown"],
            'cycs':["No cycle", "Normal cycle", "Probe cycle", "Homing cycle", "Jog cycle"],
            'mots':["Motion off", "Motion run", "Motion hold"],
            'hold':["Feedhold off", "Feedhold sync phase", "Feedhold planning phase",
                    "Feedhold deceleration phase", "Feedhold holding", "Feedhold end hold"],
            'coor':["G53", "G54", "G55", "G56", "G57", "G58", "G59"],
            'plan':["G17 (xy)", "G18 (xz)", "G19 (yz)"],
            'path':["G61 (exact path)", "G61.1 (exact stop)", "G64 (continuous)"],
            'dist':["G90 (absolute)", "G91 (incremental)"],
            'frmo':["G93 (inv time)", "G94 (u/min)", "G95(u/rev)"]
        }
        if code < 0:
            raise ValueError("Invalid error code")
        if not msgtype in messages.keys():
            raise ValueError("Invalid status message type.")
        if code < len(messages[msgtype]):
            value = messages[msgtype][code]
        else:
            value = "Unknown"
        return value
        
    
    def getMachineMenu(self):
        """
        See :meth:´Base.MachineBase.MachineBase.getMachineMenu´
        """
        menu = QtWidgets.QMenu("TinyG")
        testpanelaction = menu.addAction("Com Testpanel")
        testpanelaction.triggered.connect(self.mnuTinyGTestpanel_triggered)
        resetaction = menu.addAction("Reset")
        resetaction.triggered.connect(self.mnuTinyGReset_triggered)
        clearaction = menu.addAction("Clear")
        clearaction.triggered.connect(self.mnuTinyGClear_triggered)
        return menu
        
    
    @QtCore.pyqtSlot()
    def mnuTinyGTestpanel_triggered(self):
        """
        Slot triggered when the testpanel menu entry is clicked
        """
        if not self.isInitialized():
            QtWidgets.QMessageBox.critical(None, "Not initialized", 
                "Machine communication is not initialized!")
            return
        self.testpanel = TinyGTestpanel(self)
        self.testpanel.show()
        
    @QtCore.pyqtSlot()
    def mnuTinyGReset_triggered(self):
        """
        Slot triggered when the reset menu entry is clicked
        """
        if not self.isInitialized():
            QtWidgets.QMessageBox.critical(None, "Not initialized", 
                "Machine communication is not initialized!")
            return
        self.reset()
    
    @QtCore.pyqtSlot()
    def mnuTinyGClear_triggered(self):
        """
        Slot triggered when the clear menu entry is clicked
        """
        if not self.isInitialized():
            QtWidgets.QMessageBox.critical(None, "Not initialized", 
                "Machine communication is not initialized!")
            return
        self.executeCommand({"clear":None})
    
    
    @staticmethod
    def getComParameters():
        """
        See :meth:´Base.MachineBase.MachineBase.getComParameters´
        """
        params = {
            'name':'TinyGComSettings', 'type':'group', 'children':[
                {
                    'name':'com',
                    'title':'Com Port', 
                    'type':'list', 
                    'values':{port.description: port.device for port in slp.comports()}
                },
                {
                    'name':'baud',
                    'title':'Baudrate', 
                    'type':'list', 
                    'values':[9600, 19200, 38400, 57600, 115200, 230400],
                    'value':115200
                },
                {
                    'name':'flowctrl',
                    'title':'Flow Control', 
                    'type':'list', 
                    'values':{'None':0, 'XON/XOFF':1, 'RTS/CTS':2}, 
                    'value':'None'
                },
                {
                    'name':'timeout',
                    'title':'Timeout (s)',
                    'type':'float',
                    'min':0,
                    'default':1,
                    'value':1
                }
            ]
        }
        return ptypes.GroupParameter(**params)
    
    @staticmethod
    def updateComParameters(params):
        """
        See :meth:´Base.MachineBase.MachineBase.updateComParameters´
        """
        ports = {port.description: port.device for port in slp.comports()}
        params.child('com').setOpts(values=ports, limits=ports)
    
    
    @staticmethod
    def getParameters():
        """
        See :meth:´Base.MachineBase.MachineBase.getParameters´
        """
        params = {
            'name':'TinyGSettings', 'type':'group', 'children':[
                {
                    'name':'general', 'title':'General settings', 'type':'group', 'children':[
                        {
                            'name':'si',
                            'title':'Status report interval (ms)',
                            'type':'int',
                            'min':50,
                            'max':1000,
                            'default':200,
                            'value':200
                        }
                    ]
                },
                {
                    'name':'motor', 'title':'Motor settings', 'type':'group', 'children':[
                        {
                            'name':'1ma', 
                            'title':'Motor 1 axis', 
                            'type':'list',
                            'values':{'X':0, 'Y':1, 'Z':2}, 
                            'default':0, 
                            'value':0
                        },
                        {
                            'name':'2ma', 
                            'title':'Motor 2 axis', 
                            'type':'list',
                            'values':{'X':0, 'Y':1, 'Z':2}, 
                            'default':1, 
                            'value':1
                        },
                        {
                            'name':'3ma', 
                            'title':'Motor 3 axis', 
                            'type':'list',
                            'values':{'X':0, 'Y':1, 'Z':2}, 
                            'default':2, 
                            'value':2
                        },
                        {
                            'name':'1sa', 
                            'title':'Motor 1 step angle (deg)', 
                            'type':'float',
                            'min':0,
                            'default':1.8, 
                            'value':1.8
                        },
                        {
                            'name':'2sa', 
                            'title':'Motor 2 step angle (deg)', 
                            'type':'float',
                            'min':0,
                            'default':1.8, 
                            'value':1.8
                        },
                        {
                            'name':'3sa', 
                            'title':'Motor 3 step angle (deg)', 
                            'type':'float',
                            'min':0,
                            'default':1.8, 
                            'value':1.8
                        },
                        {
                            'name':'1tr',
                            'title':'Motor 1 travel per revolution (mm)',
                            'type':'float',
                            'min':0,
                            'decimals':5,
                            'default':2.54,
                            'value':2.54
                        },
                        {
                            'name':'2tr',
                            'title':'Motor 2 travel per revolution (mm)',
                            'type':'float',
                            'min':0,
                            'decimals':5,
                            'default':2.54,
                            'value':2.54
                        },
                        {
                            'name':'3tr',
                            'title':'Motor 3 travel per revolution (mm)',
                            'type':'float',
                            'min':0,
                            'decimals':5,
                            'default':2.54,
                            'value':2.54
                        },
                        {
                            'name':'1mi',
                            'title':'Motor 1 microsteps',
                            'type':'list',
                            'values':[1, 2, 4, 8],
                            'default':2,
                            'value':2
                        }
                        ,
                        {
                            'name':'2mi',
                            'title':'Motor 2 microsteps',
                            'type':'list',
                            'values':[1, 2, 4, 8],
                            'default':2,
                            'value':2
                        }
                        ,
                        {
                            'name':'3mi',
                            'title':'Motor 3 microsteps',
                            'type':'list',
                            'values':[1, 2, 4, 8],
                            'default':2,
                            'value':2
                        },
                        {
                            'name':'1po',
                            'title':'Motor 1 polarity',
                            'type':'list',
                            'values':{'Clockwise':0, 'Counterclockwise':1},
                            'default':0,
                            'value':0
                        },
                        {
                            'name':'2po',
                            'title':'Motor 2 polarity',
                            'type':'list',
                            'values':{'Clockwise':0, 'Counterclockwise':1},
                            'default':0,
                            'value':0
                        },
                        {
                            'name':'3po',
                            'title':'Motor 3 polarity',
                            'type':'list',
                            'values':{'Clockwise':0, 'Counterclockwise':1},
                            'default':0,
                            'value':0
                        },
                        {
                            'name':'1pm',
                            'title':'Motor 1 power management',
                            'type':'list',
                            'values':{'Motor disabled':0, 'Always on':1, 'On during cycle':2, 'On when moving':3},
                            'default':2,
                            'value':2
                        },
                        {
                            'name':'2pm',
                            'title':'Motor 2 power management',
                            'type':'list',
                            'values':{'Motor disabled':0, 'Always on':1, 'On during cycle':2, 'On when moving':3},
                            'default':2,
                            'value':2
                        },
                        {
                            'name':'3pm',
                            'title':'Motor 3 power management',
                            'type':'list',
                            'values':{'Motor disabled':0, 'Always on':1, 'On during cycle':2, 'On when moving':3},
                            'default':2,
                            'value':2
                        }
                    ]
                },
                {
                    'name':'axis', 'title':'Axis settings', 'type':'group', 'children':[
                        {
                            'name':'xfr',
                            'title':'X axis feed rate upper limit (mm/min)',
                            'type':'float',
                            'min':0,
                            'default':1000,
                            'value':1000
                        },
                        {
                            'name':'yfr',
                            'title':'Y axis feed rate upper limit (mm/min)',
                            'type':'float',
                            'min':0,
                            'default':1000,
                            'value':1000
                        },
                        {
                            'name':'zfr',
                            'title':'Z axis feed rate upper limit (mm/min)',
                            'type':'float',
                            'min':0,
                            'default':1000,
                            'value':1000
                        },
                        {
                            'name':'sl',
                            'title':'Enable soft limits',
                            'type':'list',
                            'values':{'No':0, 'Yes':1},
                            'default':1,
                            'value':1
                        },
                        {
                            'name':'xtn',
                            'title':'X axis travel minimum (mm)',
                            'type':'float',
                            'default':0,
                            'value':0
                        },
                        {
                            'name':'xtm',
                            'title':'X axis travel maximum (mm)',
                            'type':'float',
                            'default':300,
                            'value':300
                        },
                        {
                            'name':'ytn',
                            'title':'Y axis travel minimum (mm)',
                            'type':'float',
                            'default':0,
                            'value':0
                        },
                        {
                            'name':'ytm',
                            'title':'Y axis travel maximum (mm)',
                            'type':'float',
                            'default':300,
                            'value':300
                        },
                        {
                            'name':'ztn',
                            'title':'Z axis travel minimum (mm)',
                            'type':'float',
                            'default':0,
                            'value':0
                        },
                        {
                            'name':'ztm',
                            'title':'Z axis travel maximum (mm)',
                            'type':'float',
                            'default':300,
                            'value':300
                        },
                        {
                            'name':'xjm',
                            'title':'X axis maximum jerk (10^6 mm/min^3)',
                            'type':'float',
                            'min':0,
                            'default':50,
                            'value':50
                        },
                        {
                            'name':'yjm',
                            'title':'Y axis maximum jerk (10^6 mm/min^3)',
                            'type':'float',
                            'min':0,
                            'default':50,
                            'value':50
                        },
                        {
                            'name':'zjm',
                            'title':'Z axis maximum jerk (10^6 mm/min^3)',
                            'type':'float',
                            'min':0,
                            'default':50,
                            'value':50
                        },
                        {
                            'name':'xjd',
                            'title':'X axis junction deviation (mm)',
                            'type':'float',
                            'min':0,
                            'default':0.05,
                            'value':0.05
                        },
                        {
                            'name':'yjd',
                            'title':'Y axis junction deviation (mm)',
                            'type':'float',
                            'min':0,
                            'default':0.05,
                            'value':0.05
                        },
                        {
                            'name':'zjd',
                            'title':'Z axis junction deviation (mm)',
                            'type':'float',
                            'min':0,
                            'default':0.05,
                            'value':0.05
                        },
                        {
                            'name':'ja',
                            'title':'Junction acceleration (mm/min^2)',
                            'type':'float',
                            'min':0,
                            'default':50000,
                            'value':50000
                        }
                    ]
                },
                {
                    'name':'homing', 'title':'Homing settings', 'type':'group', 'children':[
                        {
                            'name':'st',
                            'title':'Switch type',
                            'type':'list',
                            'values':{'Normally open':0, 'Normally closed':1},
                            'default':1,
                            'value':1
                        },
                        {
                            'name':'xsn',
                            'title':'X minimum switch',
                            'type':'list',
                            'values':{'Disabled':0, 'Homing only':1, 'Limit only':2, 'Homing & limit':3},
                            'default':3,
                            'value':3
                        },
                        {
                            'name':'xsx',
                            'title':'X maximum switch',
                            'type':'list',
                            'values':{'Disabled':0, 'Homing only':1, 'Limit only':2, 'Homing & limit':3},
                            'default':0,
                            'value':0
                        },
                        {
                            'name':'ysn',
                            'title':'Y minimum switch',
                            'type':'list',
                            'values':{'Disabled':0, 'Homing only':1, 'Limit only':2, 'Homing & limit':3},
                            'default':3,
                            'value':3
                        },
                        {
                            'name':'ysx',
                            'title':'Y maximum switch',
                            'type':'list',
                            'values':{'Disabled':0, 'Homing only':1, 'Limit only':2, 'Homing & limit':3},
                            'default':0,
                            'value':0
                        },
                        {
                            'name':'zsn',
                            'title':'Z minimum switch',
                            'type':'list',
                            'values':{'Disabled':0, 'Homing only':1, 'Limit only':2, 'Homing & limit':3},
                            'default':0,
                            'value':0
                        },
                        {
                            'name':'asx',
                            'title':'A axis maximum switch',
                            'type':'list',
                            'values':{'Disabled':0, 'Limit only':2},
                            'default':2,
                            'value':2
                        },
                        {
                            'name':'asn',
                            'title':'A axis minimum switch',
                            'type':'list',
                            'values':{'Disabled':0, 'Limit only':2},
                            'default':2,
                            'value':2
                        },
                        {
                            'name':'zsx',
                            'title':'Z maximum switch',
                            'type':'list',
                            'values':{'Disabled':0, 'Homing only':1, 'Limit only':2, 'Homing & limit':3},
                            'default':3,
                            'value':3
                        },
                        {
                            'name':'xsv',
                            'title':'X axis homing search velocity (mm/min)',
                            'type':'float',
                            'min':0,
                            'default':500,
                            'value':500
                        },
                        {
                            'name':'ysv',
                            'title':'Y axis homing search velocity (mm/min)',
                            'type':'float',
                            'min':0,
                            'default':500,
                            'value':500
                        },
                        {
                            'name':'zsv',
                            'title':'Z axis homing search velocity (mm/min)',
                            'type':'float',
                            'min':0,
                            'default':500,
                            'value':500
                        },
                        {
                            'name':'xlv',
                            'title':'X axis homing latch velocity (mm/min)',
                            'type':'float',
                            'min':0,
                            'default':100,
                            'value':100
                        },
                        {
                            'name':'ylv',
                            'title':'Y axis homing latch velocity (mm/min)',
                            'type':'float',
                            'min':0,
                            'default':10,
                            'value':10
                        },
                        {
                            'name':'zlv',
                            'title':'Z axis homing latch velocity (mm/min)',
                            'type':'float',
                            'min':0,
                            'default':10,
                            'value':10
                        },
                        {
                            'name':'xjh',
                            'title':'X axis homing jerk (10^6 mm/min^3)',
                            'type':'float',
                            'min':0,
                            'default':100,
                            'value':100
                        },
                        {
                            'name':'yjh',
                            'title':'Y axis homing jerk (10^6 mm/min^3)',
                            'type':'float',
                            'min':0,
                            'default':100,
                            'value':100
                        },
                        {
                            'name':'zjh',
                            'title':'Z axis homing jerk (10^6 mm/min^3)',
                            'type':'float',
                            'min':0,
                            'default':100,
                            'value':100
                        },
                        {
                            'name':'xlb',
                            'title':'X axis homing backoff (mm)',
                            'type':'float',
                            'min':0,
                            'default':5,
                            'value':5
                        },
                        {
                            'name':'ylb',
                            'title':'Y axis homing backoff (mm)',
                            'type':'float',
                            'min':0,
                            'default':5,
                            'value':5
                        },
                        {
                            'name':'zlb',
                            'title':'Z axis homing backoff (mm)',
                            'type':'float',
                            'min':0,
                            'default':5,
                            'value':5
                        },
                        {
                            'name':'xzb',
                            'title':'X axis zero backoff (mm)',
                            'type':'float',
                            'min':0,
                            'default':5,
                            'value':5
                        },
                        {
                            'name':'yzb',
                            'title':'Y axis zero backoff (mm)',
                            'type':'float',
                            'min':0,
                            'default':5,
                            'value':5
                        },
                        {
                            'name':'zzb',
                            'title':'Z axis zero backoff (mm)',
                            'type':'float',
                            'min':0,
                            'default':5,
                            'value':5
                        }
                    ]
                }
            ]
        }
        return ptypes.GroupParameter(**params)
        