# lesson 12 of using CV 
    # tracking on color, there rises an issue with what range of BGR is considered green, blue, red, yellow,...
    # the first part of this program demonstrated this by showing that a green screen has a wide range of pixel values when sampling from the camera feed
    # even tho it is a solid color in real life or in the eyes of humans
    # a new way to think about colors is needs
# hue HSV color space
    # hue = "color value" as an angle between 0 and 360, defines colors across the rainbow
    # saturation = color amount from 0 to 255 for any hue
    # value = how much black is in the color and saturation (goes from black to hue, saturation values)
    # picture a 3D cylinder with 3 data points to be mapped
    # hue is a angle in range (0,179), each incriments represents 2 degrees. 
    # saturation (0,255)
    # value range (0,255) value of 0 is black and value of 255 is no black
        # this is vary helpful bc now we can track on the HUE value. As witnessed in the excersise,the hue is alot 
        # more consistant clicking on objects in frame with the same color. Lets say you wanted to track on yellow, all 
        # you would need to do is find the min and max angle for a range you would consider yellow in the color wheel.
        # Track across 1 parameter instead of 3... GOOD SHIT
        
import cv2
import numpy as np

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

# colors
blue = (255,0,0)
red = (0,0,255)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)

# text parameters
th = 1
fontScale = 1

# camera Parameters
width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW) # 
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30) 
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG')) 

cv2.namedWindow('1') 
cv2.setMouseCallback('1',mouseClick)

while True:
    _ ,frame = cam.read() 
    if evt ==1:
        x = np.zeros([250,250,3],dtype=np.uint8) 
        y = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # converts the frame to Hue/sat/value
        clr = y[yVal][xVal] # takes color value from mouse click spot

        print("color of mouse spot",clr)

        x[:,:] = clr # set blank window to HSV value

        cv2.putText(x,str(clr),(0,50),cv2.FONT_HERSHEY_COMPLEX,fontScale,black,th)
        cv2.imshow('Color Picker', x)
        cv2.moveWindow('Color Picker',width,0)
        evt=0
    cv2.imshow('1',frame) 
    cv2.moveWindow('1',0,0) 
    
    if cv2.waitKey(1) & 0xff == ord('q'): 
        break
cam.release()