from ultralytics import YOLO
import cv2


# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch
#model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data="config.yaml", epochs=1    )  # train the model
# metrics = model.val()  # evaluate model performance on the validation set
# results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
# path = model.export(format="onnx")  # export the model to ONNX format


# colors
blue = (255,0,0)
red = (0,0,255)
green = (0,255,0)

# camera Parameters
width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW) # 
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30) 
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG')) 

while True:
    _ ,frame = cam.read() 
    cv2.imshow('1',frame) 
    cv2.moveWindow('1',0,0) 
    
    if cv2.waitKey(1) & 0xff == ord('q'): 
        break
cam.release() 





