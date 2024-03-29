# PRM_CV2
Probablistic Road Maps (PRM) designed for the purpose of building exploration graphs using Open CV2 and Networkx, written in Python.

## Required Dependencies
* cv2
* numpy
* networkx
* matplotlib.pyplot

## How to format the Networkx graphs
This library uses Networkx graphs to build the graphs generated by the roadmaps. If you input an empty graph into the prm() function than you do not have to worry about the formating the function will take care of it for you. If you want to add things to the graph before hand such as a starting node than follow this formatting
* The name of the node needs to be an Int
* The x coordinate of the node is stored in the 'x' attribute
* The y coordinate of the node is stored in the 'y' attribute

Here is an example of how to add a node:
> Exgraph.add_node(1)

Here is an example of how to add the coordinates (0, 0) to a node:
> Exgraph.nodes[1]['x'] = 0; 
> Exgraph.nodes[1]['y'] = 0

## What images to use
This libary is designed to use .pgm files which is a grayscale file format
* Collision free space is denoted as a color of 254
* Obstacles are denoted as a color of 0
* Unknown / Unexplored space is denoted as a color of 205

## Example of output
Here is an example of how the output might look. This example is map 2 in a 2 map sequence, meaning that one map came before it. Note that the visual display you see here is recreated in sequence_example.py to help you visualize what the graph looks like. But this is not implemented else where.

![Map 2 before graphing](/resources/assets/cropped_map2.png)
![Map 2 after graphing](/resources/assets/cropped_PRM_map2.png)

## Contributions
The frontier identification for this code was written by [Kenzo450D](https://github.com/Kenzo450D).
