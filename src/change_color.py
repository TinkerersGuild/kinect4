import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,800)
cap.set(4,600)
cv2.namedWindow('image')

img = np.zeros((312, 512,3), np.uint8)
kernel = np.ones((5,5),np.float32)/25
mask2 = None
foundcircles = list()
def nothing(x):
	pass
compcount = 0
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
                if mask2 == None:
                    mask2 = mask
#		mask = cv2.GaussianBlur(mask, (5,5), 3)
                mask2 = cv2.bitwise_or(mask, mask2)
                circles = cv2.HoughCircles(mask2, cv2.HOUGH_GRADIENT  , 1, 30, param1=100, param2=17, 
                        minRadius=5, maxRadius=20)
                if not circles == None:
                        dupe = 0
                        circles = np.uint16(np.around(circles))
                        for i in circles[0,:]:
                            for j in foundcircles:
                                if (abs(int(i[0]) - int(j[0] ))<7 and abs(int(i[1] )- int(j[1])) < 7) :
                                        dupe = 1
                            if (dupe == 0): 
                                print("Adding")
                                print(i)
                                foundcircles.append(i)
                for i in foundcircles:    
                    cv2.circle(img,(i[0],i[1]),13, (0,255,0),2)

		cv2.imshow('image', img)
		cv2.imshow('Mask', mask)
		cv2.imshow('MaskComposite', mask2)
                if compcount >= 100:
                    mask2 = None
                    #foundcircles = list()

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()

