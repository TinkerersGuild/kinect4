import numpy as np
import cv2
import collections

# how many pictures to average the circle detection over. HSV is very
# jumpy, so we add this many images together 
PIC_AVG = 30

# Map colors to openCV H range
COLORS = { "RED": {"hues":(9, 175), "sats":(191,255), "vals":(109,253)} ,
            "YELLOW": {"hues":(20,), "sats":(150,240), "vals":(160,255)}
            }
board = list()
# Set up the camera for 800 x 600 
cap = cv2.VideoCapture(0)
cap.set(3,800)
cap.set(4,600)


# Window for display
cv2.namedWindow('image')

# set up the arrays for the initial image and the kernel for Guassian
# blur
img = np.zeros((312, 512,3), np.uint8)
#harris = np.zeros((312,512,3), CV_32FC1)
kernel = np.ones((5,5),np.float32)/25

# the collections module lets us build a stack of the last ten images
# so we get more consistent detection
img_history = collections.deque(maxlen=PIC_AVG)
found_circles = list()
# Callback for the trackbars
def nothing(x):
        pass


while(cap.isOpened()):
        ret, img = cap.read()

        if ret == True:
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                hue = COLORS["YELLOW"]
                lower = np.array([hue["hues"][0] -10, hue["sats"][0], hue["vals"][0]])
                upper = np.array([hue["hues"][0] +10, hue["sats"][1], hue["vals"][1]])
                mask = cv2.inRange(hsv,lower,upper)
                mask = cv2.GaussianBlur(mask, (5,5), 3)
               
                #mask = np.float32(mask)
                masksum = mask
                for i in img_history:
                    masksum = cv2.bitwise_or(masksum, i)
                masksum = cv2.GaussianBlur(masksum, (5,5), 3)
                edges = cv2.Canny(masksum, 30,90, apertureSize=5)
                
                # lines = cv2.HoughLines(edges,1, np.pi/180,5)
                # for rho,theta in lines[0]:
                #     a = np.cos(theta)
                #     b = np.sin(theta)
                #     x0 = a*rho
                #     y0 = b*rho
                #     x1 = int(x0 + 1000*(-b))
                #     y1 = int(y0 + 1000*(a))
                #     x2 = int(x0 - 1000*(-b))
                #     y2 = int(y0 - 1000*(a))

                #     cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
                circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT  , 1, 20, param1=100, param2=19, 
                        minRadius=5, maxRadius=30)
                if not circles is None:
                    dupe = 0
                    circles = np.uint16(np.around(circles))
                    for i in circles[0,:]:
                        for j in found_circles:
                            if (abs(int(i[0]) - int(j[0] ))<7 and abs(int(i[1] )- int(j[1])) < 7) :
                                
                                dupe = 1
                        if (dupe == 0): 
                           # print("Adding")
                            #print(i)
                            found_circles.append(i)
                for i in found_circles:    
                    cv2.circle(img,(i[0],i[1]),10, (0,255,0),2)

                #img2, cont,hier = cv2.findContours(masksum, 1, 2)
                #for cnt in cont:
                 #   approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
                    
                  #  if len(approx) > 15:
                   #     print(len(approx))
                    #    cv2.drawContours(img,[cnt],0,255,-1)

                #x,y,w,h = cv2.boundingRect(cnt)
                #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

#                 for k,v in COLORS.items():
#                     print(k)
#                     for hue in v["hues"]:

#                         lower = np.array([hue-4, v["sats"][0], v["vals"][0]])
#                         upper = np.array([hue+4, v["sats"][1], v["vals"][1]])
    

#                         mask = cv2.inRange(hsv,lower,upper)
#                         masksum = mask
# #               
#                         for i in img_history:
#                             masksum = cv2.bitwise_or(masksum, i)
#                         circles = cv2.HoughCircles(masksum, cv2.HOUGH_GRADIENT  , 1, 30, param1=100, param2=17, 
#                         minRadius=10, maxRadius=20)
#                         if not circles is None:
#                             dupe = 0
#                             circles = np.uint16(np.around(circles))
#                             for i in circles[0,:]:
#                                 for j in found_circles:
#                                     if (abs(int(i[0]) - int(j[0] ))<7 and abs(int(i[1] )- int(j[1])) < 7) :
#                                         dupe = 1
#                                 if (dupe == 0): 
#                                     print("Adding")
#                                     print(i)
#                                     found_circles.append(i)
#                     for i in found_circles:    
#                         cv2.circle(img,(i[0],i[1]),13, (0,255,0),2)

                cv2.imshow('image', img)
                cv2.imshow('corners?', edges)

#               cv2.imshow('mask', mask)
                img_history.append(mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()

