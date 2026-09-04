import cv2
import matplotlib.pyplot as plt
import statistics as st

def preform_math(x_found):
     """this is to find the amount of pixel between the two"""
     if not x_found:
         return 0
     else:
        distance = x_found[-1] - x_found[0]
        return distance

def find_colors(y, x_found, img):
    """This is to find the colors and loop for the horizontal pixels and see if they are white"""
    # The value of a droplet and cropping the area that is processed
    low = 160
    x_min = 137
    x_max = 4745
    y_min = 1600
    y_max = 5327

    for x in range(img.shape[1]):
        #looping through each pixle and
        bgr_color = img[y, x]
        blue = int(bgr_color[0])
        green = int(bgr_color[1])
        red = int(bgr_color[2])

        #check the pixel to see if it is as droplet
        if (blue >= low) and (green >= low) and (red >= low) and (x > x_min) and (x < x_max) and (y > y_min) and (y < y_max):
            x_found.append(x)     
    dist = preform_math(x_found)
    return dist
   
def loop_image(img):
    """This is to loop verticlly through the image"""
    x_found = []
    all_dist = []
    for y in range(img.shape[0]):
        distance = find_colors(y, x_found, img)   
        all_dist.append(distance)      
    return all_dist  

#The images that are used
img = cv2.imread("photos/test1.jpg")
img = cv2.imread("photos/test2.jpg")


def display(img):
    """This is to display the results"""
    all_dist = loop_image(img)
    mean_dist = st.mean(all_dist)
    results = f"The average distance in Pixels is {mean_dist:.0f} Pixels. "
    print(results)

    #plt.imshow(img)
    #plt.title("Distance between the droplets for Viral's expirements")
    #plt.xlabel("X - Axis")
    #plt.ylabel("Y - Axis")
    #plt.show()
display(img)


