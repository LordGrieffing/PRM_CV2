#!/usr/bin/python3

import cv2
import numpy as np
import networkx as nx
import random as rd
import math
import time
import find_frontier_cell as ff



def generateSample(height, width):
    """
    generateSample function generates a random coordinate within a space based on the provided height and width

    :param height: height of the space 
    :param width: width of the space
    :return: A list of an x coordinate and a y coordinate
    """
    sample_x = rd.randrange(0, height)
    sample_y = rd.randrange(0, width)

    #print([sample_x, sample_y])
    
    return [sample_x, sample_y]

def mySubtract(imgLast, imgNext, Height, Width):
    """
    mySubtract function takes in two images and marks any space that is Collision free in both (color of 254) as an obstacle. This leaves you with 
    space that is only collision free in the latest image

    :param imgLast: The previous map before exploration (as a .pgm)
    :param imgNext: The current map after exploration (as a .pgm)
    :return: A numpy array that has the updated collision free space
    """
    temp_Next = np.copy(imgNext)
    for i in range(Height):
        for j in range(Width):
            if imgLast[i, j] == 254:
                temp_Next[i, j] = 0


    return temp_Next

def getLargestNode(Exgraph):
    """
    getLargestNode function takes in a correctly formated networkx graph (formatting provided in the README.md) and returns the largest numbered node
    from the graph provided.

    :param Exgraph: A networkx graph object
    :return: An int that designates the latest node to be added
    """
    list_of_Nodes = list(Exgraph.nodes)
    largestNode = 0

    # Check if the graph is empty
    if not list_of_Nodes:
        return largestNode
    
    for i in range(len(list_of_Nodes)):
        if list_of_Nodes[i] >= largestNode:
            largestNode = list_of_Nodes[i]

    return largestNode

def check_if_neighbor(currentNode, neighborNode, radius):
    """
    check_if_neighbor function checks if two nodes are neighbors. The two nodes are considered neighbors if the distance between the two nodes is less
    than the radius

    :param currentNode: List of ints containing the coordinates of the current node
    :param neighborNode: List of ints containing the coordinates of the potential neighbor node
    :param radius: The int that reperesnts the radius that deteremines neighbors
    :return: Bool True if neighbors False if not neighbors
    """

    nodeDist = math.dist(currentNode, neighborNode)

    if nodeDist <= radius:
        return True
    
    else:
        return False
    
def bresenham_line(x1, y1, x2, y2):
    """
    bresenham_line function performs the bresenham line algorithm between the two points provided.  This function was written by ChatGPT

    :param x1: The x coordinate of the first point
    :param y1: The y coordinate of the first point
    :param x2: The x coordniate of the second point
    :param y2: The y coordniate of the second point
    :return: A list of tuples containing the x and y coordniates of each point on the line
    """
    # Setup initial conditions
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    # Decision variables for determining the next point
    if dx > dy:
        err = dx / 2
        while x != x2:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2
        while y != y2:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy

    points.append((x, y))  # Add the final point
    return points
    
def check_legal_edge(currentNode, neighborNode, img):
    """
    check_legal_edge function checks if the edge between two points interescts with an obstacle.

    :param currentNode: A list containing the coordinates of the current node
    :param neighborNode: A list containing the coordinates of the neighbor node
    :param img: The Image that the graph is being built over
    :return: Bool that is True if the edge does not interesct with an obsticle, False if it does
    """
    line = []
    line = bresenham_line(int(currentNode[0]), int(currentNode[1]), int(neighborNode[0]), int(neighborNode[1]))
    lineValid = True

    for j in range(len(line)):
        if img[line[j][0], line[j][1]] == 0 or img[line[j][0], line[j][1]] == 205:
            lineValid = False
            break

    return lineValid

