import os
import numpy as np
import cv2 as cv

# Creating a list of all the files in the data folder.
file_names = [f for f in os.listdir(os.path.join(os.getcwd(), 'data'))]

def nothing(x):
    """
    The function takes in an argument x, and does nothing with it
    
    :param x: The current trackbar position
    """
    pass

# Create a black image, a window
cv.namedWindow('image')

# Reading the first image in the data folder and eroding it.
img = cv.imread(f'./data/{file_names[0]}')
kernel = np.ones((5,5),dtype=np.uint8)
img = cv.erode(img, kernel, iterations=1)

# It creates a trackbar for each of the HSV values.
cv.createTrackbar('HMin', 'image', 0, 179, nothing)
cv.createTrackbar('SMin', 'image', 0, 255, nothing)
cv.createTrackbar('VMin', 'image', 0, 255, nothing)
cv.createTrackbar('HMax', 'image', 0, 179, nothing)
cv.createTrackbar('SMax', 'image', 0, 255, nothing)
cv.createTrackbar('VMax', 'image', 0, 255, nothing)

# It sets the maximum value of the trackbar to 179, 255, 255 respectively.
cv.setTrackbarPos('HMax', 'image', 179)
cv.setTrackbarPos('SMax', 'image', 255)
cv.setTrackbarPos('VMax', 'image', 255)

hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

# A loop that keeps updating the image with the new values of the trackbars.
while (1):

    hMin = cv.getTrackbarPos('HMin', 'image')
    sMin = cv.getTrackbarPos('SMin', 'image')
    vMin = cv.getTrackbarPos('VMin', 'image')
    hMax = cv.getTrackbarPos('HMax', 'image')
    sMax = cv.getTrackbarPos('SMax', 'image')
    vMax = cv.getTrackbarPos('VMax', 'image')

    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Converting the image to HSV, then it is creating a mask that is the range of the HSV values, and
    # then it is applying the mask to the image.
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower, upper)
    result = cv.bitwise_and(img, img, mask=mask)

    # Counting the number of non-zero pixels in the mask, and then dividing it by the total number of
    # pixels in the image.
    ratio_green = cv.countNonZero(mask)/(img.size/3)
    cv.imshow('image', result)

    if cv.waitKey(10) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

# Looping through all the files in the data folder and printing the percentage of green pixels in each image.
for file in file_names:
    img = cv.imread(f'./data/{file}')
    kernel = np.ones((5, 5),dtype=np.uint8)
    img = cv.erode(img, kernel, iterations=1)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower, upper)
    result = cv.bitwise_and(img, img, mask=mask)
    ratio_green = cv.countNonZero(mask)/(img.size/3)
    print(f'green pixel percentage for file {file}:', np.round(ratio_green*100, 2))
