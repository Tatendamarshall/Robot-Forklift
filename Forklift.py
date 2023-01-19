import pySerial
import pyRobot
import cv2
import numpy as np
import winsound

# Connect to the microcontroller or controller
ser = serial.Serial('COM3', 9600)

# Initialize the forklift object
forklift = pyRobot.Forklift()

# Initialize the cameras
camera1 = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(1)
camera3 = cv2.VideoCapture(2)
camera4 = cv2.VideoCapture(3)

# Set the collision distance threshold
collision_distance = 0.5  # meters

while True:
    # Get the images from the cameras
    ret1, frame1 = camera1.read()
    ret2, frame2 = camera2.read()
    ret3, frame3 = camera3.read()
    ret4, frame4 = camera4.read()

    frames = [frame1, frame2, frame3, frame4]
    for frame in frames:
        # Convert the image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect edges in the image
        edges = cv2.Canny(gray, 50, 150)

        # Find contours in the image
        _, contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate over the contours
        for contour in contours:
            # Get the moments of the contour
            moments = cv2.moments(contour)

            if moments["m00"] != 0:
                # Get the centroid of the contour
                x = int(moments["m10"] / moments["m00"])
                y = int(moments["m01"] / moments["m00"])

                # Calculate the distance from the centroid to the forklift
                distance = calculate_distance(x, y)

                # Check if the distance is less than the collision distance threshold
                if distance < collision_distance:
                    # Play a warning beep sound
                    winsound.Beep(2000, 500)
                    # Stop the forklift
                    forklift.stop()
                    ser.write('S')
                    break
    # Move the forklift forwards
    forklift.move_forwards()
    ser.write('F')

# Release the cameras
camera1.release()
camera2.release()
camera3.release()
camera4.release()
