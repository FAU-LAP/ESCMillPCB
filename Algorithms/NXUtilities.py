"""
Created on 10.02.2018

@author: Christian Ott
"""

import numpy as np
import networkx as nx

def nodePath(graph):
    """
    Returns a list of nodes along a path in the graph.
    Works only for undirected path graphs which start at node 0.

    :param networkx.graph graph: Undirected path graph to traverse
    :returns: Nodes along path
    :rtype: list[int]
    """
    path = np.empty(shape=len(graph), dtype=int)
    path[0] = 0
    for i, edge in enumerate(nx.dfs_edges(graph)):
        path[i+1] = edge[1]
    return path


def randomPathGraph(graph):
    """
    :param networkx.graph graph: Undirected complete graph. Edge attributes are transfered.
        No changes to the original graph are made.
    :returns: Random undirected path graph starting at node 0
    :rtype: networkx.graph
    """
    graph = graph.copy()
    # Create random path by connecting them in a shuffled order
    nodes = list(graph.nodes())
    nodes.remove(0)
    np.random.shuffle(nodes)
    # remove all undesired edges
    edgelist = list(graph.edges())
    edgelist.remove((0, nodes[0]))
    for i in range(0, len(nodes)-1):
        try:
            edgelist.remove((nodes[i], nodes[i+1]))
        except:
            edgelist.remove((nodes[i+1], nodes[i]))
    graph.remove_edges_from(edgelist)
    return graph


def calculateAllDistances(nodes):
    """
    Calculates the distances between all nodes.

    :param np.ndarray nodes: Matrix containing all node coordinates.
    :returns: Matrix with entry i,j containing the distance between the i'th and j'th point
    :rtype: np.ndarray
    """
    # repeat nodes array on 3rd axis len(nodes) times
    tmp = np.tile(nodes, (nodes.shape[0], 1, 1))
    # subtract node coordinates of all nodes from each nodes array on 3rd axis 
    tmp = tmp - nodes[:,np.newaxis,:]
    tmp = tmp**2
    # add squared coordinates for each node
    tmp = tmp[:,:,0] + tmp[:,:,1]
    distances = np.sqrt(tmp)
    return distances


def calculateAllDistancesTwoPointNodes(nodes):
    """
    Calculates the distances between all nodes.
    This special version allows nodes to have different start and end points. Distances are
    calculated between the end point of one node and the start point of another node.

    :param nodes: Tuple of two matrices containing (start, end) coordinates of all nodes
    :type nodes: tuple[np.ndarray, np.ndarray]
    :returns: Matrix with entry i,j containing the distance between the i'th and j'th node
    :rtype: np.ndarray
    """
    # repeat start nodes array on 3rd axis len(nodes) times
    tmp = np.tile(nodes[0], (nodes[0].shape[0], 1, 1))
    # subtract node end coordinates of all nodes from each node start coordinates array on 3rd axis
    tmp = tmp - nodes[1][:,np.newaxis,:]
    tmp = tmp**2
    # add squared coordinates for each node
    tmp = tmp[:,:,0] + tmp[:,:,1]
    distances = np.sqrt(tmp)
    return distances 


def pathDistance(distances, nodeorder):
    """
    Calculates the length of a path from a distances array and a node-order array.

    :param np.ndarray distances: Matrix with entry i,j containing the distance between the i'th and j'th node
    :param np.ndarray nodeorder: Array containing the node indices in the path order
    :returns: path length
    :rtype: float
    """
    distance = 0
    for i in range(nodeorder.shape[0]-1):
        distance += distances[nodeorder[i], nodeorder[i+1]]
    return distance


def pathDistanceFromNodes(nodes, nodeorder):
    """
    Calculates the length of a path from a nodes array and a node-order array.

    :param np.ndarray nodes: (n, 2) matrix containing all node coordinates
    :param np.ndarray nodeorder: Array containing the node indices in the path order
    :returns: path length
    :rtype: float
    """
    distance = 0
    for i in range(nodeorder.shape[0]-1):
        distance += np.linalg.norm(nodes[nodeorder[i]] - nodes[nodeorder[i+1]])
    return distance


def pathDistanceFromTwoPointNodes(nodes, nodeorder):
    """
    Calculates the length of a path from a nodes array and a node-order array.
    This special version allows nodes to have different start and end points. Distances are
    calculated between the end point of one node and the start point of another node.

    :param nodes: Tuple of two matrices containing (start, end) coordinates of all nodes
    :type nodes: tuple(np.ndarray, np.ndarray)
    :param nodeorder: Array containing the node indices in the path order
    :type nodeorder: np.ndarray(int)
    :returns: path length
    :rtype: float
    """
    distance = 0
    for i in range(nodeorder.shape[0]-1):
        distance += np.linalg.norm(nodes[1][nodeorder[i]] - nodes[0][nodeorder[i+1]])
    return distance
