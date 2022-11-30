import cv2 as cv
import math
import os
import pandas as pd

op = open("op2.txt", "w")

def detect(imgpath, target):
    ip = cv.imread(imgpath)
    # ip1 = cv.resize(ip, (1000,1000))
    # cv.imshow('input', ip1)
    
    if(ip is None):
        print("Image not found")
        return

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3), (2,2))
    cv.morphologyEx(src=ip, dst=ip, op=cv.MORPH_CLOSE, kernel=kernel, anchor=(-1,-1), iterations=7)
    # ip1 = cv.resize(ip, (1000,1000))
    # cv.imshow('canvasOutput', ip1);
    

    # cv.waitKey(0)
    
    iw = ip.shape[1]
    
    imgOriginal = ip

    imgEdges = cv.Canny(imgOriginal, 120, 240)

    contours, hierarchy = cv.findContours(imgEdges, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)



    ci = 0
    cj = 0

    minEllipses = [0 for i in range(len(contours))]
    selEllipses = [0 for i in range(len(contours))]
    selContours = []
    for ci in range(len(contours)):
        if(len(contours[ci]) > 500):
            minEllipses[ci] = cv.fitEllipse(contours[ci])
            if (minEllipses[ci][0][0]>=imgOriginal.shape[1]/2-400 
            and minEllipses[ci][0][0]<=imgOriginal.shape[1]/2+400
            and minEllipses[ci][0][1]>=imgOriginal.shape[0]/2-350 
            and minEllipses[ci][0][1]<=imgOriginal.shape[1]/2+350):
                selEllipses[cj] = minEllipses[ci];
                selContours.append(contours[ci]);
                cj += 1;
    
    for ci in range(1,cj):
        if(cv.contourArea(selContours[ci])>cv.contourArea(selContours[0])):
            selEllipses[0] = selEllipses[ci]
            selContours[0] = selContours[ci]

    image = cv.ellipse(imgOriginal,selEllipses[0],(0,0,255),10);
    # ip1 = cv.resize(image, (1000,1000))
    # cv.imshow('input', ip1)
    # cv.waitKey(0)
    xret = selEllipses[0][0][0];
    yret = selEllipses[0][0][1];
    k = selEllipses[0][1][1]/selEllipses[0][1][0];
    # print(k)

    w = selEllipses[0][2]*3.14/180
    al = math.sqrt(-((math.cos(w)*math.cos(w)*(k*k-1))/(pow(math.sin(w),2)*(1-k*k)-1)))
    be = math.sqrt(-(math.sin(w)*math.sin(w)*(1-k*k)))
    op.write(str(math.asin(al)*180/3.14) + "," + str(math.asin(be)*180/3.14) + "," + str(target) + "\n")

    # print("a, b: ", math.asin(al)*180/3.14, ", ", math.asin(be)*180/3.14, "\n")
    
    # img = imgOriginal
    # img = cv.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)))
    # cv.namedWindow("rims"+imgpath, cv.WINDOW_AUTOSIZE);
    # cv.imshow("rims"+imgpath, img);

    return xret,yret,iw
    

if __name__ == '__main__':
    op.write("a,b,target\n")
    mainpath = os.getcwd() + "/python/bw/"
    folder = "U3TL000"
    np = ["/Negative x/", "/Negative y/", "/Positive x/", "/Positive y/"]
    for j in range(1,3):
        for i in range(4):
            path = mainpath + folder + str(j) + np[i]

            dir_list = os.listdir(path)

            for file in dir_list:
                filename = file[8:]
                imgcam = path + folder + str(j) + filename
                xl,yl,iw = detect(imgcam,i)

    dataframe = pd.read_csv("op2.txt", delimiter=',')
    
    dataframe.to_csv('op2.csv', index = None)

    
    # xr,yr,iw = detect(imgcam2)

    # f = iw/(2*math.tan(0.4887/2))

    # b = 0.2;
    # d = math.fabs(xr-xl);
    # Z = f*b/d
    # print(Z)
    # X = xl*Z/f;
    # Y = yl*Z/f;
    # print("X, Y: ",X,", ",Y)
    # print("Z: ",Z)
    # print("D: ",math.sqrt(X*X+Y*Y+Z*Z))
    # cv.waitKey(0);