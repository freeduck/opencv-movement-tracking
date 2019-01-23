import numpy as np
import cv2
import time
import pygame
from findcircle_blob import circleposition
import pickle


undistinfo = pickle.load(open("undistinfo.p","rb"))
mtx = undistinfo['mtx']
dist = undistinfo['dist']

cap = cv2.VideoCapture('../Videos/Webcam/2017-12-20-223500.webm')

start = time.time()
clock = pygame.time.Clock()
newcameramtx = []

while(cap.isOpened()):
    clock.tick(30)
    ret, frame = cap.read()
    h,  w = frame.shape[:2]
    if not len(newcameramtx):
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    # undistort
    #time1 = time.time()
    #frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    #time2 = time.time()
    #print '%s function took %0.3f ms' % ("undist", (time2-time1)*1000.0)

    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    thresh = 0
    maxValue = 255
    print "CAP type" + str(type(cap))
    [oldx,oldy] = [0,0]
    
    params = cv2.SimpleBlobDetector_Params()
    
    # Change thresholds
    #params.minThreshold = 10;
    #params.maxThreshold = 200;
     
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 75
     
    # Filter by Circularity
    #params.filterByCircularity = True
    #params.minCircularity = 0.8
     
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.87
     
    # Filter by Inertia
    #params.filterByInertia = True
    #params.minInertiaRatio = 0.01
     
    
    detector = cv2.SimpleBlobDetector(params)

        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #npcap = np.array(cap,dtype='float32')
    th, dst = cv2.threshold(gray, thresh, maxValue, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    cv2.imshow("threshold", dst)
     
    # Detect blobs.
    keypoints = detector.detect(dst)
    print "keypoints" + str(keypoints)
    if len(keypoints) > 0: 
        keypoint = [keypoints[-1]]
    else:
        keypoint = []
    print "keypoint" + str(keypoint)
    print keypoint[0].pt
    point = np.array([keypoint[0].pt],dtype='float32')
    print point
    #point = np.array([keypoint])
    #point = np.array(keypoint)
    #print type(np.array(keypoint))
    time1 = time.time()
    point = cv2.undistortPoints(np.array([point]), mtx, dist, None, newcameramtx)
    time2 = time.time()
    print '%s function took %0.3f ms' % ("undist", (time2-time1)*1000.0)
    dst = cv2.undistort(gray, mtx, dist, None, newcameramtx)
    hest = point[0][0]
    hest[0] = int(hest[0])
    hest[1] = int(hest[1])
    print "Hest"
    print hest
    #pts = np.float([keypoints[idx].pt for idx in len(keypoints)]).reshape(-1,1,2) 
    #pts = np.float(keypoints[1].pt).reshape(-1,1,2)
    #print "pts" + str(pts) 
    #keypoint[0].pt = hest
     
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    #im_with_keypoints = cv2.drawKeypoints(gray, point, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.circle(dst,(hest[0],hest[1]), 10, (0,0,255), -1)
     
    #cv2.imshow("im_with_keypoints", gray)
    cv2.imshow("im_with_keypoints", dst)
    
 
    cv2.waitKey(0)

end = time.time()

print "Duration {0}".format(end-start)
cap.release()
cv2.destroyAllWindows()
