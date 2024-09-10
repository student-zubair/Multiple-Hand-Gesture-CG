Hand Gesture Controlled System
Overview
This project implements a hand gesture-controlled system using a webcam feed and OpenCV for image processing. It allows you to control the mouse cursor with hand gestures and adjust the system volume through a hand-shaking motion. This functionality is achieved using the cvzone.HandTrackingModule to detect and track hands, pyautogui to control the mouse, and pycaw for system audio control.

Features
Mouse Control:

The right hand is used to control the mouse pointer.
The index finger is mapped to move the mouse, while a pinch gesture (index and middle finger extended) simulates a mouse click.
Volume Control:

The left hand is used to control the system volume.
A shaking motion of the left hand increases or decreases the volume:
Shaking left decreases the volume.
Shaking right increases the volume.
Performance Tracking:

The program tracks the Frames Per Second (FPS) and displays it on the video feed.
Libraries and Dependencies
This project uses the following libraries:

OpenCV: For capturing webcam feed and displaying the video.
cvzone: For hand tracking using the HandTrackingModule.
numpy: For mathematical operations like calculating movement.
pycaw: For controlling system audio.
pyautogui: For mouse control.
collections: To store and track the history of hand movements.
Installation Instructions
To run this project, ensure that you have Python installed and the following libraries set up:

bash
Copy code
pip install opencv-python cvzone numpy pycaw pyautogui comtypes
You might also need to install dependencies for pycaw:

bash
Copy code
pip install comtypes
How It Works
Hand Tracking
Hand Detection: The webcam captures video frames, and the HandTrackingModule detects up to two hands (left and right).
Landmarks: Each hand has 21 landmarks, which are used to calculate gestures and detect specific finger positions.
Mouse Control (Right Hand)
Index Finger: The index finger's position is tracked to move the mouse pointer across the screen.
Click Gesture: A mouse click is simulated when both the index and middle fingers are extended while the ring and pinky fingers are folded.
Volume Control (Left Hand)
Shaking Motion: The program detects the left hand's movement by comparing the change in its position over time (using a history of the last 10 positions).
Threshold for Shake: If the detected movement exceeds a certain threshold, it determines if the shake was towards the left (volume down) or right (volume up).
Volume Adjustment: The volume is controlled using pycaw, with limits set by the system's minimum and maximum volume levels.
Frame Rate Calculation
The program calculates and displays the FPS to monitor performance.

Code Breakdown
Video Capture: Initializes the webcam to capture video frames.
Hand Detection: The HandDetector module is used to detect hand gestures.
Mouse Control: Maps the right-hand index finger movement to mouse cursor movement. A specific gesture is used for mouse clicks.
Volume Control: Tracks the left-hand movement history. A shaking motion either increases or decreases the system volume.
Performance: The frame rate (FPS) is calculated and displayed on the video feed.
Exit Condition: The program will terminate if the user presses the 'q' key.
Usage
Run the Python script.
Position your hands in front of the webcam.
Use your right hand to control the mouse by moving the index finger.
Extend the index and middle fingers to simulate a mouse click.
Use your left hand to adjust the system volume by shaking left or right.
The program displays the current volume percentage and FPS on the screen.
Press 'q' to exit the program.
Future Improvements
Adding more gesture-based functionalities, such as scrolling or switching windows.
Improving accuracy in hand tracking for different lighting conditions.
Customizing the sensitivity and thresholds for hand movements and gestures.
Troubleshooting
Ensure your camera is properly connected and working.
Adjust the lighting in your room to improve hand detection.
Ensure all necessary Python libraries are installed.
