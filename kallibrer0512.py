import numpy as np
import cv2

corners = []
clicked = False

ffframe = None
clickcount = 0

def onMouse(event, x, y, flags, param):
    global clicked
    global ffframe
    global clickcount
    global corners
    print("MOUSE" + str(x) + " " + str(y) + " " + str(cv2.EVENT_LBUTTONUP) + " " + str(event))
    if event == cv2.EVENT_LBUTTONUP:
        print("mouse")
        cv2.circle(ffframe,(x,y),10,(0,0,255),-1)
        clicked = True
        clickcount = clickcount + 1
        corners.append((x,y))
   
def kallibrer(cap,dest,newcameramtx,mtx,dist):        
    global ffframe
    global clickcount
    
    if type(cap) is np.ndarray:
        frame = cap
        success = True
    else:
        success, frame = cap.read()
        success, frame = cap.read()
        

    frame = cv2.undistort(frame, mtx, dist, None, newcameramtx) 
     
    ffframe=frame   
    #fframe=cv2.flip(frame,0)
    #ffframe=cv2.flip(fframe,1)


    blurred = cv2.GaussianBlur(ffframe, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    ##dest = np.array([ [0,0],[1299,0],[1299,699],[0,699] ],np.float32)




    cv2.namedWindow('img')
    cv2.setMouseCallback('img', onMouse)

    cv2.imshow('img',ffframe)

    clickcount = 0

    while success and cv2.waitKey(1) == -1 and clickcount < 4:
        cv2.imshow('img',ffframe)
        pass

    cv2.waitKey(10)
    cv2.destroyWindow('img')


    npacorners = np.array(corners,np.float32)
    maskcorners = np.array(corners,dtype=np.int32)
    #maskcorners = np.array([[542, 107], [562, 102], [582, 110], [598, 142], [600, 192], [601, 225], [592, 261], [572, 263], [551, 245], [526, 220], [520, 188], [518, 152], [525, 127], [524, 107]],dtype=np.int32)
    
    transform = cv2.getPerspectiveTransform(npacorners,dest)
    
    mask = np.zeros((ffframe.shape[0], ffframe.shape[1]))

    cv2.fillConvexPoly(mask, maskcorners,1)
    mask = mask.astype(np.bool)
    out = np.zeros_like(ffframe)
    cv2.imshow('out before mask',out)
    cv2.waitKey(100)
    out[mask] = ffframe[mask] 
    cv2.imshow('out after mask',out)
    cv2.waitKey(100)
    
    print("transform:")
    print(transform)
    return [transform,mask,maskcorners,ffframe]



##cv2.destroyAllWindows()
