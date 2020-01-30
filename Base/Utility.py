"""
Created on 13.02.2018

@author: Christian Ott
"""

import numpy as np
from PyQt5 import QtGui, QtCore

import Base.Errors as errs

def createSimpleTriangle(center, width, height, orientation="up"):
    """
    Returns a QtPolygon containing a simple triangle.

    :param center: Center coordinates of the triangle's bounding box
    :type center: tuple(float, float)
    :param float width: Width of the triangles bounding box
    :param float height: Height of the triangles bounding box
    :param str orientation: Orientation of the triangle (tip direction)
                            Valid values are "up", "down"
    """
    polygon = QtGui.QPolygonF()
    if orientation == "up":
        polygon.append(QtCore.QPointF(center[0]-width/2, center[1]-height/2))
        polygon.append(QtCore.QPointF(center[0]+width/2, center[1]-height/2))
        polygon.append(QtCore.QPointF(center[0], center[1]+height/2))
        polygon.append(QtCore.QPointF(center[0]-width/2, center[1]-height/2))
    if orientation == "down":
        polygon.append(QtCore.QPointF(center[0]-width/2, center[1]+height/2))
        polygon.append(QtCore.QPointF(center[0]+width/2, center[1]+height/2))
        polygon.append(QtCore.QPointF(center[0], center[1]-height/2))
        polygon.append(QtCore.QPointF(center[0]-width/2, center[1]+height/2))
    return polygon


def calculateAngle(vec1, vec2):
    """
    Calculates the angle between two 2-dim vectors. Note that the zero vector is invalid.

    :param np.ndarray vec1: First vector
    :param np.ndarray vec2: Second vector
    :returns: angle between the vectors
    :rtype: float
    """
    if not np.any(vec1) or not np.any(vec2):
        raise errs.InvalidArgument("vec1, vec2", "Zero vectors are not allowed.")
    if vec1.shape != (2,) or  vec2.shape != (2,):
        raise errs.InvalidArgument("vec1, vec2", "Invalid vector dimensions.")
    #val = np.dot(vec1, vec2)/np.linalg.norm(vec1)/np.linalg.norm(vec2)
    #return np.arccos(np.clip(val, -1, 1))
    angle1 = np.arctan2(vec1[1], vec1[0])
    angle2 = np.arctan2(vec2[1], vec2[0])
    return angle2-angle1


def create2DRotation(angle):
    """
    Creates a 2D rotation matrix.

    :param float angle: Angle in radiant
    :returns: 2x2 rotation matrix
    :rtype: np.ndarray
    """
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[c, -s], [s, c]])
        
    
def degToRad(angle):
    """
    Transforms angle from degree to radiant.

    :param float ange: angle to transform
    """
    return angle * np.pi/180
    
    
def radToDeg(angle):
    """
    Transforms angle from radiant to degree.

    :param float ange: angle to transform
    """
    return angle * 180/np.pi