"""
Created on 09.02.2018

@author: christian
"""

#initialize logging
import logging
logger = logging.getLogger(__name__)

import numpy as np

from Algorithms import NXUtilities as nxutils


def _greedyCore(distances):
    """
    Core implementation of the greedy next neighbor algorithm.

    :param distances: Matrix with entry i,j containing the distance between the i'th and j'th node
    :type distances: np.ndarray(float)
    :returns: Array of node indices in optimized order
    :rtype: np.ndarray(int)
    """
    nodeorder = np.arange(0, distances.shape[0])
    nodesleft = np.arange(1, distances.shape[0])
    for i in range(0, distances.shape[0] - 1):
        # find index in distance array for smallest distance
        # take current node and all not already reordered nodes into account
        minindices = np.where(distances[nodeorder[i],:] == np.min(distances[nodeorder[i], nodesleft]))[0]
        minindex = None
        # take first index entry which is not already reordered
        # this takes into account that there might be distances with the same length
        for index in minindices:
            if index in nodesleft:
                minindex = index
                break
        nodeorder[i+1] = minindex
        nodesleft = np.delete(nodesleft, np.where(nodesleft == minindex)[0][0])
    return nodeorder


def greedy(nodes):
    """
    Greedy next neighbor algorithm to find the shortest path.

    numpy version.

    :param nodes: Matrix containing all node coordinates
    :type nodes: np.ndarray(float)
    :returns: Array of node indices in optimized order
    :rtype: np.ndarray(int)
    """
    distances = nxutils.calculateAllDistances(nodes)
    return _greedyCore(distances)


def greedyTwoPointNodes(nodes):
    """
    Special version of the greedy next neighbor algorithm to find the shortest path.
    In this version, nodes are allowed to have different start and end coordinates and
    the vertices are connecting the end coordinates of one node to the start coordinate of the
    next node. The algorithm reorders the nodes such that the overall length of the
    vertices is minimized.

    :param nodes: Tuple of two matrices containing (start, end) coordinates of all nodes
    :type nodes: tuple(np.ndarray, np.ndarray)
    :returns: Array of node indices in optimized order
    :rtype: np.ndarray(int)
    """
    distances = nxutils.calculateAllDistancesTwoPointNodes(nodes)
    return _greedyCore(distances)


def twoOpt1(graph, iterations=5):
    """
    2-opt algorithm to find the shortest path.

    networkx version (very slow!).

    This algorithm implements a complete 2-opt local search which tries to minimize
    the overall path weight by swapping connections and then choosing the shorter variant.
    The idea behind this is that by doing so crossing paths are removed.
    The algorithm optimizes _iterations_ random paths and returns the best solution.

    :param networkx.graph graph: Undirected graph to traverse. No changes are made to the original graph.
                                 The graph needs to be a complete graph with weighted edges.
    :returns: Undirected path graph starting at node 0.
    :rtype: networkx.graph
    """
    shortestDistance = float("inf")
    shortestPath = None
    for iteration in range(iterations):
        optimized = nxutils.randomPathGraph(graph)
        nodeorder = nxutils.nodePath(optimized)
        newDistance = optimized.size("weight")
        lastDistance = float("inf")
        # repeat until no further progress is made
        while newDistance < lastDistance:
            lastDistance = newDistance
            #print("step start: {}".format(lastDistance))
            # swap all node combinations but node 0
            for i in range(1, len(graph)-1):
                for k in range(i+1, len(graph)):
                    # check if swap would reduce path weight
                    # subtract edge weight first-1 <> fist (is removed if swapped)
                    delta = -graph.get_edge_data(nodeorder[i-1], nodeorder[i])["weight"]
                    # add edge weight first-1 <> second (is added if swapped)
                    tmpweight1 = graph.get_edge_data(nodeorder[i-1], nodeorder[k])["weight"]
                    delta += tmpweight1
                    # check if second is last node in path
                    tmpweight2 = 0
                    if k < len(nodeorder)-1:
                        # subtract edge weight second <> second+1 (is removed if swapped)
                        delta -= graph.get_edge_data(nodeorder[k], nodeorder[k+1])["weight"]
                        # add edge weight first <> second+1 (is added if swapped)
                        tmpweight2 = graph.get_edge_data(nodeorder[i], nodeorder[k+1])["weight"]
                        delta += tmpweight2
                    # if delta is < 0 then the swapped route is shorter
                    if delta <= 0:
                        # remove edge first-1 <> first
                        optimized.remove_edge(nodeorder[i-1], nodeorder[i])
                        # add edge first-1 <> second
                        optimized.add_edge(nodeorder[i-1], nodeorder[k], weight=tmpweight1)
                        # check if second is last node in path
                        if tmpweight2:
                            # remove edge second <> second+1
                            optimized.remove_edge(nodeorder[k], nodeorder[k+1])
                            # add edge first <> second+1
                            optimized.add_edge(nodeorder[i], nodeorder[k+1], weight=tmpweight2)
                        # update distance
                        newDistance += delta
                        # update node order
                        oldorder = nodeorder.copy()
                        nodeorder[i:k] = oldorder[k:i:-1]
                        nodeorder[k] = oldorder[i]
        logger.debug("2opt iteration %s: %.3f", iteration+1, newDistance)
        if newDistance < shortestDistance:
            shortestDistance = newDistance
            shortestPath = optimized.copy()
    return shortestPath
 
 
 
