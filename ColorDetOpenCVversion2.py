import cv2
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Define color ranges for detection (in HSV)
color_ranges = {
    'Green': ([38, 100, 100], [85, 255, 255]),
    'Red': ([0, 100, 100], [10, 255, 255]),
    'Red': ([160, 100, 100], [180, 255, 255]),
    'Blue': ([90, 100, 100], [134, 255, 255]),
    'Yellow': ([26, 70, 90], [40, 255, 255]),
    'Orange': ([11, 100, 100], [20, 255, 255]),
    'Purple': ([125, 100, 100], [150, 255, 255]),
    'Pink': ([150, 50, 50], [170, 255, 255]),
    'Brown': ([10, 100, 50], [30, 255, 150]),  # Adjusted brown range
    'Black': ([0, 0, 0], [180, 255, 30]),
    'White': ([0, 0, 200], [180, 30, 255]),
    'Gray': ([0, 0, 100], [180, 30, 200])
}

# Function to detect the color based on its average color
def detect_color(avg_color):
    for color_name, (lower, upper) in color_ranges.items():
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)
        avg_color_pixel = np.array([[avg_color]], dtype=np.uint8)
        mask = cv2.inRange(avg_color_pixel, lower_bound, upper_bound)
        if mask.any():
            return color_name
    return 'Other'

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Apply Gaussian blur to the frame
    blurred = cv2.GaussianBlur(hsv_frame, (9, 9), 2)
    
    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(
        blurred[:, :, 2],  # Use the V channel for circle detection
        cv2.HOUGH_GRADIENT, # Use the Hough gradient method
        dp=1, # The inverse ratio of resolution
        minDist=20, # Minimum distance between circles
        param1=50, # Upper threshold for Canny edge detection
        param2=30, # Threshold for center detection
        minRadius=5, # Minimum radius
        maxRadius=100 # Maximum radius
    )
    
    # Process detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, radius = circle[0], circle[1], circle[2]
            
            # Extract region of interest (ROI) around the circle
            roi = hsv_frame[y - radius:y + radius, x - radius:x + radius]
            
            # Calculate the average color of the ROI
            avg_color = np.mean(roi, axis=(0, 1))
            
            # Detect the color of the circle
            color = detect_color(avg_color)
            
            # Draw a circle and label it with the detected color
            cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
            cv2.putText(frame, color, (x - radius, y - radius - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # Display the frame with circle detection
    cv2.imshow('Circle Detection', frame)
    
    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
