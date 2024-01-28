'''
The file reads an image pgm file and identifies the frontier cells in the image.

Frontier cells are defined as occupied cells adjacent to gray cells. 
Tasks:
1. Read the image file, identify the background cell color, obstacle cell color, and unoccupied cell color.
2. Find the unoccupied cells adjacent to the background cells.
3. Create a list of frontier cells.
4. Change color of frontier cells to a different color.
5. Save the image as a new .png file.
'''

# -- import packages
import numpy as np
import cv2
import matplotlib.pyplot as plt

def read_image(filename):
    '''
    Reads an image file and returns the image as a numpy array.
    '''
    img = cv2.imread(filename,0)
    assert img is not None, "file could not be read, check with os.path.exists()"
    return img


def get_frontier_image(img, save_temp_images=False):
    # -- identify background cell color, obstacle cell color, and unoccupied cell color
    background_color = 205
    obstacle_color = 0
    unoccupied_color = 254

    # -- increase the obstacle cell size by 10 pixels
    # -- threshold obstacle cells
    ret, thresh = cv2.threshold(img,obstacle_color,255,cv2.THRESH_BINARY)
    # -- save the threshold image
    if save_temp_images:
        cv2.imwrite('map_threshold.png',thresh)
    # -- erode the cells
    kernel = np.ones((10,10),np.uint8)
    eroded = cv2.erode(thresh,kernel,iterations = 1)
    # -- save the eroded image
    if save_temp_images:
        cv2.imwrite('map_eroded.png',eroded)

    # -- overlay the eroded cells on the original image
    # -- save the overlay image
    overlay = img.copy()
    overlay[eroded == 0] = 0
    if save_temp_images:
        cv2.imwrite('map_overlay.png',overlay)


    # -- find unoccupied cells adjacent to background cells
    # -- create a list of frontier cells
    frontier_cells = []
    frontier_img = np.zeros_like(img)
    for i in range(1, overlay.shape[0]-1):
        for j in range(1, overlay.shape[1]-1):
            if overlay[i,j] == unoccupied_color:
                if overlay[i-1,j] == background_color or \
                        overlay[i+1,j] == background_color or \
                        overlay[i,j-1] == background_color or \
                        overlay[i,j+1] == background_color:
                    frontier_cells.append((i,j))
                    frontier_img[i,j] = 254

    # -- change color of frontier cells to a different color
    #for i in range(len(frontier_cells)):
        #img[frontier_cells[i]] = 100

    # -- dilate and erode the frontier cells to remove noise
    #kernel = np.ones((3,3),np.uint8)
    #frontier_dilated = cv2.dilate(frontier_img,kernel,iterations = 1)
    #frontier_eroded = cv2.erode(frontier_dilated,kernel,iterations = 1)
    #frontier_eroded = frontier_dilated
    # -- save the frontier image
    #if save_temp_images:
        #cv2.imwrite('map_frontier.png', frontier_img)
        #cv2.imwrite('map_frontier.png', frontier_eroded)
    
    # -- return the frontier image
    return frontier_cells

if __name__ == "__main__":
    # -- read the image file
    img = read_image('resources/map1.pgm')
    # -- get the frontier image
    frontier = get_frontier_image(img)
    # -- show frontier image
    cv2.imshow('frontier', frontier)
    cv2.waitKey(0)