import cv2
import numpy as np

def circleposition(cap,transform):
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
    params.minArea = 100
     
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.8
     
    # Filter by Convexity
    #params.filterByConvexity = True
    #params.minConvexity = 0.87
     
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
    #pts = np.float([keypoints[idx].pt for idx in len(keypoints)]).reshape(-1,1,2) 
    #pts = np.float(keypoints[1].pt).reshape(-1,1,2)
    #print "pts" + str(pts) 
     
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(gray, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
     
    cv2.imshow("im_with_keypoints", im_with_keypoints)
    
    #cv2.waitKey(0)
        
        
