#!/usr/bin/python3

# Importing external Libraries
import cv2
import numpy as np
import networkx as nx
import random as rd
import math
import time

#Importing internal Libraries
from PRM import PRM_main as prm













def main():

    # -- Intialize variable to store different stages of the graph
    graphs = []
    # -- Loading the different maps
    maps =  []
    for i in range(8):
        maps.append(cv2.imread("resources/input/map" + str(i + 1) + ".pgm", 0))
    
    # -- initalize the networkx graph
    Exgraph = nx.Graph()

    # -- get image height and width in this case all the maps are the same size so this information only needs to be grabbed once
    imgHeight, imgWidth = maps[0].shape

    # -- This loop runs for each map
    for i in range(8):

        imgLast = None

        if i > 0:
            imgLast = maps[i-1]

        Exgraph = prm.prm(Exgraph, imgHeight, imgWidth, maps[i], imgLast, 5, 90)
        tempgraph = nx.Graph()
        tempgraph.add_nodes_from(Exgraph)
        tempgraph.add_edges_from(Exgraph.edges)
        graphs.append(tempgraph)
        print(graphs[i])

    # This section of the code is soley for the purposes of displaying the graphs
    # If you are looking to use this code in a mobile robot or other application where the just need the data then this is not nessecery 
        
    # -- Display the graphs
    for i in range(8):
        painted_map = (cv2.cvtColor(maps[i], cv2.COLOR_GRAY2BGR))
        nodeList = list(graphs[i].nodes)
        edgeList = list(graphs[i].edges)

        # -- add nodes
        for j in range(len(nodeList)):
            nodeCoords = (Exgraph.nodes[nodeList[j]]['y'], Exgraph.nodes[nodeList[j]]['x'])
            cv2.circle(painted_map, nodeCoords, 4, (255, 0, 0), -1)

        for j in range(len(edgeList)):
            
            currentEdge = edgeList[j]
            cv2.line(painted_map, (Exgraph.nodes[currentEdge[0]]['y'], Exgraph.nodes[currentEdge[0]]['x']), (Exgraph.nodes[currentEdge[1]]['y'], Exgraph.nodes[currentEdge[1]]['x']), (0, 0, 255), 1)

        cv2.imwrite('resources/output/map' + str(i+1) + "_graphed.png", painted_map)
    

if __name__ == "__main__":
    main()









































