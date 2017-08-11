import numpy as np
import cv2
import collections

import sys
sys.path.append("../lib/")
import game 

RAD = 26
ROWS = 6
COLS = 7
# how many pictures to average the circle detection over. HSV is very
# jumpy, so we add this many images together 
PIC_AVG = 10

# Map colors to openCV H range
COLORS = { "RED": {"hues":(9, 175), "sats":(191,255), "vals":(109,253)} ,
            "YELLOW": {"hues":(20,), "sats":(182,240), "vals":(119,202)},
            "BOARD": {"hues":(20,), "sats":(182,240), "vals":(119,202)},
            }
# set up the arrays for the initial image and the kernel for Guassian
# blur
img = np.zeros((312, 512,3), np.uint8)

kernel = np.ones((5,5),np.float32)/25
# the collections module lets us build a stack of the last ten images
# so we get more consistent detection
# Callback for the trackbars

def find_tiles(cap):
    cap_count = 0
    found_circles = list()
    masksum = None
    do_once = 1 
    while(cap.isOpened()):
        ret, img = cap.read()
            
        while(cap_count < PIC_AVG):
            cap_count += 1

            if ret == True:
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                hue = COLORS["BOARD"]
                lower = np.array([hue["hues"][0] -7, hue["sats"][0], hue["vals"][0]])
                upper = np.array([hue["hues"][0] +7, hue["sats"][1], hue["vals"][1]])
                mask = cv2.inRange(hsv,lower,upper)
                if (cap_count == 1):
                    masksum = mask
                else:
                    masksum = cv2.bitwise_or(masksum, mask)
               
                masksum = cv2.GaussianBlur(masksum, (5,5), 3)
        
        if (do_once):
            do_once = 0
            edges = cv2.Canny(masksum, 30,90, apertureSize=5)
            
                
            circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT  , 1, 20, param1=100, param2=19, minRadius=RAD/2, maxRadius=RAD)
            if not circles is None:
                dupe = 0
                circles = np.uint16(np.around(circles))
                for i in circles[0,:]:
                    for j in found_circles:
                        if (abs(int(i[0]) - int(j[0] ))< RAD/2 and abs(int(i[1] )- int(j[1])) < RAD/2) :
                                
                            dupe = 1
                    if (dupe == 0): 
                        found_circles.append([i[0], i[1]])
            
            cv2.imshow("edges", edges)
            cv2.imshow("masksum", masksum)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    return (found_circles)


if __name__ == "__main__":
# Set up the camera for 800 x 600 
    cap = cv2.VideoCapture(0)
    cap.set(3,800)
    cap.set(4,600)

    new_game = game.Game(COLS, ROWS)
    print(new_game.showBoard())

    circles = find_tiles(cap)
    print("Circles: {}".format(circles))
    new_game.setTiles(circles)
    tiles = new_game.getTiles()
    while(cap.isOpened()):
   
        ret, img = cap.read()

        #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
       
        
        for tile in tiles:
            roi = img[tile[1]-5:tile[1] + 5, tile[0]-5:tile[0]+5]
            m = cv2.mean(roi)
            if (m[2] > 100 ) and (m[0] < 50):
                print(m)
                if m[1] > 100 :
                    print("Yellow")    
                    cv2.circle(img,(tile[0],tile[1]),5, (0,255,0),2)
                    cv2.circle(img,(tile[0],tile[1]),RAD, (m[0],m[1], m[2]),2)
                elif (m[1] < 25):
                    print("Red")
                    
                    cv2.circle(img,(tile[0],tile[1]),5, (0,255,0),2)
                    cv2.circle(img,(tile[0],tile[1]),RAD, (m[0],m[1], m[2]),2)
                
       

        #for tile in tiles:    
        #    cv2.circle(img,(tile[0],tile[1]),RAD, (0,255,0),2)
        #for circ in circles:
        #    cv2.circle(img,(circ[0],circ[1]),RAD, (255,0,0),2)
        
        cv2.imshow("Board", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

