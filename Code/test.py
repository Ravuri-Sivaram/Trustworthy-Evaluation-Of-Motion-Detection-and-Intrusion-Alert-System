import cv2
import imutils
import numpy as np
import threading
from playsound import playsound
import mail
from sklearn.metrics import precision_score, recall_score, f1_score

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not found!")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()

# Check if the first frame is captured properly
if start_frame is None:
    print("Error: Failed to capture initial frame!")
    cap.release()
    exit()

start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0

# Evaluation variables for motion detection
motion_true_positives = 0
motion_false_positives = 0
motion_false_negatives = 0
motion_true_negatives = 0

# Add this function to update motion detection metrics
def update_motion_metrics(motion_detected, actual_motion):
    global motion_true_positives, motion_false_positives, motion_false_negatives, motion_true_negatives

    if motion_detected and actual_motion:
        motion_true_positives += 1  # Correctly detected motion
    elif motion_detected and not actual_motion:
        motion_false_positives += 1  # False alarm
    elif not motion_detected and actual_motion:
        motion_false_negatives += 1  # Missed detection
    else:
        motion_true_negatives += 1  # No motion detected, correct prediction

def beep_alarm():
    global alarm
    while alarm_mode:
        print("ALARM")
        playsound('alarm.mp3')

while True:
    _, frame = cap.read()

    # If the frame is not captured successfully, break
    if frame is None:
        print("Error: Failed to capture image from camera.")
        break

    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_btw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_btw = cv2.GaussianBlur(frame_btw, (5, 5), 0)

        difference = cv2.absdiff(start_frame, frame_btw)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_btw

        if threshold.sum() > 10000:
            alarm_counter += 1
            if alarm_counter > 20:
                if not alarm:
                    alarm = True
                    threading.Thread(target=beep_alarm).start()
                    threading.Thread(target=mail.send_email, args=(frame, frame, frame, frame, frame)).start()
                
                # Assume actual_motion as ground truth for evaluation
                update_motion_metrics(True, True)  # This should be dynamically set based on actual motion
        else:
            if alarm_counter > 0:
                alarm_counter -= 1
        
        # Calculate Precision, Recall, and F1-Score for motion detection
        motion_precision = precision_score([motion_true_positives], [motion_false_positives], zero_division=0)
        motion_recall = recall_score([motion_true_positives], [motion_false_negatives], zero_division=0)
        motion_f1 = f1_score([motion_precision], [motion_recall])

        print(f"Motion Detection - Precision: {motion_precision}, Recall: {motion_recall}, F1-Score: {motion_f1}")

        cv2.imshow("Cam", threshold)
    elif not alarm_mode and alarm:
        black_frame = np.zeros_like(frame)
        cv2.imshow("Cam", black_frame)
    else:
        cv2.imshow("Cam", frame)

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord('t'):
        print("You have activated/deactivated the alarm!")
        alarm_mode = not alarm_mode
        alarm_counter = 0
    elif key_pressed == ord('q'):
        print("Quitting the program!")
        alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()
