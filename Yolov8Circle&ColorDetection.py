from ultralytics import YOLO
import cv2
import imutils


# Load a model
model = YOLO('C:/#~Secondary Files~#/AeroCode/RGBYPcircles.pt')  # or yolov5m, yolov5l, yolov5x, custom
# model.predict(source="0", show=True, conf=0.35)


# load video
video_path = "C:\#~Secondary Files~#\AeroCode\Dronew_Foot\Parkinglot 50 Feet Fast (All Colors) .mp4"
cap = cv2.VideoCapture(video_path)

ret = True
# read frames from video and process them 
while ret:
    ret, frame = cap.read()


    # detect objects in frames
    # track objects in frames
    results = model.track(frame, persist=True)  


    # save video with tracked objects


    # plot results
    frame_ = results[0].plot()
    frame_ = imutils.resize(frame_, width=1080)

    # visualize results
    cv2.imshow('frame', frame_)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break