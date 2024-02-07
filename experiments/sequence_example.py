#!/usr/bin/python3

# Importing external Libraries
import cv2
import numpy as np
import networkx as nx
import random as rd
import math
import time

#Importing internal Libraries
import src.PRM_main as prm













def main():

    # Loading the different maps
    maps =  []
    for i in range(8):
        maps.append("resources/input/map" + (i + 1) + ".pgm")
    
    for i in range(8):
        print(maps[i])

if __name__ == "__main__":
    main()









































