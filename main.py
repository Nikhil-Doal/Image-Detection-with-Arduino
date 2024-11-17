import cv2 as cv
from teachable_machine import TeachableMachine
import serial
import time
from PIL import Image
import numpy as np
import tempfile
import os

# Initialize serial communication with Arduino
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

# Load the model and labels from TeachableMachine, you may need to use the direct file path
model = TeachableMachine(model_path=r"keras_model.h5",
                         labels_file_path=r"labels.txt")
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read() 
    if not ret:
        print("Failed to grab frame")
        break

    pil_image = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))  # Convert BGR (OpenCV format) to RGB (PIL format)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_file_path = temp_file.name
        pil_image.save(temp_file_path)

    # Classify the current frame in realtime using the temporary file path
    result = model.classify_image(temp_file_path)
    
    # Get the predicted class name and confidence
    class_name = result["class_name"]
    class_confidence = result["class_confidence"]

    # Draw a rectangle around the frame - Rectange has no real function
    height, width, _ = frame.shape
    start_point = (50, 50)  
    end_point = (width - 50, height - 50)  
    color = (0, 255, 0)  # Green
    thickness = 2  
    cv.rectangle(frame, start_point, end_point, color, thickness)

    # Display the class name and confidence on the frame
    text = f'{class_name} ({class_confidence:.2f})'
    font = cv.FONT_HERSHEY_SIMPLEX
    org = (50, 40)  # Starting position of the text
    font_scale = 1
    font_color = (0, 255, 0)  # Green, for visibility
    thickness = 2
    cv.putText(frame, text, org, font, font_scale, font_color, thickness, cv.LINE_AA)

    # Console for debugging
    # Check if action is detected and control the LED
    if class_name == "1 action" and class_confidence > 0.8:  # You can adjust the confidence threshold
        print(f"Action detected with confidence: {class_confidence}. Sending '1' to Arduino to turn ON the LED.")
        arduino.write(b'1')  # Send '1' to turn on the LED
    else:
        print(f"Idle or low confidence. Sending '0' to Arduino to turn OFF the LED.")
        arduino.write(b'0')  # Send '0' to turn off the LED

    # Display the video feed with detection results
    cv.imshow("Video Stream with Detection", frame)

    # Clean up the temporary file
    os.remove(temp_file_path)

    # Break the loop when 'q' is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv.destroyAllWindows()
arduino.close()  # Close the serial connection to Arduino
