# this code will ignore everything but the object of insterest based on color 
# uses mouse clcik function to find the HSV value of pixel with a click
# creates a tracker bar to dial in the HSV filters
# creates another window that is just the object of interest taken out of the frame

import cv2
import numpy as np

# colors
blue = (255,0,0)
red = (0,0,255)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)

# text parameters
th = 1
fontScale = 1

# track bar functions ---------------------------------------------
def Track1(val):
    global huelow
    huelow=val
    print('Hue Low',huelow)
def Track2(val):
    global huehigh
    huehigh=val
    print('Hue high',huehigh)
def Track3(val):
    global satlow
    satlow=val
    print('Sat Low',satlow)
def Track4(val):
    global sathigh
    sathigh=val
    print('Sat High',sathigh)
def Track5(val):
    global valuelow
    valuelow=val
    print('Value Low',valuelow)
def Track6(val):
    global valuehigh
    valuehigh=val
    print('Value high',valuehigh)
def Track7(val):
    global huelow2
    huelow2=val
    print('Hue Low',huelow2)
def Track8(val):
    global huehigh2
    huehigh2=val
    print('Hue high',huehigh2)

# mouse click functions -------------------------------------------------
# mouse click function
evt = 0
xVal = 0
yVal = 0
def mouseClick(event,xPos,yPos,flags,params):
    global evt
    global xVal
    global yVal
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Mouse Event was: ",event)
        print("at position: ",xPos,yPos)
        evt = event # 1
        xVal = xPos
        yVal = yPos
        evt = event
    if event == cv2.EVENT_RBUTTONUP:
        
        evt = event # 5 
        print("Mouse Event was: ",event)
        print("at position: ",xPos,yPos)

# camera Parameters
width=int(640/2)
height=int(360/2)
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW) # 
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30) 
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG')) 

# track bars for dialing in color HSV
cv2.namedWindow('my tracker')
cv2.resizeWindow('my tracker',300,350)
cv2.moveWindow('my tracker', width*3,0)
cv2.createTrackbar('Hue Low','my tracker',10,179,Track1)
cv2.createTrackbar('Hue High','my tracker',20,179,Track2)
cv2.createTrackbar('Hue Low 2','my tracker',10,179,Track7)
cv2.createTrackbar('Hue High 2','my tracker',20,179,Track8)
cv2.createTrackbar('Sat Low','my tracker',10,255,Track3)
cv2.createTrackbar('Sat High','my tracker',250,255,Track4)
cv2.createTrackbar('Value Low','my tracker',10,255,Track5)
cv2.createTrackbar('Value High','my tracker',250,255,Track6)


# mouse click to find HSV value of spot in frame to then track
cv2.namedWindow('1')
cv2.setMouseCallback('1',mouseClick)

huelow = 10
huehigh = 20
satlow=10
sathigh=250
valuelow=10
valuehigh=250

while True:
    _ ,frame = cam.read()
    # finding HSV value for an object in frame
    if evt ==1:
        x = np.zeros([250,250,3],dtype=np.uint8) 
        y = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # converts the frame to Hue/sat/value
        clr = y[yVal][xVal] # takes color value from mouse click spot

        print("color of mouse spot",clr)

        x[:,:] = clr # set blank window to HSV value

        cv2.putText(x,str(clr),(0,50),cv2.FONT_HERSHEY_COMPLEX,fontScale,black,th)
        cv2.imshow('Color Picker', x)
        cv2.moveWindow('Color Picker',width+300,0)
        evt=0

# turn frame to HSV
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
# set bounds to be adjusted with the tracker bar
    lowbound = np.array([huelow,satlow,valuelow])
    upbound = np.array([huehigh,sathigh,valuehigh])
    lowbound2 = np.array([huelow2,satlow,valuelow])
    upbound2 = np.array([huehigh2,sathigh,valuehigh])
# create mask
    Mask=cv2.inRange(frameHSV,lowbound,upbound)
    Mask2=cv2.inRange(frameHSV,lowbound2,upbound2)
    Mask_composite = Mask | Mask2 # or the two masks 
    # Mask_composite = cv2.add(Mask,Mask2) # can also add the two masks together
    cv2.imshow('mask',Mask)
    cv2.moveWindow('mask',0,height+70)
    cv2.imshow('mask 2',Mask2)
    cv2.moveWindow('mask 2',width,height+70)
# frame of just ROI
    object = cv2.bitwise_and(frame,frame,mask=Mask_composite)
    cv2.imshow('object',object)
    cv2.moveWindow('object',width*2,height+70)
    #original frame
    cv2.imshow('1',frame) 
    cv2.moveWindow('1',0,0) 
    
    if cv2.waitKey(1) & 0xff == ord('q'): 
        break
cam.release() 