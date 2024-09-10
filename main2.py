import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import pyautogui
import collections
import time

# Initialize the video capture
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Initialize pycaw for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume_range = volume.GetVolumeRange()
min_volume = volume_range[0]
max_volume = volume_range[1]

# Parameters
position_history_left = collections.deque(maxlen=10)  # Store the last 10 positions for left hand
shake_threshold = 60  # Movement threshold to detect a shake
screen_width, screen_height = pyautogui.size()

def calculate_movement(history):
    movement = 0
    for i in range(1, len(history)):
        movement += np.linalg.norm(np.array(history[i]) - np.array(history[i-1]))
    return movement

# For performance tracking
prev_time = time.time()
frame_count = 0
fps = 0

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)  # With Draw

    if hands:
        left_hand = None
        right_hand = None

        # Assign hands based on their position
        for hand in hands:
            if hand["type"] == "Left":
                left_hand = hand
            else:
                right_hand = hand

        # Handle right hand for mouse control
        if right_hand:
            lmList_right = right_hand["lmList"]
            centerPoint_right = right_hand["center"]
            fingers_right = detector.fingersUp(right_hand)

            # Mouse control
            index_finger = lmList_right[8]  # Index finger tip

            # Convert the coordinates
            x = np.interp(index_finger[0], [0, 640], [0, screen_width])
            y = np.interp(index_finger[1], [0, 480], [0, screen_height])

            # Move the mouse
            pyautogui.moveTo(screen_width - x, y)

            # Mouse click
            if fingers_right[1] == 1 and fingers_right[2] == 1 and fingers_right[3] == 0 and fingers_right[4] == 0:
                pyautogui.click()
                print("Mouse Click")

        # Handle left hand for volume control
        if left_hand:
            lmList_left = left_hand["lmList"]
            centerPoint_left = left_hand["center"]

            # Track hand positions
            position_history_left.append(centerPoint_left)

            if len(position_history_left) == position_history_left.maxlen:
                movement = calculate_movement(position_history_left)

                # Check shake movement every few frames to reduce computation
                if frame_count % 5 == 0:
                    if movement > shake_threshold:
                        # Determine direction of shake
                        if position_history_left[-1][0] > position_history_left[0][0]:
                            # Shake right - increase volume
                            new_vol = min(max_volume, volume.GetMasterVolumeLevel() + 2)
                            volume.SetMasterVolumeLevel(new_vol, None)
                            print("Volume Up")
                        else:
                            # Shake left - decrease volume
                            new_vol = max(min_volume, volume.GetMasterVolumeLevel() - 2)
                            volume.SetMasterVolumeLevel(new_vol, None)
                            print("Volume Down")

            # Display the volume level on the image
            current_vol = volume.GetMasterVolumeLevel()
            cv2.putText(img, f'Volume: {int(np.interp(current_vol, [min_volume, max_volume], [0, 100]))}%', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Frame rate calculation
    frame_count += 1
    current_time = time.time()
    if current_time - prev_time >= 1:
        fps = frame_count
        frame_count = 0
        prev_time = current_time

    cv2.putText(img, f'FPS: {fps}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
