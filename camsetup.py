import cv2
#import cv2.cv as cv

cap = cv2.VideoCapture(0)

cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 1200,800)
while True:
    ret, frame = cap.read()

    cv2.imshow('frame',frame)
    cv2.imshow('image',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
