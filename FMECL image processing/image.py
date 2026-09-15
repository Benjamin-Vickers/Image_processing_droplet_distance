import cv2
import matplotlib.pyplot as plt
import os

# This script is set up in a way that starts with looping through all the verticle values of the image,
#  then each iteration of this loop calls a function which then loops through all of the Horizontal Values 
# of the images and checks to see if the color is light enough to be considered a droplet on the RBG color scale,
#  the culmination of these two funcitons is a list which contains the first detected x values light enough
#  to be considered a droplet and the last value light enough to be considered a droplet, this information is
#  then poassed into a function what finds the distance between then and converts in to mm, this is then used
#  to plot the graph showing the width of the droplet stream in this image, the two values that get returned
#  from the starting function are used to make the red bars which show the user what parts of the photo are used


# color value that is considered light enough to be a droplet
low = 120

# Adjust these based on the where in the images you would like to measure, to crop the image
x_min = 1500
x_max = 3500
y_min = 1600
y_max = 5300


#The images that are used
img = cv2.imread("C:/Users/Owner/OneDrive/Documents/coding/fall_2026/FMECL image processing/photos/test1.jpg")
#img = cv2.imread("C:/Users/Owner/OneDrive/Documents/coding/fall_2026/FMECL image processing/photos/test3.jpg")




def find_colors_for_each_pixel(y, img):
    """finds the colored pixels and gives the x locations in a list x_found which is passed"""
    x_found = []

    # looping through all of the x values to see if they are light enough to be a droplet
    for x in range(img.shape[1]):
        bgr_color = img[y, x]
        blue = int(bgr_color[0])
        green = int(bgr_color[1])
        red = int(bgr_color[2])

        #check the pixel to see if it is a droplet
        if (blue >= low) and (green >= low) and (red >= low) and (x > x_min) and (x < x_max) and (y > y_min) and (y < y_max):
            x_found.append(x)    

    # checking to make sure the list is not empty
    if not x_found:
        pass
    else:
        return x_found


# start reading the code here
def loop_of_verticle_values(img):
    """Loops through all the verticle values in the image and for each calls find_colors_for_each_pixel()  """
    width = []
    for y in range(img.shape[0]):
        x_distance = find_colors_for_each_pixel(y,  img) 

        # If statement is used to remove NoneTypes from the returned of x locations where droplets are found, creates a list of lists with the first and last location
        if x_distance != None:
            width.append([x_distance[0], x_distance[-1]])
    return width
droplet_width_list = loop_of_verticle_values(img)


def find_distance(droplet_width_list):
    """to find the width of the stream and convert to mm to be used in the plot, (0.0530 mm = 1 pixel)"""
    distance_list = []
    for i in range(len(droplet_width_list)):
        distance = (droplet_width_list[i][-1] - droplet_width_list[i][0])  * 0.053
        distance_list.append(distance)
    return distance_list
distance_list = find_distance(droplet_width_list)


def find_x_values():
    """to find the x values of the graph used (0.0530 mm = 1 pixel)"""
    counted_values = []
    for i in range(len(distance_list)):
        i = (i + 1500) * 0.053
        counted_values.append(i)
    return counted_values



def plotting(img, distance_list):
    """Creates two plots left being the width vs location and the right showing the user what pixels are being measured"""
    counted_values = find_x_values()
    fig, (ax1,ax2) = plt.subplots(1,2, figsize=(10,6))
    plt.subplots_adjust(wspace=0.3,hspace=3)

    # The left plot showing the width of stream
    ax1.plot(counted_values, distance_list)
    ax1.grid(True)

    # The right plot showing the image being measured
    count = 1500
    for i in range(len(droplet_width_list)):
        count += 1
        img1 = cv2.line(img, (droplet_width_list[i][0], count), (droplet_width_list[i][1], count), (255, 0, 0), 1)
    ax2.imshow(img1)

    # Labels
    plt.suptitle("Droplet Stream measurements")
    ax1.set_title("Width of the droplet stream V. Y position. ")
    ax1.set_ylabel("Distance Between X values (mm)")
    ax1.set_xlabel("Y position (mm)")

    ax2.set_title("Image being alalyzed red bars show what is being measured")
    ax2.set_ylabel("Y - Axis (pixels)")
    ax2.set_xlabel("X - Axis (pixels)")
    plt.show()
plotting(img, distance_list)
