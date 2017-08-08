import numpy as np
import cv2
import collections

# how many pictures to average the circle detection over. HSV is very
# jumpy, so we add this many images together 
PIC_AVG = 10

# Map colors to openCV H range
#4_COLORS = {"RED":5, "YELLOW": 22.5}

# Set up the camera for 800 x 600 
cap = cv2.VideoCapture(0)
cap.set(3,800)
cap.set(4,600)


# Window for display
cv2.namedWindow('image')

# set up the arrays for the initial image and the kernel for Guassian
# blur
img = np.zeros((312, 512,3), np.uint8)
kernel = np.ones((5,5),np.float32)/25

# the collections module lets us build a stack of the last ten images
# so we get more consistent detection
img_history = collections.deque(maxlen=PIC_AVG)
found_circles = list()
# Callback for the trackbars
def nothing(x):
        pass


cv2.createTrackbar('Hue', 'image', 0,180,nothing)
cv2.createTrackbar('Sat', 'image', 0,255,nothing)
cv2.createTrackbar('Sat_hi', 'image', 0,255,nothing)
cv2.createTrackbar('Val', 'image', 0,255,nothing)
cv2.createTrackbar('Val_hi', 'image', 0,255,nothing)
cv2.setTrackbarPos('Hue', 'image', 4)
cv2.setTrackbarPos('Sat', 'image', 191)
cv2.setTrackbarPos('Sat_hi', 'image', 255)
cv2.setTrackbarPos('Val', 'image', 109)
cv2.setTrackbarPos('Val_hi', 'image', 255)

while(cap.isOpened()):
        ret, img = cap.read()

        if ret == True:
                compcount += 1
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                hue = cv2.getTrackbarPos('Hue', 'image')

                sat = cv2.getTrackbarPos('Sat', 'image')
                sat_hi = cv2.getTrackbarPos('Sat_hi', 'image')
                val = cv2.getTrackbarPos('Val', 'image')
                val_hi = cv2.getTrackbarPos('Val_hi', 'image')
                if hue == -1:
                    break
                #print(" {} {} {} {} {}".format(hue, sat, sat_hi, val, val_hi))
                lower = np.array([hue-10, sat, val])
                upper = np.array([hue+10, sat_hi, val_hi ])

                mask = cv2.inRange(hsv,lower,upper)
                masksum = mask
#               mask = cv2.GaussianBlur(mask, (5,5), 3)
                for i in img_history:
                   masksum = cv2.bitwise_or(masksum, i)
                circles = cv2.HoughCircles(masksum, cv2.HOUGH_GRADIENT  , 1, 30, param1=100, param2=17, 
                        minRadius=5, maxRadius=20)
                if not circles == None:
                        dupe = 0
                        circles = np.uint16(np.around(circles))
                        for i in circles[0,:]:
                            for j in found_circles:
                                if (abs(int(i[0]) - int(j[0] ))<7 and abs(int(i[1] )- int(j[1])) < 7) :
                                        dupe = 1
                            if (dupe == 0): 
                                print("Adding")
                                print(i)
                                found_circles.append(i)
                for i in found_circles:    
                    cv2.circle(img,(i[0],i[1]),13, (0,255,0),2)

                cv2.imshow('image', img)
                cv2.imshow('Mask', mask)
                cv2.imshow('MaskComposite', mask2)
                img_history.append(mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()

