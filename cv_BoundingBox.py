'''
Created on 2017. 10. 19.

@author: danny
'''
import cv2 #opencv-python
import numpy as np
import imutils
from PIL import Image

# downsample and use it for processing
img = cv2.pyrDown(cv2.imread('./images/0001.jpg', cv2.IMREAD_UNCHANGED))
# apply grayscale
small = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# morphological gradient
morph_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
grad =cv2.morphologyEx(small, cv2.MORPH_GRADIENT, morph_kernel)
# binarize
_, bw = cv2.threshold(src=grad, thresh=0, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
# connect horizontally oriented regions
connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, morph_kernel)
mask = np.zeros(bw.shape, np.uint8)
# find contours
im2, contours, hierarchy = cv2.findContours(connected, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

count = 0
# filter contours
for idx in range(0, len(hierarchy[0])):
    rect = x, y, rect_width, rect_height = cv2.boundingRect(contours[idx])
    # fill the contour
    mask = cv2.drawContours(mask, contours, idx, (255, 255, 255), cv2.FILLED)
    # ratio of non-zero pixels in the filled region
    r = float(cv2.countNonZero(mask)) / (rect_width * rect_height)
    if r > 0.45 and rect_height > 20 and rect_width > 25: # 여기서 bounding box 를 조절해주는 것 같다. 
        img = cv2.rectangle(img, (x, y+rect_height), (x+rect_width, y), (0,255,0),3)
    
    count = count + 1
    
    print("Y-h,X-w :", img[y:y+rect_height, x:x+rect_width].shape)
    #cv2.imwrite("./Images/try"+str(count)+".jpg", img[y:y+rect_height,x:x+rect_width])
    cv2.imwrite("./HI/four"+str(count)+".png", img[y:y+rect_height,x:x+rect_width], [int(cv2.IMWRITE_PNG_COMPRESSION), 5])
    
W = 700.
height, width, depth = img.shape
imgScale = W/width

newX, newY = img.shape[1]*imgScale, img.shape[0]*imgScale

newimg = cv2.resize(img, (int(newX),int(newY))) 

cv2.imshow("contours", newimg)

ESC = 27
while True:
    keycode = cv2.waitKey()
    if keycode != -1:
        keycode != 0xFF
        if keycode == ESC:
            break
