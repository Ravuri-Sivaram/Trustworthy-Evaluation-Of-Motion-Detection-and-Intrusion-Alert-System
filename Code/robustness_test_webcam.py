import cv2
import face_recognition
import numpy as np
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename="robustness_log.txt", level=logging.INFO)

# Initialize webcam
cap = cv2.VideoCapture(0)

print("Press 'l' for Lighting Variation | 'b' for Motion Blur | 'o' for Occluded Faces | 'n' for Noise | 'q' to Quit")

current_mode = None

def apply_lighting_variation(frame):
    return cv2.convertScaleAbs(frame, alpha=0.5, beta=20)

def apply_motion_blur(frame):
    return cv2.GaussianBlur(frame, (15, 15), 0)

def apply_adversarial_noise(frame):
    noise = np.random.randint(0, 50, frame.shape, dtype='uint8')
    return cv2.add(frame, noise)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Apply robustness mode
    modified_frame = frame.copy()
    if current_mode == 'lighting':
        modified_frame = apply_lighting_variation(modified_frame)
    elif current_mode == 'blur':
        modified_frame = apply_motion_blur(modified_frame)
    elif current_mode == 'noise':
        modified_frame = apply_adversarial_noise(modified_frame)
    elif current_mode == 'occlusion':
        # Draw rectangle to simulate mask/sunglasses
        h, w, _ = modified_frame.shape
        cv2.rectangle(modified_frame, (int(w*0.3), int(h*0.4)), (int(w*0.7), int(h*0.55)), (0, 0, 0), -1)

    # Face detection
    rgb_frame = cv2.cvtColor(modified_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)

    # Log results
    scenario = current_mode if current_mode else 'normal'
    if face_locations:
        logging.info(f"{datetime.now()} - {scenario} - Faces Detected: {len(face_locations)}")
    else:
        logging.info(f"{datetime.now()} - {scenario} - No Face Detected")

    # Display
    cv2.putText(modified_frame, f'Mode: {scenario}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Robustness Test Webcam', modified_frame)

    # Key controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('l'):
        current_mode = 'lighting'
    elif key == ord('b'):
        current_mode = 'blur'
    elif key == ord('n'):
        current_mode = 'noise'
    elif key == ord('o'):
        current_mode = 'occlusion'
    elif key == ord('q'):
        break
    elif key == ord('c'):
        current_mode = None  # Clear mode

cap.release()
cv2.destroyAllWindows()
