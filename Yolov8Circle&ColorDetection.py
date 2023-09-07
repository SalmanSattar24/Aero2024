from torch import tensor
from ultralytics import YOLO
import cv2
import imutils
import numpy as np
import subprocess


# Load a model
model = YOLO('C:/#~Secondary Files~#/AeroCode/RGBYPcircles.pt')  # or yolov5m, yolov5l, yolov5x, custom
# model.predict(source="0", show=True, conf=0.35)


# load video
video_path = "C:\#~Secondary Files~#\AeroCode\Dronew_Foot\Parkinglot 50 Feet Fast (All Colors) .mp4"
cap = cv2.VideoCapture(video_path) # Chnage this to capture from different sources, 0 is webcam.

# plot_box function
def plot_bboxes(result, frame):
    
    xyxys = []
    confidences = []
    class_ids = []
    
    # Extract detections for each class

    
    # Print out the class ids
    
    pass

ret = True
# read frames from video and process them 
while ret:
    ret, frame = cap.read()


    # detect objects in frames
    # track objects in frames
    results = model.track(frame, persist=True, save=True)
    
    
    
    # calculate the coordinates of the bounding boxes
    # calculate the coordinates of the center of the bounding boxes
    
    for r in results:
        print("======================================")
        print(r.boxes.cls)
        for box in r.boxes.cls:
            if box == 0:
        # The class values for each object is as follows:
        # 0. = Blue, 1. = Green (not tested yet), 2. = Purple, 3. = Red,  4. = Yellow 
                print("box data as tensor")
                
                print(r.boxes.xyxy) # print the coordinates of the bounding boxes
                box_data = np.array(r.boxes.xyxy.cpu().numpy()) # convert the coordinates of the bounding boxes to an array
                print("box data as array")
                print(box_data)# convert the coordinates of the bounding boxes to an array
                # Print the datatype of the numpy array
                print("box data type: " + box_data.dtype.name)
                print("box data ends")
                top_cord = box_data[0][0:2] # get the top left corner coordinates of the bounding box
                bottom_cord = box_data[0][2:4] # get the bottom right corner coordinates of the bounding box
                print(top_cord)
                print(bottom_cord)
                x_top = top_cord[0]
                y_top = top_cord[1]
                x_bot = bottom_cord[0]
                y_bot = bottom_cord[1]
                x_center = (x_top + x_bot)/2
                y_center = (y_top + y_bot)/2
                centerpoint = (x_center, y_center)
                print("center point =", centerpoint)
                print("--------------------------------------")
        pass


    # save video with tracked objects
    # saved_video = model()


    # plot results
    frame_ = results[0].plot()
    frame_ = imutils.resize(frame_, width=1080) # with of my screen is 1536

    # visualize results
    cv2.imshow('frame', frame_)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()