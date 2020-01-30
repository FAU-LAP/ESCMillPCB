"""
Created on 04.02.2018

@author: Christian Ott
"""

import logging
#logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s:%(message)s", 
#                                        level=logging.DEBUG)

import sys, os.path, traceback, timeit
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import networkx as nx
import matplotlib.pyplot as plt
import pyqtgraph as pg

from Base.AppBase import AppBase
from Base.ImportFactory import ImportFactory
import Base.MachiningObjects as mo
from ui.MachiningROIs import HoleROI, StraightMillingROI, ArcMillingROI
from ui.WorkpieceWidget import WorkpieceWidget 
from Algorithms.TSPOptimizer import greedy, twoOpt1, twoOpt2, twoOpt3
from Algorithms.NXUtilities import nodePath, randomPathGraph
from Algorithms import NXUtilities as nxutils

def handle_exception(exc_type, exc_value, exc_traceback):  
    """ handle all exceptions """

    ## KeyboardInterrupt is a special case.
    ## We don't raise the error dialog when it occurs.
    if issubclass(exc_type, KeyboardInterrupt):
        if QtWidgets.qApp:
            QtWidgets.qApp.quit()
        return

    filename, line, dummy, dummy = traceback.extract_tb( exc_traceback ).pop()
    filename = os.path.basename( filename )
    error    = "%s: %s" % ( exc_type.__name__, exc_value )

    QtWidgets.QMessageBox.critical(None,"Error",
        "<html>A critical error has occured.<br/> "
        + "<b>%s</b><br/><br/>" % error
        + "It occurred at <b>line %d</b> of file <b>%s</b>.<br/>" % (line, filename)
        + "</html>")

    print("Closed due to an error. This is the full error report:")
    print()
    print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
  
# install handler for exceptions
sys.excepthook = handle_exception
  
pg.setConfigOptions(imageAxisOrder='row-major')
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

AppBase.initialize()

## create GUI
app = QtWidgets.QApplication([])
# w = pg.GraphicsWindow(size=(1000,800), border=True)
# w.setWindowTitle('ESCMillPCB test')
# w.show()
# g = pg.PlotItem()
# w.addItem(g)

filepath = r"_test\esc_spray_etcher.brd"
imp = ImportFactory()
workpiece = imp.importFile(filepath, "eagle")
#workpiece.optimize()

nodes = np.array([hole.center for hole in workpiece.holeList])

ngr = nx.Graph()
for i, hole in enumerate(nodes):
    for j, hole2 in enumerate(nodes):
        if not i == j:
            ngr.add_edge(i, j, weight=np.sqrt(np.sum((hole-hole2)**2)))

## distance calculation conservative way
def dist1(nodes):
    distances = np.empty([nodes.shape[0], nodes.shape[0]])
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            distances[i, j] = np.linalg.norm(node1-node2)
    return distances

## distance calculation numpy way
def dist2(nodes):
    tmp = np.tile(nodes, (nodes.shape[0], 1, 1))
    tmp = tmp - nodes[:,np.newaxis,:]
    tmp = tmp**2
    tmp = tmp[:,:,0] + tmp[:,:,1]
    distances = np.sqrt(tmp)
    return distances

distances1 = dist1(nodes)
distances2 = dist2(nodes)

print(np.all(distances1 == distances2)) # ergibt False
print(np.all(np.abs(distances1 - distances2) < 1e-13)) # ergibt True
print(np.all(np.abs(distances1 - distances2) < 1e-14)) # ergibt False
print("{:e}".format(np.min(np.abs(distances1 - distances2)))) # ergibt "0.00000e+0"

print("-------------------------")
print(nodes.shape)
print(timeit.timeit('dist1(nodes)', setup='from __main__ import dist1, nodes', number=10)/10)
print(timeit.timeit('dist2(nodes)', setup='from __main__ import dist2, nodes', number=1000)/1000)

print("-------------------------")
print(np.linalg.norm(nodes[10,:] - nodes[103,:]))
print(distances1[10, 103])
print(distances2[10, 103])

print("-------------------------")
print(timeit.timeit('twoOpt1(ngr, 5)', setup='from __main__ import twoOpt1, ngr', number=1))
print(timeit.timeit('twoOpt2(nodes, 5)', setup='from __main__ import twoOpt2, nodes', number=1))
print(timeit.timeit('twoOpt3(nodes, 5)', setup='from __main__ import twoOpt3, nodes', number=1))

print("-------------------------")
#print(timeit.timeit('greedy1(ngr)', setup='from __main__ import greedy1, ngr', number=1))
print(timeit.timeit('greedy(nodes)', setup='from __main__ import greedy, nodes', number=1))

order = twoOpt3(nodes, 50)
#order = greedy(nodes)
workpiece.holeList.reorder(order)

print("-------------------------")
print("Final path length: {}".format(nxutils.pathDistanceFromNodes(nodes, order)))

wnd = QtWidgets.QWidget()
wnd.setWindowTitle("ESCMillPCB test")
wnd.resize(1000, 1000)
ww = WorkpieceWidget(parent=wnd)
ww.setWorkpiece(workpiece)
ww.resize(1000, 1000)
wnd.show()


# data = np.empty(shape=[len(holelist.holes),2])
# ngr = nx.Graph()
# 
# sizes = []
# for i, hole in enumerate(holelist.holes):
#     data[i,] = hole.center
#     #sizes.append(hole.diameter*10)
#     r = HoleROI(hole.diameter, pos=hole.center)
#     g.addItem(r)
#     ngr.add_node(i, {"pos":hole.center})
#     
# for mill in millings.pathList:
#     print(type(mill))
#     if isinstance(mill, mo.StraightPath):
#         r = StraightMillingROI(mill.start, mill.end, True, True)
#         g.addItem(r)
#     elif isinstance(mill, mo.ArcPath):
#         r = ArcMillingROI(mill.start, mill.end, np.array(mill.start)+np.array(mill.offset), True, True)
#         g.addItem(r)
#     
# 
# for i, hole in enumerate(data):
#     for j, hole2 in enumerate(data):
#         if not i == j:
#             ngr.add_edge(i, j, {"weight" : np.sqrt(np.sum((hole-hole2)**2))})        
#         
# optimized = greedy(ngr)
# 
# odata = np.empty(shape=[len(holelist.holes),2])
# path = nodePath(optimized)
# for i, node in enumerate(path):
#     odata[i,] = holelist.holes[node].center
#print(odata)

# optimized2 = twoOpt(ngr)
#nx.draw(optimized2)
#plt.show()

# path = nodePath(optimized2)
# for i, node in enumerate(path):
#     odata[i,] = holelist.holes[node].center
# #print(odata)
# 
# g.plot(odata, pen=pg.mkPen("r"))
# 
# print("Random graph size: {}".format(rndgraph.size("weight")))
# print("Greedy graph size: {}".format(optimized.size("weight")))
# print("2opt graph size: {}".format(optimized2.size("weight")))

app.exec_()