def twoOpt2(nodes, iterations=20):
    """
    2-opt algorithm to find the shortest path.

    Numpy version (still slow!).

    This algorithm implements a complete 2-opt local search which tries to minimize
    the overall path weight by swapping connections and then choosing the shorter variant.
    The idea behind this is that by doing so crossing paths are removed.
    See https://en.wikipedia.org/wiki/2-opt
    The algorithm optimizes _iterations_ random paths and returns the best solution.

    :param nodes: (n,2) matrix containing all node coordinates
    :type nodes: np.ndarray(float)
    :param int iterations: Number of random start configurations
    :returns: Array of node indices in optimized order
    :rtype: np.ndarray(int)
    """
    distances = nxutils.calculateAllDistances(nodes)
    shortestDistance = float("inf")
    shortestPath = None
    for iteration in range(iterations):
        nodeorder = np.concatenate([[0], np.random.permutation(np.arange(1, nodes.shape[0], dtype=np.int_))])
        newDistance = nxutils.pathDistance(distances, nodeorder)
        lastDistance = float("inf")
        # repeat until no further progress is made
        while newDistance < lastDistance:
            lastDistance = newDistance
            #logger.debug("Step start: {}".format(lastDistance))
            # swap all node combinations but node 0
            for i in range(1, nodeorder.shape[0]-1):
                for k in range(i+1, nodeorder.shape[0]):
                    # subtract edge weight first-1->first (is removed if swapped)
                    delta = -distances[nodeorder[i-1], nodeorder[i]]
                    # add edge weight first-1->second (is added if swapped)
                    delta += distances[nodeorder[i-1], nodeorder[k]]
                    # check if second is last node in path
                    if k < nodeorder.shape[0]-1:
                        # subtract edge weight second->second+1 (is removed if swapped)
                        delta -= distances[nodeorder[k], nodeorder[k+1]]
                        # add edge weight first->second+1 (is added if swapped)
                        delta += distances[nodeorder[i], nodeorder[k+1]]
                    # if delta is < 0 then the swapped route is shorter
                    if delta <= 0:
                        oldnodeorder = nodeorder.copy()
                        nodeorder[i:k] = oldnodeorder[k:i:-1]
                        nodeorder[k] = oldnodeorder[i]
                        # update distance
                        newDistance += delta
        logger.debug("2opt iteration %s: %.3f", iteration+1, newDistance)
        if newDistance < shortestDistance:
            shortestDistance = newDistance
            shortestPath = nodeorder
    return shortestPath


def twoOpt3(nodes, iterations=5):
    """
    2-opt algorithm to find the shortest path.

    Optimized numpy version.

    This algorithm implements a complete 2-opt local search which tries to minimize
    the overall path weight by swapping connections and then choosing the shorter variant.
    The idea behind this is that by doing so crossing paths are removed.
    See https://en.wikipedia.org/wiki/2-opt
    It differs slightly from the original algorithm, because it calculates all swap possibilities
    for one given node and then picks the best one. This is then repeated for all following nodes.
    This whole process is then repeated until no further improvement of the total path length is achieved.
    The algorithm optimizes *iterations* random paths and returns the best solution.

    :param nodes: (n, 2) matrix containing all node coordinates
    :type nodes: np.ndarray(float)
    :param int iterations: Number of random start configurations
    :returns: Array of node indices in optimized order
    :rtype: np.ndarray(int)
    """
    distances = nxutils.calculateAllDistances(nodes)
    shortestDistance = float("inf")
    shortestPath = None
    for iteration in range(iterations):
        nodeorder = np.concatenate([np.random.permutation(np.arange(0, nodes.shape[0], dtype=np.int_))])
        newDistance = nxutils.pathDistance(distances, nodeorder)
        lastDistance = float("inf")
        # repeat until no further progress is made
        while newDistance < lastDistance:
            lastDistance = newDistance
            #logger.debug("Step start: {}".format(lastDistance))
            # swap all node combinations but node 0
            for i in range(1, nodeorder.shape[0]-1):
                krange = np.arange(i+1, nodeorder.shape[0])
                delta = np.empty(krange.shape[0])
                # subtract edge weight first-1->first (is removed if swapped)
                delta.fill(-distances[nodeorder[i-1], nodeorder[i]])
                # add edge weight first-1->second for all possible second nodes (is added if swapped)
                delta += distances[nodeorder[i-1], nodeorder[krange]]
                # subtract edge weight second->second+1 for all second nodes (is removed if swapped)
                # only possible if the second node is not the last -> 0 change for last node
                delta -= np.concatenate([distances[nodeorder[krange[:-1]], nodeorder[krange[1:]]], [0]])
                # add edge weight first->second+1 for all second nodes (is added if swapped)
                # only possible if the second node is not the last -> 0 change for last node
                delta += np.concatenate([distances[nodeorder[i], nodeorder[krange[1:]]], [0]])
                # find the best possible swap candidate
                bestindex = np.where(delta == np.min(delta))[0][0]
                bestswap = krange[bestindex]
                if delta[bestindex] <= 0:
                    oldnodeorder = nodeorder.copy()
                    nodeorder[i:bestswap] = oldnodeorder[bestswap:i:-1]
                    nodeorder[bestswap] = oldnodeorder[i]
                    # update distance
                    newDistance += delta[bestindex]
        logger.debug("2opt iteration %s: %.3f", iteration+1, newDistance)
        if newDistance < shortestDistance:
            shortestDistance = newDistance
            shortestPath = nodeorder
    return shortestPath