def add_legal_edges(Exgraph, newNode, radius, img):
    """
    add_legal_edges function takes in a networkx object and a newly added node. It then builds edges from the new node and any prexisting node as long
    as it is legal. Legal meaning it is not colliding with any obstacles and isn't too far from the node.

    :param Exgraph: A networkx graph object
    :param newNode: A int that designates the most recently added node
    :param radius: The Maximum distance an edge is allowed to be
    :param img: The map that is being explored
    :return: The function returns nothing and just directly edits the networkx object
    """

    nodeList = list(Exgraph)
    newNodeCoords = [0, 0]
    currentNodeCoords = [0, 0]
    newNodeCoords[0] = Exgraph.nodes[newNode]['x']
    newNodeCoords[1] = Exgraph.nodes[newNode]['y']

    if len(nodeList) == 1:
        return 

    for i in range(len(nodeList)):
        currentNodeCoords[0] = Exgraph.nodes[nodeList[i]]['x']
        currentNodeCoords[1] = Exgraph.nodes[nodeList[i]]['y']

        neighbor = check_if_neighbor(newNodeCoords, currentNodeCoords, radius)

        if neighbor:
            legal_edge = check_legal_edge(newNodeCoords, currentNodeCoords, img)

            if legal_edge:
                Exgraph.add_edge(newNode, nodeList[i])

    return 
 
def prm(Exgraph, imgHeight, imgWidth, imgNext, imgLast = None, sampleNum = 100, radius = 40, frontierSample = 5):
    """
    prm function takes in a correctly formated networkx graph (formatting provided in the README.md) and an image. It will perform the PRM algorithm
    over the provided image and update the graph. If two images are provided it will subtract the two images and only sample in the area that is not 
    present in the first image. 

    :param Exgraph: A networkx graph object
    :param imgHeight: The height of the image provided in pixels
    :param imgWidth: The width of the image provided in pixels
    :param imgNext: The image that the graph will be built over (as a .pgm)
    :param imgLast: The previous image (Not the one you want to build a roadmap on) (as a .pgm)
    :param sampleNum: The number of samples taken from the provided image
    :param radius: The maximum distance that an edge can be built between two nodes
    :param frontierSample: The number of samples taken from frontier pixels (Pixels at the edge of Cspace and unknown space)
    :return: The updated networkx graph
    """
    
    graph_unfinished = True

    largestNode = getLargestNode(Exgraph)
    newMax = largestNode + sampleNum

    # -- Declare imgDelta outside of if to fix scope potentially?
    imgDelta = imgNext
    
    # -- Create a subtracted image if this isn't the first map
    if imgLast is not None:
        imgDelta = mySubtract(imgLast, imgNext, imgHeight, imgWidth)
    
    # -- Erode the image to account for robot size
    kernel = np.ones((3,3),np.uint8)
    imgDelta = cv2.erode(imgDelta, kernel, iterations = 1)



    # -- Run a while loop until the graph has the number of nodes specified by sampleNum

    
    for i in range(sampleNum):

        # -- Generate a sample
        legal_sample = False
        newSample = [0,0]

        while not legal_sample:
            
            newSample = generateSample(imgHeight, imgWidth)
            color = imgDelta[int(newSample[0]), int(newSample[1])]


            if np.all(color == 254):
                legal_sample = True

        # -- Add legal node to graph
        largestNode = largestNode + 1
        Exgraph.add_node(largestNode)
        Exgraph.nodes[largestNode]['x'] = newSample[0]
        Exgraph.nodes[largestNode]['y'] = newSample[1]

        #print(Exgraph)

        # -- add legal edges to sample
        add_legal_edges(Exgraph, largestNode, radius, imgNext)

        # -- check if graph is finished
        #print(Exgraph)

    # -- generate and add frontier cells
    frontier_cells = ff.get_frontier_image(imgNext)
    legal_sample = False
    frontier_finished = False
    newSample = [0,0]

    while not frontier_finished:
        print("Frontier in progress...")

        # -- Generate a sample inside of the frontier 
        

        for i in range(frontierSample):
            tempFront = rd.randrange(0, len(frontier_cells))
            newSample = frontier_cells[tempFront]
            # -- Add legal node to graph
            largestNode = largestNode + 1
            Exgraph.add_node(largestNode)
            Exgraph.nodes[largestNode]['x'] = newSample[0]
            Exgraph.nodes[largestNode]['y'] = newSample[1]

            # -- add legal edges to sample
            add_legal_edges(Exgraph, largestNode, radius, imgNext)

        frontier_finished = True

    return Exgraph