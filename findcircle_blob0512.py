import cv2
import numpy as np 
import time

def circleposition(cap,transform,newcameramtx,mtx,dist,mask,maskcorners):
    thresh = 0
    maxValue = 255
    #print "CAP type" + str(type(cap))
    [oldx,oldy] = [0,0]
    #print "maskcorners %s" % str(maskcorners)
    params = cv2.SimpleBlobDetector_Params()
    
    # Change thresholds
    #params.minThreshold = 10;
    #params.maxThreshold = 200;
     
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 125
    params.maxArea = 375
    
     
    # Filter by Circularity
    #params.filterByCircularity = True
    #params.minCircularity = 0.8
     
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.87
     
    # Filter by Inertia
    #params.filterByInertia = True
    #params.minInertiaRatio = 0.01     
    ret, frame = cap.read()
    detector = cv2.SimpleBlobDetector_create(params)
    h,  w = frame.shape[:2]
    done = False
    l=[[1,1],[1,1],[1,1]]
    while True:
        time1 = time.clock()
        ret, frame = cap.read()
        if frame is None:
            return
            
        frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        ffframe=frame
        
        ulx = maskcorners[0][0] -20 ##sorg for ikke at ryge udenfor billede
        uly = maskcorners[0][1] -20
        brx = maskcorners[2][0] + 20
        bry = maskcorners[2][1] + 20
        
        ffframe = ffframe[uly:bry,ulx:brx]
        
        gray = cv2.cvtColor(ffframe, cv2.COLOR_BGR2GRAY)

        th, dst = cv2.threshold(gray, thresh, maxValue, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        # Detect blobs.
        dtime1 = time.clock()
        keypoints = detector.detect(dst)
        dtime2 = time.clock()
        #print('detector %0.6f' % (dtime2-dtime1))
        #print "keypoints" + str(keypoints)
        
        #for k in keypoints:
        #    print("respovce {}".format(k.response))
        
        if len(keypoints) > 0: 
            keypoint = [keypoints[-1]]
        else:
            keypoint = None
            
        #print "keypoint" + str(keypoint)
        if keypoint is not None:
            #print keypoint[0].pt
            circle = keypoint[0].pt
            #circlesize = keypoint[0].size
            #print("Size {}".format(keypoint[0].size))
            #cv2.waitKey(5000)
            #print "im alive"
            im_with_keypoints = cv2.drawKeypoints(ffframe, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            cv2.imshow("im_with_keypoints", im_with_keypoints)
            #cv2.imshow("out", out)
            
            #cv2.waitKey(1)
            print("point diff")
            print(np.absolute(circle[0]-l[2][0])) 
            print(np.absolute(circle[1]-l[2][1]))
            #if (np.absolute(c) > 12 or np.absolute(circle[1]-l[2][1]) > 12): ## and (np.absolute(circle[0]-l[2][0]) < 100 or np.absolute(circle[1]-l[2][1]) < 100):
            l.append([int(circle[0]+ulx),int(circle[1]+uly)])
            l=l[1:]
            #else:
            #    raise Exception("hej")
        else:
            print("else")
            continue
        
        adpoint = np.array(l[2],dtype='float32')
        point = np.array([[l[2]]],dtype='float32')
        pointOut = cv2.perspectiveTransform(point, transform)   

        [[[xo,yo]]]=pointOut
        
        time2 = time.clock()
        print('findcircle clocktime %0.6f' % (time2-time1))

        yield [xo,yo,im_with_keypoints,keypoint[0].size]
        
