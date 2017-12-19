'''
Created on 2017. 10. 26.

@author: danny
'''
import cv2
import numpy as np
img = cv2.imread('.\Images/0001.jpg')
img_original = img.copy()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#p1 : 원점에서 거리 50
#p2 : 각도가 150
#p3 : Aperture size for the Sobel() operator[Sobel() 연산을 위한 조리개 사이즈]
edges = cv2.Canny(gray, 50,150, apertureSize = 3)

#p1 : edges
#p2 : rho accuracies(픽셀은 라디안단위로 측정됨)
#p3 : theta accuracies
#p4 : threshold(탐지되는 최소의 거리)
lines = cv2.HoughLines(edges, 1, np.pi/180, 700)



for line in lines:
    for rho,theta in line:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 3000*(-b))
        y1 = int(y0 + 3000*(a))
        x2 = int(x0 - 3000*(-b))
        y2 = int(y0 - 3000*(a))
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        print(x1,y1, x2,y2)

res = np.vstack((img_original,img))
cv2.imwrite("kakaka2.jpg",res)

W = 500.
#height, width, depth = edges.shape
height, width, depth = res.shape
imgScale = W/width

newX, newY = res.shape[1]*imgScale, res.shape[0]*imgScale

newimg = cv2.resize(res, (int(newX),int(newY)))
