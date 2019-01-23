import cv2
import cv2.cv as cv
import numpy as np
import math
import random
import os.path
import pickle
import cProfile
import time
from kallibrer import kallibrer
from findcircle_blob import circleposition
from puckmovement import puck_movement

def main():
    count = 0
    cap = cv2.VideoCapture(0)
     
    undistinfo = pickle.load(open("undistinfo.p","rb"))
    mtx = undistinfo['mtx']
    dist = undistinfo['dist']
    ret, frame = cap.read()
    h,  w = frame.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    dest = np.array([ [0,0],[1299,0],[1299,699],[0,699] ],np.float32)
    warp,mask,maskcorners,frame = kallibrer(cap,dest,newcameramtx,mtx,dist)
    time1 = time.clock()
    
    h,  w = frame.shape[:2]
    
    framewarp = cv2.warpPerspective(frame,warp,(w,h))

    for p in circleposition(cap,warp,newcameramtx,mtx,dist,mask,maskcorners):
        count = count + 1
        framecopy = framewarp
        cv2.circle(framecopy,(p[0],p[1]),10,(0,0,255),1)  #Red
        #cv2.circle(framecopy,(p[0][0],p[0][1]),10,(0,0,255),1)  #Red
        #cv2.circle(framecopy,(p[1][0],p[1][1]),10,(0,255,0),1) #Green
        #cv2.circle(framecopy,(p[2][0],p[2][1]),10,(255,0,0),1) #Blue
        #if count > 100:
        #    break
            
        cv2.imshow('framecopy',framecopy)    
    
    time2 = time.clock()
    print 'clocktime %0.3f' % (time2-time1)

main()    
    

